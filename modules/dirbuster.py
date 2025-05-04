#!/usr/bin/env python3
"""
Directory Brute-Forcing Module
Performs brute force attacks on web directories
"""

import requests
import threading
import queue
import time
import os
from urllib.parse import urljoin
from .utils import print_info, print_error, print_success, print_warning

class DirBuster:
    """Directory brute-forcing for web applications"""
    
    def __init__(self):
        """Initialize the directory brute-forcing module"""
        self.timeout = 5  # Request timeout in seconds
        self.max_threads = 10  # Maximum number of threads
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.wordlist_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "wordlists", "common.txt")
        self.extensions = ["", ".php", ".html", ".txt", ".bak", ".old", ".backup"]
        
        # Create wordlists directory if it doesn't exist
        os.makedirs(os.path.dirname(self.wordlist_path), exist_ok=True)
        
        # Create default wordlist if it doesn't exist
        if not os.path.exists(self.wordlist_path):
            self._create_default_wordlist()
    
    def brute_force(self, target, http_ports):
        """
        Perform directory brute-forcing on target web servers
        
        Args:
            target (str): Target IP address or domain name
            http_ports (list): List of HTTP ports to check
            
        Returns:
            dict: Dictionary with URLs as keys and status information as values
        """
        results = {}
        
        for port in http_ports:
            port_str = str(port)
            
            # Determine if HTTP or HTTPS based on port
            protocol = "https" if port in [443, 8443] else "http"
            base_url = f"{protocol}://{target}:{port}"
            
            try:
                # Test if the server is reachable
                test_response = requests.get(
                    base_url, 
                    timeout=self.timeout,
                    verify=False,  # Disable SSL verification
                    headers={"User-Agent": self.user_agent}
                )
                
                # Start brute forcing
                print_info(f"Starting directory brute-forcing on {base_url}...")
                paths = self._brute_force_paths(base_url)
                
                if paths:
                    results[port_str] = paths
                    print_success(f"Found {len(paths)} paths on {base_url}")
                else:
                    print_warning(f"No paths found on {base_url}")
                
            except requests.exceptions.RequestException as e:
                print_error(f"Error connecting to {base_url}: {str(e)}")
        
        return results
    
    def _brute_force_paths(self, base_url):
        """
        Brute force directories and files on the target server
        
        Args:
            base_url (str): Base URL to brute force
            
        Returns:
            dict: Dictionary with paths as keys and status information as values
        """
        paths = {}
        path_queue = queue.Queue()
        found_count = 0
        
        # Load wordlist
        try:
            with open(self.wordlist_path, 'r') as f:
                for line in f:
                    path = line.strip()
                    if path and not path.startswith('#'):
                        # Add path with different extensions
                        for ext in self.extensions:
                            path_queue.put(path + ext)
        except Exception as e:
            print_error(f"Error loading wordlist: {str(e)}")
            return paths
        
        total_paths = path_queue.qsize()
        print_info(f"Loaded {total_paths} paths to check")
        
        # Create lock for thread-safe operations
        lock = threading.Lock()
        
        # Function for worker threads
        def worker():
            nonlocal found_count
            
            while not path_queue.empty():
                path = path_queue.get()
                url = urljoin(base_url, path)
                
                try:
                    response = requests.get(
                        url, 
                        timeout=self.timeout,
                        verify=False,  # Disable SSL verification
                        headers={"User-Agent": self.user_agent},
                        allow_redirects=False  # Don't follow redirects
                    )
                    
                    status_code = response.status_code
                    
                    # Only consider successful or redirect responses
                    if status_code < 400:
                        with lock:
                            found_count += 1
                            
                            # Save information about the found path
                            paths[path] = {
                                'status_code': status_code,
                                'content_type': response.headers.get('Content-Type', ''),
                                'content_length': len(response.content),
                                'redirect_url': response.headers.get('Location', '') if 300 <= status_code < 400 else ''
                            }
                            
                            # Print progress
                            print_success(f"[{found_count}] Found: {path} (Status: {status_code})")
                
                except requests.exceptions.RequestException:
                    # Ignore connection errors for individual paths
                    pass
                
                # Mark the task as done
                path_queue.task_done()
        
        # Start worker threads
        threads = []
        for _ in range(min(self.max_threads, total_paths)):
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Display progress while waiting for threads to finish
        start_time = time.time()
        total = total_paths
        
        while path_queue.qsize() > 0:
            remaining = path_queue.qsize()
            completed = total - remaining
            elapsed = time.time() - start_time
            
            # Avoid division by zero
            if elapsed > 0:
                rate = completed / elapsed
                eta = remaining / rate if rate > 0 else 0
            else:
                rate = 0
                eta = 0
            
            print_info(f"Progress: {completed}/{total} ({int(completed/total*100)}%) - {int(rate)}/sec - ETA: {int(eta)}s", end='\r')
            time.sleep(1)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join(1)
        
        print_info("")  # Print newline after progress
        
        return paths
    
    def _create_default_wordlist(self):
        """Create a default minimal wordlist if none exists"""
        print_info("Creating default wordlist...")
        
        default_paths = [
            "index", "home", "admin", "wp-admin", "login", "wp-login", "administrator",
            "backup", "backups", "webmail", "conf", "config", "phpmyadmin", "dashboard",
            "api", "v1", "api/v1", "api/v2", "static", "uploads", "images", "img",
            "css", "js", "assets", "docs", "documentation", "blog", "wp-content",
            "includes", "include", "users", "user", "admin/login", "administrator/login",
            "install", "setup", "wp-includes", "private", "public", "src", "source",
            "test", "dev", "development", "staging", "prod", "production", "wp-json",
            "robots.txt", "sitemap.xml", ".git", ".env", ".htaccess", ".htpasswd",
            "readme", "readme.txt", "readme.md", "license", "license.txt", "CHANGELOG",
            "server-status", "server-info"
        ]
        
        try:
            with open(self.wordlist_path, 'w') as f:
                f.write("# Default wordlist for directory brute-forcing\n")
                for path in default_paths:
                    f.write(path + "\n")
            
            print_success(f"Default wordlist created at {self.wordlist_path}")
        except Exception as e:
            print_error(f"Error creating default wordlist: {str(e)}")