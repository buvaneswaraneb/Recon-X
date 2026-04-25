
# 🔍 RECON-X

**A Lightweight Linux Reconnaissance Toolkit (CLI-based)**

---

## 📌 Overview

**RECON-X** is a Python-based reconnaissance toolkit designed for performing basic network and OSINT tasks from the command line.

It provides a simple, menu-driven interface for quickly gathering information such as IP details, domain resolution, open ports, system info, and more.

---

## ✨ Features

* 🌐 IP Lookup (Geo + ISP info)
* 🔎 Domain & DNS Lookup
* 🚪 Basic Port Scanning (common ports)
* 📡 Ping Test
* 🧠 OSINT Username Search (social links)
* 🖥️ System Information Viewer
* 📥 HTTP Header Grabber
* 🔐 SSL Certificate Checker
* 🌍 Subdomain Finder (common prefixes)
* 📁 Directory Reader

---

## ⚙️ Installation

### 🔹 Method 1: Clone & Install (Recommended)

```bash
git clone https://github.com/yourname/reconx.git
cd reconx
pip install .
```

Run:

```bash
reconx
```

---

### 🔹 Method 2: Run Without Installing

```bash
git clone https://github.com/yourname/reconx.git
cd reconx
python reconx/main.py
```

---

## 📦 Requirements

* Python 3.8+
* `requests`

Install manually:

```bash
pip install -r requirements.txt
```

---

## 🧪 Usage

After installation:

```bash
reconx
```

You’ll see an interactive menu:

```
1  - IP Lookup
2  - Domain Lookup
3  - Port Scan
4  - DNS Lookup
5  - OSINT Search
6  - System Info
7  - Ping Test
8  - Header Grabber
9  - SSL Checker
10 - Subdomain Finder
11 - Username Search
12 - Directory Reader
13 - Exit
```

---

## 📁 Project Structure

```
reconx/
├── reconx/
│   ├── __init__.py
│   └── main.py
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md
```

---

## 🛠️ Development Setup

```bash
git clone https://github.com/yourname/reconx.git
cd reconx
pip install -e .
```

---

## 🧹 Uninstall

If installed via pip:

```bash
pip uninstall reconx
```

---

## ⚠️ Disclaimer

This tool is intended for **educational and ethical use only**.

* Do NOT use it on networks/systems without permission
* The author is not responsible for misuse

---

## 🚀 Roadmap (Future Improvements)

* [ ] Multi-threaded port scanning
* [ ] CLI arguments support (non-interactive mode)
* [ ] Advanced subdomain enumeration
* [ ] Output export (JSON / TXT)
* [ ] Proxy & stealth features
* [ ] API integrations for OSINT

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Commit your changes
4. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 💡 Author

**ADITHYAN KS**
Cybersecurity Student | Developer

---

## ⭐ Support

If you like this project:

* ⭐ Star the repository
* 🛠️ Suggest improvements
* 🐛 Report issues

---
