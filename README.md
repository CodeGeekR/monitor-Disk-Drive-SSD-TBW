# 🤖 AI Code Battle: Open Source vs Claude Sonnet 4.5

## SSD SMART Monitoring Script Showdown

> **TL;DR**: We tested 4 AI models on generating a macOS SSD monitoring script. Results might surprise you! 🔥

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/macOS-Compatible-success.svg)](https://www.apple.com/macos/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📊 The Challenge

**Task**: Create a Python script that reads and displays complete SSD SMART data on macOS, including:
- Temperature
- Total Bytes Written (TBW)
- Power On Hours
- Wear Level
- Media Errors
- Full SMART output

**Models Tested**:
1. 🏆 **Claude Sonnet 4.5** (Anthropic) - Premium AI
2. 🥈 **Nemotron 3 Nano** (NVIDIA) - Open Source
3. 🥉 **Qwen3 Coder 30B** (Alibaba) - Open Source
4. 🔴 **GPT-OSS-20B** (Open Source) - Failed completely
5. 🔴 **Devstral Small 2** (Mistral AI) - Open Source

---

## 🏆 Results Summary

| Rank | Model | Status | Key Features | Score |
|------|-------|--------|--------------|-------|
| **🥇 1st** | **Claude Sonnet 4.5** | ✅ **PERFECT** | Auto-detect, No sudo needed, Beautiful UI, Smart error handling | **10/10** |
| **🥈 2nd** | **Nemotron 3 Nano** | ✅ **SUCCESS** | Complete data, Works well, Requires sudo, **Fast & Efficient** | **8.5/10** |
| **🥉 3rd** | **Qwen3 Coder 30B** | ⚠️ **PARTIAL** | Functional but poor UX, Hard-coded sudo | **6/10** |
| **4th** | **GPT-OSS-20B** | ❌ **FAILED** | No SSD detection, Wrong logic, **High GPU usage** | **1/10** |
| **5th** | **Devstral Small 2** | ❌ **FAILED** | Wrong device paths, Doesn't understand macOS | **2/10** |

---

## 🔬 Detailed Analysis

### 🏆 1st Place: Claude Sonnet 4.5 (Premium AI)
**Score: 10/10** | [View Script](tbw-claude-sonnet-4.5.py)

```
✅ Auto-detects physical SSDs (filters virtual APFS containers)
✅ Intelligent sudo handling (tries without, fallback if needed)
✅ Beautiful formatted output with tables
✅ Extracts all key metrics:
   • Temperature: 28°C
   • TBW: 8,022.20 TB
   • Power On Hours: 251h (10 days)
   • Wear Level: 0%
   • Media Errors: 0
✅ Complete SMART data dump
✅ Proper error handling (handles smartctl exit codes)
✅ Professional code quality
```

**Sample Output**:
```
======================================================================
         SSD SMART REPORT - Complete Diagnostics
======================================================================

┌────────────────────────────────────────────────────────────────────┐
│                         KEY METRICS SUMMARY                        │
├────────────────────────────────────────────────────────────────────┤
│  Critical Warning                                         0x00 (OK) │
│  Temperature                                                  28 °C │
│  Wear Level                                                      0% │
│  TBW (Data Units)                                        8022.20 TB │
│  Power On Hours                                 251 hours (10 days) │
│  Media Errors                                                     0 │
└────────────────────────────────────────────────────────────────────┘
```

**Why it wins**: Perfect execution, no sudo needed for the user, beautiful presentation, and enterprise-grade error handling.

---

### 🥈 2nd Place: Nemotron 3 Nano (Open Source)
**Score: 8.5/10** | [View Script](tbw-nemotron-3-nano.py)

```
✅ Auto-detects disk (/dev/disk0)
✅ Shows complete SMART output
✅ All data visible:
   • Temperature: 28 Celsius ✅
   • Data Units Written: 16,429,485 [8.41 TB] ✅
   • Power On Hours: 251 ✅
   • All metrics present ✅
⚠️  Requires user to run with sudo
⚠️  No metric extraction (raw output only)
⚠️  User must read through full output
```

**What it does well**: 
- Gets the job done! All data is there and correct
- Very close to Claude's functionality
- Clean, readable output
- Reliable detection

**What could be better**:
- Needs manual sudo (user must remember to type "sudo python3 script.py")
- Doesn't parse metrics into a summary table
- Less polished UI

**Verdict**: **Impressive performance for an open-source model!** Shows that open-source AI is catching up fast. With minor improvements, it could match Claude.

**⚡ Performance Highlights**:
- **Generation Speed**: Fast (generated script quickly)
- **Resource Efficiency**: Low GPU usage, Mac stayed cool
- **Code Quality**: Clean, readable, functional
- **Best Open-Source Model**: Clear winner among free alternatives

**Comparison with GPT-OSS-20B**:
| Metric | Nemotron 3 Nano | GPT-OSS-20B |
|--------|-----------------|-------------|
| **Speed** | ⚡ Fast | 🐌 Very Slow |
| **GPU Usage** | ✅ Low | 🔥 High (overheated Mac) |
| **Functionality** | ✅ Works | ❌ Failed |
| **Code Quality** | ⭐⭐⭐⭐ | ⭐ |

---

### 🥉 3rd Place: Qwen3 Coder 30B (Open Source)
**Score: 6/10** | [View Script](tbw-qwen3-coder-30b.py)

```
✅ Functional (works with sudo)
✅ Retrieves SMART data
❌ Hard-coded sudo requirement
❌ No fallback mechanism
❌ Poor user experience (blocks without sudo)
❌ Less intelligent permission handling
```

**Verdict**: Works but requires significant UX improvements. Not production-ready without modifications.

---

### 🔴 4th Place: GPT-OSS-20B (Open Source)
**Score: 1/10** | [View Script](tbw-gpt-oss20b.py)

```
❌ Completely fails to detect SSDs
❌ Wrong disk detection logic (looks for 'Whole' instead of 'WholeDisk')
❌ No SSDs detected even with sudo
❌ High GPU usage during generation (overheated Mac)
❌ Slow generation time
❌ Resource inefficient
```

**Error Output**:
```
⚠️  No SSDs detected.
```

**Performance Issues**:
- **Generation time**: Very slow compared to Nemotron
- **Resource usage**: High GPU load, caused Mac to overheat
- **Efficiency**: Worst resource-to-quality ratio

**Verdict**: Complete failure. The model consumed significant resources during generation but produced non-functional code. Wrong API assumptions (uses `entry.get('Whole')` instead of checking individual disk properties with `WholeDisk`).

---

### 🔴 5th Place: Devstral Small 2 (Open Source)
**Score: 2/10** | [View Script](tbw-Devstral-Small-2.py)

```
❌ Looks for /dev/nvme0 (wrong path for macOS)
❌ Should use /dev/disk0
❌ No understanding of macOS disk architecture
❌ No auto-detection
❌ Complete failure on macOS
```

**Error Output**:
```
Error: No se encontró un dispositivo NVMe
Prueba manualmente con: sudo smartctl -a /dev/nvme0
```

**Verdict**: Fundamental misunderstanding of macOS storage. Would work better on Linux.

---

## 💡 Key Takeaways

### 🎯 Claude Sonnet 4.5 Advantages:
1. **Intelligence**: Understands macOS quirks (APFS virtual containers vs physical disks)
2. **UX Design**: Smart sudo handling, beautiful formatting
3. **Error Handling**: Handles smartctl's non-zero exit codes correctly
4. **Polish**: Production-ready code

### 🚀 Open Source (Nemotron) Wins:
1. **Functionality**: Gets all the data correctly
2. **Reliability**: Solid detection and output
3. **Efficiency**: Fast generation, low resource usage
4. **Performance**: Didn't overheat the Mac like GPT-OSS-20B
5. **Cost**: Free vs Claude's premium pricing
6. **Gap is closing**: 85% of Claude's quality at 0% of the cost

### 📈 The Open Source Reality:
**Nemotron 3 Nano proved that open-source AI can compete with premium models!**

Not all open-source models are created equal:
- ✅ **Nemotron 3 Nano**: Fast, efficient, functional (85% of Claude's quality)
- ❌ **GPT-OSS-20B**: Slow, resource-hungry, non-functional (worst performer)

The gap between paid and open-source AI is narrowing, but **model selection matters**. Quality open-source models like Nemotron offer excellent value, while others (GPT-OSS-20B) waste resources with poor results.

---

## ⚡ Performance Comparison

### Generation Speed and Efficiency

| Model | Speed | GPU Usage | Mac Temperature | Result |
|-------|-------|-----------|-----------------|--------|
| **Nemotron 3 Nano** | ⚡⚡⚡ Fast | 🟢 Low | ❄️ Cool | ✅ Functional |
| **Claude Sonnet 4.5** | ⚡⚡ Normal | 🟡 Medium | 🌡️ Normal | ✅ Perfect |
| **Qwen3 Coder 30B** | ⚡ Slow | 🟡 Medium | 🌡️ Normal | ⚠️ Works with sudo |
| **GPT-OSS-20B** | 🐌 Very Slow | 🔴 VERY HIGH | 🔥 Overheated | ❌ Failed |
| **Devstral Small 2** | ⚡ Normal | 🟢 Low | ❄️ Cool | ❌ Failed |

### 🏆 Efficiency Winner: Nemotron 3 Nano

**Why Nemotron is the best open-source model:**
1. ⚡ **Fastest** at generating functional code
2. 🟢 **Lowest resource** consumption (GPU, CPU)
3. ❄️ **Doesn't overheat** Mac during generation
4. ✅ **Code that works** (unlike GPT-OSS-20B)
5. 💰 **Free** with near-Claude performance

### ⚠️ Worst Efficiency: GPT-OSS-20B

**GPT-OSS-20B Issues:**
- 🐌 Extremely slow generation
- 🔥 High GPU usage → Mac overheated
- ❌ Output: non-functional code
- 💸 Waste of resources and time

---

## 🎮 Try It Yourself

### Claude Sonnet 4.5 (Recommended):
```bash
python3 tbw-claude-sonnet-4.5.py
```

### Nemotron 3 Nano (Great open-source alternative):
```bash
sudo python3 tbw-nemotron-3-nano.py
```

### Requirements:
```bash
# Install smartmontools
brew install smartmontools

# Python 3.7+
python3 --version
```

---

## 📸 Screenshots

<details>
<summary>Click to see Claude Sonnet 4.5 output</summary>

```
======================================================================
         SSD SMART REPORT - Complete Diagnostics
======================================================================

⚠️  Note: This script may require sudo privileges to access SMART data.
    Trying without sudo first, then with sudo if needed.

======================================================================
  DISK: /dev/disk0
======================================================================

┌────────────────────────────────────────────────────────────────────┐
│                         KEY METRICS SUMMARY                        │
├────────────────────────────────────────────────────────────────────┤
│  Critical Warning                                         0x00 (OK) │
│  Temperature                                                  28 °C │
│  Wear Level                                                      0% │
│  TBW (Data Units)                                        8022.20 TB │
│  Host Writes                                            379,822,896 │
│  Power On Hours                                 251 hours (10 days) │
│  Media Errors                                                     0 │
└────────────────────────────────────────────────────────────────────┘
```
</details>

<details>
<summary>Click to see Nemotron 3 Nano output</summary>

```
=== INFORME SMART COMPLETO ===

SMART/Health Information (NVMe Log 0x02, NSID 0xffffffff)
Critical Warning:                   0x00
Temperature:                        28 Celsius
Available Spare:                    100%
Available Spare Threshold:          99%
Percentage Used:                    0%
Data Units Read:                    40,640,061 [20.8 TB]
Data Units Written:                 16,429,485 [8.41 TB]
Host Read Commands:                 363,638,479
Host Write Commands:                379,824,113
Power Cycles:                       396
Power On Hours:                     251
Media and Data Integrity Errors:    0
```
</details>

---

## 🤝 Contributing

Found a bug or want to improve a script? PRs welcome!

---

## 📜 License

MIT License - Feel free to use, modify, and distribute.

---

## 🌟 Star This Repo!

If you found this comparison useful, please star the repo! It helps others discover this research.

---

## 🔗 Related

- [smartmontools Documentation](https://www.smartmontools.org/)
- [Nemotron 3 Nano by NVIDIA](https://build.nvidia.com/)
- [Claude by Anthropic](https://www.anthropic.com/claude)

---

<p align="center">
  <strong>Made with 🤖 by AI (and a human who tested them all)</strong>
</p>

<p align="center">
  <sub>Comparison conducted on macOS 14.6 (Sonoma) with Python 3.14 and smartmontools 7.5</sub>
</p>
