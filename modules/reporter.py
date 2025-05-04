#!/usr/bin/env python3
"""
Reporter Module
Generates reports of scan results in different formats
"""

import os
import time
import json
from datetime import datetime
from .utils import print_info, print_error, print_success

class Reporter:
    """Reporter for generating scan reports"""
    
    def __init__(self, output_file="report", output_format="txt"):
        """
        Initialize the reporter
        
        Args:
            output_file (str): Base name for the output file
            output_format (str): Output format (txt or html)
        """
        self.output_file = output_file
        self.output_format = output_format.lower()
        
        # Create reports directory if it doesn't exist
        self.reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
        os.makedirs(self.reports_dir, exist_ok=True)
        
        # Set full output path
        self.output_path = os.path.join(self.reports_dir, f"{self.output_file}.{self.output_format}")
    
    def generate_report(self, results):
        """
        Generate a report from scan results
        
        Args:
            results (dict): Dictionary containing all scan results
            
        Returns:
            bool: True if report was generated successfully, False otherwise
        """
        if self.output_format == "txt":
            return self._generate_txt_report(results)
        elif self.output_format == "html":
            return self._generate_html_report(results)
        else:
            print_error(f"Unsupported output format: {self.output_format}")
            return False
    
    def _generate_txt_report(self, results):
        """Generate a text report"""
        try:
            with open(self.output_path, 'w') as f:
                # Write header
                f.write("=" * 70 + "\n")
                f.write("PENTESTER - AUTOMATED PENETRATION TESTING REPORT\n")
                f.write("=" * 70 + "\n\n")
                
                # Write target information
                f.write("TARGET INFORMATION\n")
                f.write("-" * 70 + "\n")
                f.write(f"Target: {results['target']}\n")
                f.write(f"Scan Date: {results['timestamp']}\n")
                f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Write port scan results
                f.write("PORT SCAN RESULTS\n")
                f.write("-" * 70 + "\n")
                
                if results['scan_results']:
                    for port, service in results['scan_results'].items():
                        service_str = f"{service.get('name', 'unknown')}"
                        
                        if service.get('product'):
                            service_str += f" ({service.get('product')})"
                        
                        if service.get('version'):
                            service_str += f" {service.get('version')}"
                        
                        f.write(f"Port {port}/{service.get('protocol', 'tcp')}: {service_str}\n")
                else:
                    f.write("No open ports found.\n")
                
                f.write("\n")
                
                # Write banner grabbing results
                f.write("BANNER GRABBING RESULTS\n")
                f.write("-" * 70 + "\n")
                
                if results['banner_results']:
                    for port, banner_info in results['banner_results'].items():
                        f.write(f"Port {port} ({banner_info.get('service', 'unknown')}):\n")
                        f.write("-" * 50 + "\n")
                        f.write(f"{banner_info.get('banner', 'No banner')}\n")
                        
                        # Write potential vulnerabilities
                        if banner_info.get('potential_vulnerabilities'):
                            f.write("\nPotential Vulnerabilities:\n")
                            for vuln in banner_info['potential_vulnerabilities']:
                                f.write(f"- {vuln}\n")
                        
                        f.write("\n")
                else:
                    f.write("No banner information available.\n")
                
                f.write("\n")
                
                # Write directory brute-forcing results
                f.write("DIRECTORY BRUTE-FORCING RESULTS\n")
                f.write("-" * 70 + "\n")
                
                if results['dirbust_results']:
                    for port, paths in results['dirbust_results'].items():
                        protocol = "https" if port in ['443', '8443'] else "http"
                        f.write(f"{protocol}://{results['target']}:{port}\n")
                        f.write("-" * 50 + "\n")
                        
                        if paths:
                            for path, info in paths.items():
                                status = info.get('status_code', '')
                                content_type = info.get('content_type', '').split(';')[0]
                                size = info.get('content_length', 0)
                                
                                # Add redirect information if available
                                redirect = f" -> {info.get('redirect_url')}" if info.get('redirect_url') else ""
                                
                                f.write(f"/{path} (Status: {status}{redirect}) [Size: {size}] [{content_type}]\n")
                        else:
                            f.write("No directories/files found.\n")
                        
                        f.write("\n")
                else:
                    f.write("No directory brute-forcing results available.\n")
                
                f.write("\n")
                
                # Write Metasploit results if available
                if results['msf_results']:
                    f.write("METASPLOIT RESULTS\n")
                    f.write("-" * 70 + "\n")
                    
                    for module, module_results in results['msf_results'].items():
                        f.write(f"Module: {module}\n")
                        f.write("-" * 50 + "\n")
                        
                        if isinstance(module_results, dict):
                            for key, value in module_results.items():
                                if isinstance(value, dict):
                                    f.write(f"{key}:\n")
                                    for subkey, subvalue in value.items():
                                        f.write(f"  {subkey}: {subvalue}\n")
                                else:
                                    f.write(f"{key}: {value}\n")
                        elif isinstance(module_results, list):
                            for item in module_results:
                                f.write(f"- {item}\n")
                        else:
                            f.write(f"{module_results}\n")
                        
                        f.write("\n")
                
                # Write footer
                f.write("=" * 70 + "\n")
                f.write("END OF REPORT\n")
                f.write("=" * 70 + "\n")
            
            print_success(f"Text report generated: {self.output_path}")
            return True
        
        except Exception as e:
            print_error(f"Error generating text report: {str(e)}")
            return False
    
    def _generate_html_report(self, results):
        """Generate an HTML report"""
        try:
            with open(self.output_path, 'w') as f:
                # Write HTML header
                f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PenTester Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            border-radius: 5px 5px 0 0;
            margin-bottom: 20px;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th {
            background-color: #34495e;
            color: white;
            text-align: left;
            padding: 10px;
        }
        td {
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .port-open {
            color: #27ae60;
            font-weight: bold;
        }
        .vulnerability {
            color: #e74c3c;
            font-weight: bold;
        }
        .banner {
            font-family: monospace;
            white-space: pre-wrap;
            background-color: #f8f8f8;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            overflow-x: auto;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 0.8em;
            color: #7f8c8d;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>PenTester - Automated Penetration Testing Report</h1>
    </div>
""")
                
                # Target Information
                f.write("""
    <div class="container">
        <h2>Target Information</h2>
        <table>
            <tr>
                <th>Target</th>
                <td>{}</td>
            </tr>
            <tr>
                <th>Scan Date</th>
                <td>{}</td>
            </tr>
            <tr>
                <th>Report Generated</th>
                <td>{}</td>
            </tr>
        </table>
    </div>
""".format(results['target'], results['timestamp'], datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                
                # Port Scan Results
                f.write("""
    <div class="container">
        <h2>Port Scan Results</h2>
""")
                
                if results['scan_results']:
                    f.write("""
        <table>
            <tr>
                <th>Port</th>
                <th>Protocol</th>
                <th>Service</th>
                <th>Product</th>
                <th>Version</th>
            </tr>
""")
                    
                    for port, service in results['scan_results'].items():
                        f.write("""
            <tr>
                <td class="port-open">{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
""".format(
                            port,
                            service.get('protocol', 'tcp'),
                            service.get('name', 'unknown'),
                            service.get('product', ''),
                            service.get('version', '')
                        ))
                    
                    f.write("""
        </table>
""")
                else:
                    f.write("<p>No open ports found.</p>")
                
                f.write("</div>")
                
                # Banner Grabbing Results
                f.write("""
    <div class="container">
        <h2>Banner Grabbing Results</h2>
""")
                
                if results['banner_results']:
                    for port, banner_info in results['banner_results'].items():
                        f.write("""
        <h3>Port {} ({})</h3>
        <div class="banner">{}</div>
""".format(port, banner_info.get('service', 'unknown'), banner_info.get('banner', 'No banner').replace('<', '&lt;').replace('>', '&gt;')))
                        
                        # Write potential vulnerabilities
                        if banner_info.get('potential_vulnerabilities'):
                            f.write("<h4>Potential Vulnerabilities</h4><ul>")
                            for vuln in banner_info['potential_vulnerabilities']:
                                f.write(f'<li class="vulnerability">{vuln}</li>')
                            f.write("</ul>")
                else:
                    f.write("<p>No banner information available.</p>")
                
                f.write("</div>")
                
                # Directory Brute-Forcing Results
                f.write("""
    <div class="container">
        <h2>Directory Brute-Forcing Results</h2>
""")
                
                if results['dirbust_results']:
                    for port, paths in results['dirbust_results'].items():
                        protocol = "https" if port in ['443', '8443'] else "http"
                        f.write(f"<h3>{protocol}://{results['target']}:{port}</h3>")
                        
                        if paths:
                            f.write("""
        <table>
            <tr>
                <th>Path</th>
                <th>Status Code</th>
                <th>Size</th>
                <th>Content Type</th>
                <th>Redirect</th>
            </tr>
""")
                            
                            for path, info in paths.items():
                                status = info.get('status_code', '')
                                content_type = info.get('content_type', '').split(';')[0]
                                size = info.get('content_length', 0)
                                redirect = info.get('redirect_url', '')
                                
                                f.write("""
            <tr>
                <td>/{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
""".format(path, status, size, content_type, redirect))
                            
                            f.write("</table>")
                        else:
                            f.write("<p>No directories/files found.</p>")
                else:
                    f.write("<p>No directory brute-forcing results available.</p>")
                
                f.write("</div>")
                
                # Metasploit Results
                if results['msf_results']:
                    f.write("""
    <div class="container">
        <h2>Metasploit Results</h2>
""")
                    
                    for module, module_results in results['msf_results'].items():
                        f.write(f"<h3>Module: {module}</h3>")
                        
                        if isinstance(module_results, dict):
                            f.write("<table>")
                            for key, value in module_results.items():
                                if isinstance(value, dict):
                                    f.write(f"<tr><th colspan='2'>{key}</th></tr>")
                                    for subkey, subvalue in value.items():
                                        f.write(f"<tr><td>{subkey}</td><td>{subvalue}</td></tr>")
                                else:
                                    f.write(f"<tr><td>{key}</td><td>{value}</td></tr>")
                            f.write("</table>")
                        elif isinstance(module_results, list):
                            f.write("<ul>")
                            for item in module_results:
                                f.write(f"<li>{item}</li>")
                            f.write("</ul>")
                        else:
                            f.write(f"<p>{module_results}</p>")
                    
                    f.write("</div>")
                
                # Write HTML footer
                f.write("""
    <div class="footer">
        <p>Generated by PenTester - Automated Penetration Testing Framework</p>
    </div>
</body>
</html>
""")
            
            print_success(f"HTML report generated: {self.output_path}")
            return True
        
        except Exception as e:
            print_error(f"Error generating HTML report: {str(e)}")
            return False