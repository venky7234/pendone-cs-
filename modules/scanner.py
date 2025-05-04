#!/usr/bin/env python3
"""
Port Scanner Module
Uses python-nmap to scan for open ports on a target IP or domain
"""

import nmap
import socket
from .utils import print_info, print_error, print_success

class PortScanner:
    """Port scanner using python-nmap"""
    
    def __init__(self):
        """Initialize the port scanner"""
        self.scanner = nmap.PortScanner()
        
    def scan(self, target, ports=None):
        """
        Scan the target for open ports
        
        Args:
            target (str): Target IP address or domain name
            ports (str, optional): Ports to scan. Default is top 1000 ports.
            
        Returns:
            dict: Dictionary with port numbers as keys and service details as values
        """
        try:
            # Resolve hostname to IP if target is a domain
            try:
                ip = socket.gethostbyname(target)
                print_info(f"Resolved {target} to {ip}")
            except socket.gaierror:
                print_error(f"Could not resolve hostname: {target}")
                return {}
            
            # Set default ports if not specified
            if not ports:
                ports = "1-1000"  # Scan top 1000 ports by default
            
            print_info(f"Scanning {target} ({ip}) for open ports ({ports})...")
            
            # Run the scan with service detection
            arguments = f"-sS -sV -T4 -p {ports}"
            self.scanner.scan(ip, arguments=arguments)
            
            # Process the results
            open_ports = {}
            
            # Check if the host was scanned successfully
            if ip in self.scanner.all_hosts():
                for proto in self.scanner[ip].all_protocols():
                    ports_dict = self.scanner[ip][proto]
                    
                    for port in ports_dict:
                        if ports_dict[port]['state'] == 'open':
                            service_info = {
                                'name': ports_dict[port].get('name', 'unknown'),
                                'product': ports_dict[port].get('product', ''),
                                'version': ports_dict[port].get('version', ''),
                                'extrainfo': ports_dict[port].get('extrainfo', ''),
                                'protocol': proto
                            }
                            
                            open_ports[port] = service_info
                            print_success(f"Found open port {port}/{proto}: {service_info['name']} ({service_info['product']} {service_info['version']})")
            
            return open_ports
            
        except nmap.PortScannerError as e:
            print_error(f"Nmap scan error: {str(e)}")
            print_error("Make sure nmap is installed and you have sufficient privileges.")
            return {}
        except Exception as e:
            print_error(f"An error occurred during port scanning: {str(e)}")
            return {}
            
    def get_scan_techniques(self):
        """Return available scan techniques for user selection"""
        techniques = {
            '1': {'name': 'SYN Scan (Stealth)', 'arg': '-sS'},
            '2': {'name': 'TCP Connect Scan', 'arg': '-sT'},
            '3': {'name': 'UDP Scan', 'arg': '-sU'},
            '4': {'name': 'Comprehensive Scan', 'arg': '-sS -sU -sV -O'},
            '5': {'name': 'Quick Scan', 'arg': '-F'}
        }
        return techniques