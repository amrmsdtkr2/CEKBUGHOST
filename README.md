<div align="center">

**CEK BUG HOST**

</div>

---

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Patform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20Windows%20%7C%20macOS-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

🚀 Features

- ✅ **Batch Host Checking** - Process multiple domains from a file
- 🎨 **Colored Terminal Output** - Easy-to-read status with colors
- 💾 **Auto-Save Results** - Timestamped output files
- ⚡ **Configurable** - Custom timeouts and delays
- 📱 **Termux Ready** - Optimized for mobile usage
- 🔒 **Safe & Clean** - No external dependencies beyond requests

---

🛠 Installation

Install required package
```bash
pip install requests
```

Termux Installation
```bash
pkg install python
pip install requests
```

Download script (or copy manually)
Then run:
```bash
python cekbughost.py domains.txt
```

---

🎯 Quick Start

1. Create target list
```bash
echo "google.com" > targets.txt
echo "github.com" >> targets.txt
```

2. Run scan
```bash
python cekbughost.py targets.txt -v -o
```

3. Check results
```bash
cat *_success_*.txt
```
---

📖 Usage

Basic Scan

```bash
python cekbughost.py domains.txt
```

Advanced Options

Verbose mode with auto-save
```bash
python cekbughost.py targets.txt -v -o
```

Custom timeout and delay
```bash
python cekbughost.py large_list.txt -t 20 -d 2
```

Save to specific file
```bash
python cekbughost.py domains.txt -o my_results.txt
```
---

⚙️ Command Options

Option Description Default
```
-h, --help Show help message -
-v, --verbose Show response times False
-t, --timeout Request timeout (seconds) 15
-d, --delay Delay between requests (seconds) 1.0
-o, --output Save results to file (auto-generate if no filename) -
```
---

📊 Output Examples

Terminal Output
```
[ 1] google.com                                 ✓ 200 OK
[ 2] github.com                                 ✓ 200 OK
[ 3] example.com                                → REDIRECT (301)
[ 4] invalid-site.com                           ✗ CONNECTION ERROR

📊 SCAN SUMMARY
Total processed: 4 domains
Success (200 OK): 2
Redirects: 1
Errors: 1
Success rate: 50.0%
```

Output File

Saved as: targets_success_20240115_143022.txt
```text
# Results from: targets.txt
# Date: 2024-01-15 14:30:22
# Total successful hosts: 2
==================================================
https://google.com
https://github.com
```

---

🎨 Status Codes
```
Status Color Description
200 OK 🟢 Green Host is responding
3xx Redirect 🟡 Yellow Host is redirecting
403/404 🔴 Red Access denied/Not found
Timeout/Error 🔴 Red Connection failed
```
---

📁 File Format

Input File
```text
# One domain per line
google.com
github.com
example.com

# Comments and empty lines are ignored
```

Generated Files
```
· *_success_*.txt - Successful hosts (200 OK)
· *_noresults_*.txt - When no hosts respond
```

---

📱 Termux Tips

Use longer timeouts on mobile
```bash
python cekbughost.py targets.txt -t 20 -d 1.5
```

Check your Python version
```bash
python --version
```

View all result files
```bash
ls -la *success*.txt
```

---

🛡️ Responsible Use

⚠️ Important: Only use on systems you own or have explicit permission to test.

Appropriate Use Cases:
```
· Authorized penetration testing
· Security research
· Educational purposes
· Bug bounty hunting (within scope)
```

---

📜 License

MIT License - See LICENSE file for details.

---

🤝 Contributing

Feel free to submit issues and pull requests!

---

<div align="center">

If this tool is useful, give it a ⭐!

</div>
