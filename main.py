#!/usr/bin/env python3
"""
PenTester: Automated Penetration Testing Framework
Main module - Handles CLI arguments and orchestrates the penetration testing process
"""

import argparse
import sys
import os
import time
from colorama import init, Fore, Style

# Import modules
from modules.scanner import PortScanner
from modules.banner_grabber import BannerGrabber
from modules.dirbuster import DirBuster
from modules.reporter import Reporter
from modules.utils import clear_screen, print_banner, print_status, print_info, print_error, print_success

# Initialize colorama
init(autoreset=True)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='PenTester - Automated Penetration Testing Framework',
        epilog='Example: python main.py --target example.com --all'
    )
    
    parser.add_argument('--target', '-t', help='Target IP address or domain')
    parser.add_argument('--scan', '-s', action='store_true', help='Perform port scanning')
    parser.add_argument('--banner', '-b', action='store_true', help='Perform banner grabbing')
    parser.add_argument('--dirbust', '-d', action='store_true', help='Perform directory brute-forcing')
    parser.add_argument('--msf', '-m', action='store_true', help='Attempt Metasploit integration')
    parser.add_argument('--all', '-a', action='store_true', help='Perform all scanning techniques')
    parser.add_argument('--output', '-o', help='Output file for the report', default='report')
    parser.add_argument('--format', '-f', help='Report format (txt or html)', default='txt')
    
    return parser.parse_args()

def interactive_menu():
    """Display interactive menu for the user"""
    clear_screen()
    print_banner()
    
    target = input(f"{Fore.CYAN}Enter target IP or domain: {Style.RESET_ALL}")
    if not target:
        print_error("Target is required. Exiting...")
        sys.exit(1)
    
    print("\n" + "="*60)
    print(f"{Fore.YELLOW}Select scanning options:{Style.RESET_ALL}")
    print("1. Port Scanning")
    print("2. Banner Grabbing")
    print("3. Directory Brute-Forcing")
    print("4. Metasploit Integration (if available)")
    print("5. All of the above")
    print("0. Exit")
    print("="*60)
    
    choice = input(f"\n{Fore.CYAN}Enter your choice (comma-separated for multiple): {Style.RESET_ALL}")
    
    if '0' in choice:
        print_info("Exiting...")
        sys.exit(0)
    
    options = {
        'target': target,
        'scan': '1' in choice or '5' in choice,
        'banner': '2' in choice or '5' in choice,
        'dirbust': '3' in choice or '5' in choice,
        'msf': '4' in choice or '5' in choice,
        'all': '5' in choice,
    }
    
    # Ask for output format
    print("\n" + "="*60)
    print(f"{Fore.YELLOW}Select report format:{Style.RESET_ALL}")
    print("1. Text (.txt)")
    print("2. HTML (.html)")
    print("="*60)
    
    format_choice = input(f"\n{Fore.CYAN}Enter your choice (default: 1): {Style.RESET_ALL}")
    options['format'] = 'html' if format_choice == '2' else 'txt'
    
    # Ask for output file
    output = input(f"\n{Fore.CYAN}Enter output filename (default: report): {Style.RESET_ALL}")
    options['output'] = output if output else 'report'
    
    return argparse.Namespace(**options)

def main():
    """Main function to run the penetration testing framework"""
    args = parse_arguments()
    
    # If no arguments provided, show interactive menu
    if len(sys.argv) == 1:
        args = interactive_menu()
    
    if not args.target:
        print_error("Target is required. Use --target or -t to specify a target.")
        sys.exit(1)
    
    # If no specific scan type is selected, prompt the user
    if not any([args.scan, args.banner, args.dirbust, args.msf, args.all]):
        print_info("No scan type selected. Running all scans...")
        args.all = True
    
    clear_screen()
    print_banner()
    print_status(f"Target: {args.target}")
    print_status(f"Output: {args.output}.{args.format}")
    print_status("Initializing...")
    
    # Create results dictionary to store all findings
    results = {
        'target': args.target,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'scan_results': {},
        'banner_results': {},
        'dirbust_results': {},
        'msf_results': {}
    }
    
    # Create reporter instance
    reporter = Reporter(args.output, args.format)
    
    # Perform port scanning
    if args.scan or args.all:
        print_status("Starting port scan...")
        scanner = PortScanner()
        try:
            scan_results = scanner.scan(args.target)
            results['scan_results'] = scan_results
            print_success(f"Port scan completed. Found {len(scan_results)} open ports.")
        except Exception as e:
            print_error(f"Port scanning failed: {str(e)}")
    
    # Perform banner grabbing (if port scan was done)
    if (args.banner or args.all) and results['scan_results']:
        print_status("Starting banner grabbing...")
        grabber = BannerGrabber()
        try:
            banner_results = grabber.grab_banners(args.target, results['scan_results'])
            results['banner_results'] = banner_results
            print_success(f"Banner grabbing completed. Found {len(banner_results)} banners.")
        except Exception as e:
            print_error(f"Banner grabbing failed: {str(e)}")
    
    # Perform directory brute forcing
    if args.dirbust or args.all:
        print_status("Starting directory brute-forcing...")
        dirbuster = DirBuster()
        try:
            http_ports = [port for port, service in results['scan_results'].items() 
                         if service.get('name', '').lower() in ('http', 'https')]
            
            # If no HTTP ports found, try common HTTP ports
            if not http_ports:
                http_ports = [80, 443, 8080, 8443]
            
            dirbust_results = dirbuster.brute_force(args.target, http_ports)
            results['dirbust_results'] = dirbust_results
            print_success(f"Directory brute-forcing completed. Found {sum(len(paths) for paths in dirbust_results.values())} paths.")
        except Exception as e:
            print_error(f"Directory brute-forcing failed: {str(e)}")
    
    # Attempt Metasploit integration if requested
    if args.msf or args.all:
        try:
            from modules.msf_integration import MetasploitIntegration
            print_status("Starting Metasploit integration...")
            msf = MetasploitIntegration()
            if msf.is_available():
                msf_results = msf.run_modules(args.target, results['scan_results'])
                results['msf_results'] = msf_results
                print_success(f"Metasploit integration completed.")
            else:
                print_error("Metasploit integration not available. Skipping...")
        except ImportError:
            print_error("Metasploit integration module not available. Skipping...")
    
    # Generate the report
    print_status("Generating report...")
    reporter.generate_report(results)
    print_success(f"Report generated: {args.output}.{args.format}")
    
    print_info("Scan completed. Thank you for using PenTester!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n" + Fore.YELLOW + "Scan interrupted by user. Exiting..." + Style.RESET_ALL)
        sys.exit(0)
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)