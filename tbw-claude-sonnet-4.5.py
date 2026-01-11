#!/usr/bin/env python3
#  tbw‑gpt‑oss20b.py
#  Minimal SSD SMART fetch for macOS

import subprocess, plistlib, re, sys

# --------------------------------------------------------------------
# Helper – run a command and return stdout, or None if it fails
# --------------------------------------------------------------------
def run(cmd):
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=False, timeout=10
        )
        # smartctl returns non-zero codes for warnings but still provides data
        # Return output if we got stdout, regardless of return code
        if result.stdout:
            return result.stdout
        return None
    except (subprocess.TimeoutExpired, Exception):
        return None

# --------------------------------------------------------------------
# Detect whole‑disk SSDs ("/dev/diskX")
# --------------------------------------------------------------------
def get_ssd_nodes():
    plist_bytes = run(['diskutil', 'list', '-plist'])
    if not plist_bytes:
        return []

    plist = plistlib.loads(plist_bytes)
    
    nodes = []
    # Check each disk in AllDisks
    for disk in plist.get('AllDisks', []):
        # Only check whole disks (disk0, disk1, not partitions like disk0s1)
        if not re.match(r'^disk\d+$', disk):
            continue
        
        # Get detailed info for this disk
        info_bytes = run(['diskutil', 'info', '-plist', disk])
        if not info_bytes:
            continue
        
        info = plistlib.loads(info_bytes)
        # Check if it's a whole disk, solid state, and NOT virtual
        if info.get('WholeDisk') and info.get('SolidState') and info.get('VirtualOrPhysical') != 'Virtual':
            nodes.append(f"/dev/{disk}")
    
    return nodes

# --------------------------------------------------------------------
# smartctl – try the most common device types
# --------------------------------------------------------------------
def smartctl_output(node):
    # Try without sudo first, then with sudo
    for use_sudo in (False, True):
        for d in ('nvme', 'sat', 'scsi', ''):
            cmd = []
            if use_sudo:
                cmd.append('sudo')
            cmd += ['smartctl', '-a']
            if d:                      # "-d sat" / "-d nvme" / "-d scsi"
                cmd += ['-d', d]
            cmd.append(node)

            out = run(cmd)
            if out:                    # first one that succeeds
                return out.decode(errors='ignore')
    return None

# --------------------------------------------------------------------
# Extract comprehensive metrics from SMART output
# --------------------------------------------------------------------
def parse_metrics(raw):
    metrics = {}
    
    for line in raw.splitlines():
        line_lower = line.lower()
        
        # Temperature
        if 'temperature' in line_lower and ':' in line:
            m = re.search(r'(\d+)\s*(?:celsius|c)', line, re.IGNORECASE)
            if m:
                metrics['Temperature'] = f"{m.group(1)} °C"
        
        # Power On Hours
        if 'power on hours' in line_lower or 'power_on_hours' in line_lower:
            m = re.search(r'(\d+)', line)
            if m:
                hours = int(m.group(1))
                days = hours // 24
                metrics['Power On Hours'] = f"{hours:,} hours ({days:,} days)"
        
        # Data Units Written (NVMe)
        if 'data units written' in line_lower:
            m = re.search(r'([\d,]+)', line)
            if m:
                units = int(m.group(1).replace(',', ''))
                # Each unit is typically 512KB
                tbw = (units * 512) / (1024 * 1024)
                metrics['TBW (Data Units)'] = f"{tbw:.2f} TB"
        
        # Host Writes (NVMe alternative)
        if 'host write commands' in line_lower or 'host writes' in line_lower:
            m = re.search(r'([\d,]+)', line)
            if m:
                metrics['Host Writes'] = m.group(1)
        
        # Percentage Used / Wear Leveling
        if 'percentage used' in line_lower or 'available spare' in line_lower:
            m = re.search(r'(\d+)%?', line)
            if m:
                metrics['Wear Level'] = f"{m.group(1)}%"
        
        # Media Errors
        if 'media and data integrity errors' in line_lower or 'media errors' in line_lower:
            m = re.search(r'(\d+)', line)
            if m:
                metrics['Media Errors'] = m.group(1)
        
        # Critical Warning
        if 'critical warning' in line_lower:
            m = re.search(r'0x([0-9a-f]+)', line, re.IGNORECASE)
            if m:
                val = int(m.group(1), 16)
                metrics['Critical Warning'] = f"0x{m.group(1)} {'(OK)' if val == 0 else '(WARNING!)'}"
    
    return metrics

# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------
def main():
    print("=" * 70)
    print("         SSD SMART REPORT - Complete Diagnostics")
    print("=" * 70)
    print("\n⚠️  Note: This script may require sudo privileges to access SMART data.")
    print("    Trying without sudo first, then with sudo if needed.\n")
    
    nodes = get_ssd_nodes()
    if not nodes:
        print('⚠️  No SSDs detected.')
        print('Tip: Make sure smartmontools is installed (brew install smartmontools)')
        return
    
    for node in nodes:
        print(f'\n{"=" * 70}')
        print(f'  DISK: {node}')
        print(f'{"=" * 70}\n')
        
        raw = smartctl_output(node)
        if not raw:
            print(f'❌  smartctl failed for {node}')
            print('Try running: sudo smartctl -a', node)
            continue
        
        # Parse metrics first
        metrics = parse_metrics(raw)
        
        # Display key metrics summary
        if metrics:
            print("┌" + "─" * 68 + "┐")
            print("│" + " KEY METRICS SUMMARY".center(68) + "│")
            print("├" + "─" * 68 + "┤")
            for key, value in metrics.items():
                print(f"│  {key:<30} {value:>35} │")
            print("└" + "─" * 68 + "┘")
            print()
        
        # Full SMART output
        print("┌" + "─" * 68 + "┐")
        print("│" + " FULL SMART DATA".center(68) + "│")
        print("└" + "─" * 68 + "┘")
        print()
        print(raw)
        print()

if __name__ == '__main__':
    main()
