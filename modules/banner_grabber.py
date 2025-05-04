#!/usr/bin/env python3
"""
Banner Grabber Module
Connects to open ports and grabs service banners
"""

import socket
import ssl
import telnetlib
import time
from .utils import print_info, print_error, print_success, print_warning

class BannerGrabber:
    """Banner grabber for service identification"""
    
    def __init__(self):
        """Initialize the banner grabber"""
        self.timeout = 5  # Connection timeout in seconds
        
        # Common service probes - first line to send for each service
        self.service_probes = {
            'http': b'GET / HTTP/1.1\r\nHost: {}\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\n\r\n',
            'https': b'GET / HTTP/1.1\r\nHost: {}\r\nUser-Agent: Mozilla/5.0\r\nAccept: */*\r\n\r\n',
            'ftp': b'',  # FTP servers send banner on connect
            'ssh': b'',  # SSH servers send banner on connect
            'smtp': b'EHLO pentester.local\r\n',
            'pop3': b'',  # POP3 servers send banner on connect
            'imap': b'A001 CAPABILITY\r\n',
            'telnet': b'',  # Telnet servers send banner on connect
            'mysql': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        }
        
        # Common vulnerability signatures in banners
        self.vulnerability_signatures = {
            'apache': {
                '2.2.': 'Apache 2.2.x - Multiple vulnerabilities',
                '2.4.': 'Check for specific version vulnerabilities',
            },
            'nginx': {
                '1.': 'Check for specific version vulnerabilities',
            },
            'openssh': {
                '5.': 'OpenSSH 5.x - Multiple vulnerabilities',
                '6.': 'Check for specific version vulnerabilities',
            },
            'microsoft-iis': {
                '6.0': 'IIS 6.0 - Multiple vulnerabilities',
                '7.0': 'IIS 7.0 - Check for specific patches',
            },
            'proftpd': {
                '1.3.3': 'ProFTPD 1.3.3 - Multiple vulnerabilities',
            },
            'vsftpd': {
                '2.': 'Check for specific version vulnerabilities',
            },
        }
    
    def grab_banners(self, target, open_ports):
        """
        Grab banners from open ports
        
        Args:
            target (str): Target IP address or domain name
            open_ports (dict): Dictionary of open ports from port scanner
            
        Returns:
            dict: Dictionary with port numbers as keys and banner information as values
        """
        banners = {}
        
        print_info(f"Grabbing service banners from {len(open_ports)} open ports...")
        
        for port, service_info in open_ports.items():
            port = int(port)
            service_name = service_info.get('name', '').lower()
            
            print_info(f"Attempting to grab banner from port {port} ({service_name})...")
            
            try:
                # Handle HTTPS connections
                if service_name == 'https' or (service_name == 'http' and port == 443):
                    banner = self._grab_https_banner(target, port)
                    
                # Handle HTTP connections
                elif service_name == 'http':
                    banner = self._grab_http_banner(target, port)
                
                # Handle FTP connections
                elif service_name == 'ftp':
                    banner = self._grab_ftp_banner(target, port)
                
                # Handle SSH connections
                elif service_name == 'ssh':
                    banner = self._grab_ssh_banner(target, port)
                
                # Handle SMTP connections
                elif service_name == 'smtp':
                    banner = self._grab_smtp_banner(target, port)
                
                # Handle other services using generic connection
                else:
                    banner = self._grab_generic_banner(target, port, service_name)
                
                if banner:
                    # Analyze banner for potential vulnerabilities
                    vulnerabilities = self._analyze_banner(banner, service_name, service_info)
                    
                    banners[port] = {
                        'service': service_name,
                        'banner': banner,
                        'potential_vulnerabilities': vulnerabilities
                    }
                    
                    print_success(f"Banner grabbed from port {port}: {banner[:100]}...")
                    if vulnerabilities:
                        print_warning(f"Potential vulnerabilities: {', '.join(vulnerabilities)}")
                else:
                    print_error(f"Failed to grab banner from port {port}")
                
            except Exception as e:
                print_error(f"Error grabbing banner from port {port}: {str(e)}")
        
        return banners
    
    def _grab_http_banner(self, target, port):
        """Grab banner from HTTP service"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((target, port))
            
            # Send HTTP request
            request = self.service_probes['http'].format(target.encode())
            s.send(request)
            
            # Receive response
            response = b""
            s.settimeout(2)
            
            try:
                while True:
                    data = s.recv(4096)
                    if not data:
                        break
                    response += data
            except socket.timeout:
                pass
            
            s.close()
            return response.decode('utf-8', errors='ignore')
        except Exception as e:
            print_error(f"HTTP connection error: {str(e)}")
            return None
    
    def _grab_https_banner(self, target, port):
        """Grab banner from HTTPS service"""
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((target, port))
            
            # Wrap socket with SSL
            ssl_sock = context.wrap_socket(s, server_hostname=target)
            
            # Send HTTP request
            request = self.service_probes['https'].format(target.encode())
            ssl_sock.send(request)
            
            # Receive response
            response = b""
            ssl_sock.settimeout(2)
            
            try:
                while True:
                    data = ssl_sock.recv(4096)
                    if not data:
                        break
                    response += data
            except socket.timeout:
                pass
            
            # Get certificate information
            cert = ssl_sock.getpeercert(binary_form=True)
            if cert:
                cert_info = f"SSL Certificate present"
            else:
                cert_info = "No SSL Certificate"
            
            ssl_sock.close()
            
            resp_text = response.decode('utf-8', errors='ignore')
            return f"{resp_text}\n{cert_info}"
        except Exception as e:
            print_error(f"HTTPS connection error: {str(e)}")
            return None
    
    def _grab_ftp_banner(self, target, port):
        """Grab banner from FTP service"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((target, port))
            
            # FTP servers send banner upon connection
            banner = s.recv(1024)
            
            # Try anonymous login to check if allowed
            s.send(b"USER anonymous\r\n")
            response = s.recv(1024)
            s.send(b"PASS anonymous@pentester.local\r\n")
            response = s.recv(1024)
            
            anonymous_check = b"230" in response  # 230 means successful login
            
            s.close()
            
            banner_text = banner.decode('utf-8', errors='ignore')
            if anonymous_check:
                banner_text += "\nWARNING: Anonymous FTP access is allowed!"
            
            return banner_text
        except Exception as e:
            print_error(f"FTP connection error: {str(e)}")
            return None
    
    def _grab_ssh_banner(self, target, port):
        """Grab banner from SSH service"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((target, port))
            
            # SSH servers send banner upon connection
            banner = s.recv(1024)
            s.close()
            
            return banner.decode('utf-8', errors='ignore')
        except Exception as e:
            print_error(f"SSH connection error: {str(e)}")
            return None
    
    def _grab_smtp_banner(self, target, port):
        """Grab banner from SMTP service"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((target, port))
            
            # Get initial banner
            banner = s.recv(1024)
            
            # Send EHLO command
            s.send(self.service_probes['smtp'].format(target.encode()))
            response = s.recv(1024)
            
            s.close()
            
            full_response = banner + b"\n" + response
            return full_response.decode('utf-8', errors='ignore')
        except Exception as e:
            print_error(f"SMTP connection error: {str(e)}")
            return None
    
    def _grab_generic_banner(self, target, port, service_name):
        """Grab banner using generic method for unknown services"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            s.connect((target, port))
            
            # Some services send banner upon connection
            banner = b""
            s.settimeout(2)
            
            try:
                banner = s.recv(1024)
            except socket.timeout:
                # If no banner received, try sending a probe
                if service_name in self.service_probes:
                    s.send(self.service_probes[service_name].format(target.encode()))
                    time.sleep(1)
                    try:
                        banner = s.recv(1024)
                    except socket.timeout:
                        pass
            
            s.close()
            
            if banner:
                return banner.decode('utf-8', errors='ignore')
            return f"No banner received for service {service_name} on port {port}"
        except Exception as e:
            print_error(f"Generic connection error on port {port}: {str(e)}")
            return None
    
    def _analyze_banner(self, banner, service_name, service_info):
        """
        Analyze banner for potential vulnerabilities
        
        Args:
            banner (str): Service banner
            service_name (str): Service name
            service_info (dict): Service information from port scanner
            
        Returns:
            list: List of potential vulnerability descriptions
        """
        vulnerabilities = []
        
        # Check for vulnerability signatures based on service and version
        product = service_info.get('product', '').lower()
        version = service_info.get('version', '')
        
        # Check common product vulnerabilities
        for prod, versions in self.vulnerability_signatures.items():
            if prod in product or prod in service_name:
                for ver_prefix, vuln_desc in versions.items():
                    if version.startswith(ver_prefix):
                        vulnerabilities.append(vuln_desc)
        
        # Check for specific keywords in the banner
        keywords = {
            'default password': 'Default password may be in use',
            'debug': 'Debug mode may be enabled',
            'test': 'Test/development configuration may be in use',
            'admin': 'Administrative interface may be exposed'
        }
        
        for keyword, desc in keywords.items():
            if keyword in banner.lower():
                vulnerabilities.append(desc)
        
        # Check for anonymous FTP access
        if service_name == 'ftp' and 'anonymous ftp access is allowed' in banner.lower():
            vulnerabilities.append('Anonymous FTP access is allowed')
        
        # Check for specific HTTP server issues
        if service_name == 'http' or service_name == 'https':
            if 'X-Powered-By:' in banner:
                vulnerabilities.append('Technology disclosure via X-Powered-By header')
            
            if 'Server:' in banner:
                vulnerabilities.append('Server version disclosure via Server header')
        
        return vulnerabilities