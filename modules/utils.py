#!/usr/bin/env python3
"""
Utility functions for the PenTester framework
"""

import os
import sys
import platform
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def print_banner():
    """Print the application banner"""
    banner = r"""
    ____            _____         _            
   / __ \___  ____ /__  /___  ___/ /____  _____
  / /_/ / _ \/ __ \  / // _ \/ __  / __ \/ ___/
 / ____/  __/ / / / / //  __/ /_/ / /_/ / /    
/_/    \___/_/ /_/ /_/ \___/\__,_/\____/_/     
                                                
    [ Automated Penetration Testing Framework ]
    """
    
    print(Fore.CYAN + banner)
    print(f"{Fore.YELLOW}Version: 1.0.0{Style.RESET_ALL}")
    print("-" * 60)

def print_status(message, end='\n'):
    """Print a status message"""
    print(f"{Fore.BLUE}[*] {message}{Style.RESET_ALL}", end=end)

def print_info(message, end='\n'):
    """Print an information message"""
    print(f"{Fore.WHITE}[i] {message}{Style.RESET_ALL}", end=end)

def print_success(message, end='\n'):
    """Print a success message"""
    print(f"{Fore.GREEN}[+] {message}{Style.RESET_ALL}", end=end)

def print_warning(message, end='\n'):
    """Print a warning message"""
    print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}", end=end)

def print_error(message, end='\n'):
    """Print an error message"""
    print(f"{Fore.RED}[-] {message}{Style.RESET_ALL}", end=end)

def print_critical(message, end='\n'):
    """Print a critical error message"""
    print(f"{Back.RED}{Fore.WHITE}[!] {message}{Style.RESET_ALL}", end=end)

def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(f"{Fore.CYAN}{title}{Style.RESET_ALL}")
    print("=" * 60)

def progress_bar(iteration, total, prefix='', suffix='', length=50, fill='█'):
    """
    Call in a loop to create a progress bar in the terminal
    
    Args:
        iteration (int): Current iteration
        total (int): Total iterations
        prefix (str): Prefix string
        suffix (str): Suffix string
        length (int): Character length of bar
        fill (str): Bar fill character
    """
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    
    # Print new line on completion
    if iteration == total:
        print()

def yes_no_prompt(question, default="yes"):
    """
    Ask a yes/no question and return the answer.
    
    Args:
        question (str): Question to ask
        default (str): Default answer if user just presses Enter
        
    Returns:
        bool: True for yes, False for no
    """
    valid = {"yes": True, "y": True, "no": False, "n": False}
    
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError(f"Invalid default answer: '{default}'")
    
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' ('y' or 'n').\n")