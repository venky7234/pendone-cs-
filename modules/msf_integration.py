#!/usr/bin/env python3
"""
Metasploit Integration Module
Integrates with Metasploit Framework for advanced exploitation
"""

import json
import time
import socket
import subprocess
from .utils import print_info, print_error, print_success, print_warning

class MetasploitIntegration:
    """Metasploit integration for exploitation"""
    
    def __init__(self, msfrpc_host="127.0.0.1", msfrpc_port=55553, msfrpc_user="msf", msfrpc_pass="msf"):
        """
        Initialize the Metasploit integration
        
        Args:
            msfrpc_host (str): MSFRPC host address
            msfrpc_port (int): MSFRPC port
            msfrpc_user (str): MSFRPC username
            msfrpc_pass (str): MSFRPC password
        """
        self.msfrpc_host = msfrpc_host
        self.msfrpc_port = msfrpc_port
        self.msfrpc_user = msfrpc_user
        self.msfrpc_pass = msfrpc_pass
        self.connected = False
        self.token = None
        
        # Service-to-module mapping for common vulnerabilities
        self.module_mapping = {
            'ftp': [
                'auxiliary/scanner/ftp/anonymous',
                'auxiliary/scanner/ftp/ftp_version'
            ],
            'ssh': [
                'auxiliary/scanner/ssh/ssh_version',
                'auxiliary/scanner/ssh/ssh_enumusers'
            ],
            'http': [
                'auxiliary/scanner/http/http_version',
                'auxiliary/scanner/http/dir_scanner',
                'auxiliary/scanner/http/robots_txt'
            ],
            'https': [
                'auxiliary/scanner/http/http_version',
                'auxiliary/scanner/http/ssl',
                'auxiliary/scanner/http/ssl_version'
            ],
            'smb': [
                'auxiliary/scanner/smb/smb_version',
                'auxiliary/scanner/smb/smb_enumshares'
            ],
            'mysql': [
                'auxiliary/scanner/mysql/mysql_version',
                'auxiliary/scanner/mysql/mysql_login'
            ],
            'mssql': [
                'auxiliary/scanner/mssql/mssql_ping',
                'auxiliary/scanner/mssql/mssql_login'
            ],
            'smtp': [
                'auxiliary/scanner/smtp/smtp_version',
                'auxiliary/scanner/smtp/smtp_enum'
            ],
            'telnet': [
                'auxiliary/scanner/telnet/telnet_version',
                'auxiliary/scanner/telnet/telnet_login'
            ]
        }
    
    def is_available(self):
        """
        Check if Metasploit is available
        
        Returns:
            bool: True if Metasploit is available, False otherwise
        """
        try:
            # Try to connect to MSFRPC
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            result = s.connect_ex((self.msfrpc_host, self.msfrpc_port))
            s.close()
            
            if result == 0:
                # Port is open, try to authenticate
                return self._authenticate()
            else:
                # Try to start msfrpcd
                print_info("MSFRPC not running. Attempting to start it...")
                try:
                    # Try to start msfrpcd using subprocess
                    subprocess.Popen(
                        ["msfrpcd", "-U", self.msfrpc_user, "-P", self.msfrpc_pass, "-a", self.msfrpc_host, "-p", str(self.msfrpc_port)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    
                    # Wait for the service to start
                    print_info("Waiting for MSFRPC to start...")
                    time.sleep(5)
                    
                    # Try to connect again
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(3)
                    result = s.connect_ex((self.msfrpc_host, self.msfrpc_port))
                    s.close()
                    
                    if result == 0:
                        return self._authenticate()
                    else:
                        print_error("Failed to start MSFRPC.")
                        return False
                except:
                    print_error("Failed to start MSFRPC. Please start it manually.")
                    print_info("Run: msfrpcd -U msf -P msf -a 127.0.0.1 -p 55553")
                    return False
        except:
            return False
    
    def _authenticate(self):
        """
        Authenticate with MSFRPC
        
        Returns:
            bool: True if authentication was successful, False otherwise
        """
        try:
            import msgpack
            import requests
            
            # Create the authentication request
            auth_request = {
                'method': 'auth.login',
                'params': [self.msfrpc_user, self.msfrpc_pass],
                'id': 1
            }
            
            # Send the request
            response = requests.post(
                f"http://{self.msfrpc_host}:{self.msfrpc_port}/api/1.0/",
                data=msgpack.packb(auth_request),
                headers={'Content-Type': 'binary/message-pack'}
            )
            
            # Parse the response
            if response.status_code == 200:
                resp_data = msgpack.unpackb(response.content)
                if 'result' in resp_data and 'token' in resp_data['result']:
                    self.token = resp_data['result']['token']
                    self.connected = True
                    print_success("Successfully authenticated with MSFRPC")
                    return True
            
            print_error("Authentication with MSFRPC failed")
            return False
        except ImportError:
            print_error("Required libraries (msgpack and requests) not installed")
            print_info("To use Metasploit integration, install: pip install msgpack requests")
            return False
        except Exception as e:
            print_error(f"Error authenticating with MSFRPC: {str(e)}")
            return False
    
    def run_modules(self, target, scan_results):
        """
        Run Metasploit modules against the target
        
        Args:
            target (str): Target IP address or domain name
            scan_results (dict): Dictionary of open ports from port scanner
            
        Returns:
            dict: Dictionary with module names as keys and results as values
        """
        if not self.connected:
            if not self.is_available():
                return {"error": "Metasploit not available"}
        
        results = {}
        
        try:
            import msgpack
            import requests
            
            # Determine which modules to run based on detected services
            modules_to_run = {}
            
            for port, service_info in scan_results.items():
                service_name = service_info.get('name', '').lower()
                
                # Check if we have modules for this service
                if service_name in self.module_mapping:
                    for module in self.module_mapping[service_name]:
                        # Store the module with the port to run it against
                        if module not in modules_to_run:
                            modules_to_run[module] = []
                        modules_to_run[module].append(port)
            
            # Run each module
            for module, ports in modules_to_run.items():
                print_info(f"Running Metasploit module: {module}")
                
                for port in ports:
                    port = int(port)
                    
                    # Get module options
                    opts_request = {
                        'method': 'module.options',
                        'params': [self.token, 'auxiliary', module],
                        'id': 1
                    }
                    
                    response = requests.post(
                        f"http://{self.msfrpc_host}:{self.msfrpc_port}/api/1.0/",
                        data=msgpack.packb(opts_request),
                        headers={'Content-Type': 'binary/message-pack'}
                    )
                    
                    # Set up module options
                    options = {
                        'RHOSTS': target,
                        'RPORT': port
                    }
                    
                    # Execute the module
                    exec_request = {
                        'method': 'module.execute',
                        'params': [self.token, 'auxiliary', module, options],
                        'id': 1
                    }
                    
                    response = requests.post(
                        f"http://{self.msfrpc_host}:{self.msfrpc_port}/api/1.0/",
                        data=msgpack.packb(exec_request),
                        headers={'Content-Type': 'binary/message-pack'}
                    )
                    
                    # Parse the response
                    if response.status_code == 200:
                        resp_data = msgpack.unpackb(response.content)
                        
                        if 'result' in resp_data and 'job_id' in resp_data['result']:
                            job_id = resp_data['result']['job_id']
                            print_success(f"Module {module} running as job {job_id}")
                            
                            # Wait for the job to complete
                            time.sleep(5)
                            
                            # Get job results
                            job_key = f"{module}:{port}"
                            results[job_key] = f"Job ID: {job_id} (Results not available)"
                        else:
                            print_error(f"Failed to execute module {module}")
                    else:
                        print_error(f"Error executing module {module}")
            
            return results
            
        except ImportError:
            print_error("Required libraries (msgpack and requests) not installed")
            return {"error": "Required libraries not installed"}
        except Exception as e:
            print_error(f"Error running Metasploit modules: {str(e)}")
            return {"error": str(e)}