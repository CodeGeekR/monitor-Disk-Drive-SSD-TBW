#!/usr/bin/env python3
#  tbw‑gpt‑oss20b.py
#  Minimal SSD SMART fetch for macOS

import subprocess, plistlib, re, sys

# --------------------------------------------------------------------
# Helper – run a command and return stdout, or None if it fails
# --------------------------------------------------------------------
def run(cmd):
    try:
        return subprocess.run(
            cmd, capture_output=True, check=True, text=False
        ).stdout
    except subprocess.CalledProcessError:
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
    for entry in plist.get('AllDisksAndPartitions', []):
        # whole disk + solid‑state → true SSD
        if entry.get('Whole') and entry.get('SolidState'):
            nodes.append(entry.get('DeviceNode', f"/dev/{entry['disk']}"))
    return nodes

# --------------------------------------------------------------------
# smartctl – try the most common device types
# --------------------------------------------------------------------
def smartctl_output(node):
    for d in ('sat', 'nvme', 'scsi', ''):
        cmd = ['smartctl', '-a']
        if d:                      # "-d sat" / "-d nvme" / "-d scsi"
            cmd += ['-d', d]
        cmd.append(node)

        out = run(cmd)
        if out:                    # first one that succeeds
            return out.decode(errors='ignore')
    return None

# --------------------------------------------------------------------
# Quick metric extraction
# --------------------------------------------------------------------
def parse_metrics(raw):
    temp = tbw = wear = None
    for line in raw.splitlines():
        if 'Temperature_Celsius' in line:
            m = re.search(r'\d+', line)
            temp = int(m.group()) if m else None
        elif 'Total_Lifetime_Megabytes_Written' in line:
            m = re.search(r'[\d.]+', line)
            if m:
                tbw_mb = float(m.group())
                tbw = tbw_mb / 1_048_576      # MB → TB
        elif 'Wear_Leveling_Count' in line:
            m = re.search(r'[\d.]+', line)
            wear = float(m.group()) if m else None
    return temp, tbw, wear

# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------
def main():
    nodes = get_ssd_nodes()
    if not nodes:
        print('⚠️  No SSDs detected.')
        return

    for node in nodes:
        print(f'=== {node} ===')
        raw = smartctl_output(node)
        if not raw:
            print(f'❌  smartctl failed for {node}')
            continue

        # Full SMART dump
        print(raw)

        # Quick summary
        temp, tbw, wear = parse_metrics(raw)
        if temp:   print(f'Temp : {temp} °C')
        if tbw:    print(f'TBW  : {tbw:.2f} TB')
        if wear:   print(f'Wear : {wear}%')
        print()

if __name__ == '__main__':
    main()

