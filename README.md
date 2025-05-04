# PenTester - Automated Penetration Testing Framework

PenTester is a console-based automated penetration testing framework written in Python. It automates common penetration testing tasks like port scanning, directory brute-forcing, service banner grabbing, and integrates with Metasploit where possible.

## Features

- **Port Scanning**: Uses python-nmap to scan for open TCP/UDP ports on a target IP or domain.
- **Banner Grabbing**: Connects to open ports and grabs service banners to identify potential vulnerabilities.
- **Directory Brute-Forcing**: Performs brute force attacks on web directories using a wordlist.
- **Metasploit Integration** (Optional): Interacts with Metasploit RPC to run specific modules.
- **Reporting**: Generates comprehensive reports in text or HTML format.
- **Modular Design**: Code is organized into separate modules for better maintenance and extensibility.
- **User-friendly Interface**: Features both command-line arguments and an interactive menu.

## Prerequisites

- Python 3.10+
- Nmap installed on your system (for port scanning)
- Optional: Metasploit Framework (for advanced exploitation)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/pentester.git
   cd pentester
   ```

2. Install required Python packages:
   ```
   pip install python-nmap requests colorama
   ```

3. For Metasploit integration (optional):
   ```
   pip install msgpack requests
   ```

## Usage

### Command Line Arguments

```
python main.py --target example.com --all
```

Options:
- `--target`, `-t`: Target IP address or domain name
- `--scan`, `-s`: Perform port scanning
- `--banner`, `-b`: Perform banner grabbing
- `--dirbust`, `-d`: Perform directory brute-forcing
- `--msf`, `-m`: Attempt Metasploit integration
- `--all`, `-a`: Perform all scanning techniques
- `--output`, `-o`: Output file for the report (default: report)
- `--format`, `-f`: Report format (txt or html)

### Interactive Menu

Simply run the script without arguments to access the interactive menu:

```
python main.py
```

## Example Output

```
    ____            _____         _            
   / __ \___  ____ /__  /___  ___/ /____  _____
  / /_/ / _ \/ __ \  / // _ \/ __  / __ \/ ___/
 / ____/  __/ / / / / //  __/ /_/ / /_/ / /    
/_/    \___/_/ /_/ /_/ \___/\__,_/\____/_/     
                                                
    [ Automated Penetration Testing Framework ]
    
------------------------------------------------------------
[*] Target: example.com
[*] Output: report.txt
[*] Initializing...
[*] Starting port scan...
[i] Resolved example.com to 93.184.216.34
[i] Scanning example.com (93.184.216.34) for open ports (1-1000)...
[+] Found open port 80/tcp: http (nginx )
[+] Found open port 443/tcp: https (nginx )
[+] Port scan completed. Found 2 open ports.
[*] Starting banner grabbing...
[i] Grabbing service banners from 2 open ports...
[i] Attempting to grab banner from port 80 (http)...
[+] Banner grabbed from port 80: HTTP/1.1 200 OK
Server: nginx
...
[!] Potential vulnerabilities: Server version disclosure via Server header
[i] Attempting to grab banner from port 443 (https)...
[+] Banner grabbed from port 443: HTTP/1.1 200 OK
Server: nginx
...
[!] Potential vulnerabilities: Server version disclosure via Server header
[+] Banner grabbing completed. Found 2 banners.
[*] Starting directory brute-forcing...
[i] Creating default wordlist...
[+] Default wordlist created at /home/user/pentester/wordlists/common.txt
[i] Starting directory brute-forcing on http://example.com:80...
[i] Loaded 67 paths to check
[+] [1] Found: robots.txt (Status: 200)
[+] [2] Found: index.html (Status: 200)
[i] Progress: 67/67 (100%) - 22/sec - ETA: 0s
[+] Directory brute-forcing completed. Found 2 paths.
[*] Generating report...
[+] Text report generated: /home/user/pentester/reports/report.txt
[i] Scan completed. Thank you for using PenTester!
```

## Report Format

PenTester generates comprehensive reports that include:

- Target information
- Open ports and services
- Service banners and potential vulnerabilities
- Directory brute-force results
- Metasploit module results (if available)

## Extending PenTester

PenTester is designed to be easily extensible:

1. To add a new module, create a new Python file in the `modules` directory.
2. Implement your module's functionality.
3. Update `main.py` to import and use your new module.

## Disclaimer

This tool is intended for educational purposes and authorized penetration testing only. Use responsibly and only on systems you have permission to test.

## License

This project is licensed under the MIT License - see the LICENSE file for details.