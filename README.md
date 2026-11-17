# 🔍 Port Scanner

A Python-based Port Scanner with a modern pastel-themed web dashboard, designed for educational cybersecurity and network security testing.

## 📌 About the Project

Port Scanner is a web-based network scanning application developed using Python and Flask. It scans a specified range of TCP ports on an IPv4 target and identifies open and closed ports.

The application provides live scanning progress, service identification, downloadable scan reports, and scan history through a user-friendly dashboard.

## ✨ Features

- TCP port scanning
- Multithreaded scanning for improved performance
- Service identification for commonly used ports
- Live scan progress tracking
- Open and closed port detection
- IPv4 address validation
- Port range validation
- Maximum 1,000 ports per scan
- Downloadable scan reports
- Scan history management
- Pastel-themed responsive web dashboard

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| HTML5 | Webpage structure |
| CSS3 | Dashboard styling |
| JavaScript | Frontend interactions |
| Socket | TCP port connections |
| SQLite | Not currently required |

## 📂 Project Structure

```text
Port-Scanner/
│
├── app.py
├── main.py
├── scanner.py
├── services.py
├── results.py
├── gui.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── scans/
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Port-Scanner.git
```

### 2. Navigate to the Project Folder

```bash
cd Port-Scanner
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

### 5. Open in Browser

```text
http://127.0.0.1:5000
```

## 🚀 How to Use

1. Open the Port Scanner website.
2. Enter the target IPv4 address.
3. Specify the starting and ending port numbers.
4. Confirm that you have authorization to scan the target.
5. Click Start Scanning.
6. View live scanning progress and results.
7. Download the generated scan report.
8. Access previous scans through Scan History.

## 🔐 Security and Ethical Usage

This project is developed strictly for educational and authorized security testing.

Only scan systems, networks, and devices that you own or have explicit permission to test.

Unauthorized port scanning may violate applicable laws or organizational policies.

## 👩‍💻 Developer

**Mridhula A**  
B.Sc. Computer Science with Cyber Security

## 📜 Disclaimer

This tool is intended for educational and authorized cybersecurity testing purposes only.
