#!/usr/bin/env python3
#This Script For Educational Created By @amrmsdtkr2

import sys
import os
import time
import requests
import argparse
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_color(text, color):
    print(f"{color}{text}{Colors.END}")

def show_banner():
    print_color("====================================================", Colors.CYAN)
    print_color("                   CHECK BUG HOST", Colors.CYAN + Colors.BOLD)
    print_color("====================================================", Colors.CYAN)
    print()

def validate_file(input_file):
    if not os.path.isfile(input_file):
        print_color("❌ ERROR: File not found!", Colors.RED)
        return False
    
    if os.path.getsize(input_file) == 0:
        print_color("❌ ERROR: Empty file!", Colors.RED)
        return False
    
    return True

def read_domains_from_file(input_file):
    domains = []
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                domains.append(line)
        return domains
    except Exception as e:
        print_color(f"❌ Error reading file: {e}", Colors.RED)
        return []

def check_host(host, counter, timeout, verbose=False):
    counter_str = f"[{counter:2d}]"
    display_host = host
    status_str = ""
    result_type = "error"
    status_code = 000
    
    try:
        if not host.startswith(('http://', 'https://')):
            target_url = f"https://{host}"
            display_host = host
        else:
            target_url = host
            display_host = host
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Build/RKQ1.201004.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/140.0.7339.208 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        start_time = time.time()
        response = requests.head(
            target_url,
            headers=headers,
            timeout=timeout,
            allow_redirects=True,
            verify=False
        )
        response_time = time.time() - start_time
        
        status_code = response.status_code
        
        if status_code == 200:
            if verbose:
                status_str = f" {Colors.GREEN}✓ 200 OK ({response_time:.2f}s){Colors.END}"
            else:
                status_str = f" {Colors.GREEN}✓ 200 OK{Colors.END}"
            result_type = "success"
        elif status_code in [301, 302, 303, 307, 308]:
            status_str = f" {Colors.YELLOW}→ REDIRECT ({status_code}){Colors.END}"
            result_type = "redirect"
        elif status_code == 403:
            status_str = f" {Colors.RED}✗ FORBIDDEN{Colors.END}"
            result_type = "forbidden"
        elif status_code == 404:
            status_str = f" {Colors.RED}✗ NOT FOUND{Colors.END}"
            result_type = "error"
        else:
            status_str = f" {Colors.RED}✗ ERROR ({status_code}){Colors.END}"
            result_type = "error"
            
    except requests.exceptions.Timeout:
        status_str = f" {Colors.RED}✗ TIMEOUT{Colors.END}"
        result_type = "error"
    except requests.exceptions.SSLError:
        status_str = f" {Colors.RED}✗ SSL ERROR{Colors.END}"
        result_type = "error"
    except requests.exceptions.ConnectionError:
        status_str = f" {Colors.RED}✗ CONNECTION ERROR{Colors.END}"
        result_type = "error"
    except Exception as e:
        status_str = f" {Colors.RED}✗ ERROR ({str(e)[:20]}){Colors.END}"
        result_type = "error"
    
    host_str = f"{display_host:40}"
    print(f"{Colors.WHITE}{counter_str}{Colors.END} {Colors.CYAN}{host_str}{Colors.END} {status_str}")
    
    return {
        'host': display_host,
        'status_code': status_code,
        'result_type': result_type,
        'url': f"https://{host}" if not host.startswith(('http://', 'https://')) else host
    }

def get_auto_output_name(input_file, success_count):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    return f"{base_name}_success_{timestamp}.txt"

def save_successful_hosts(successful_hosts, output_file, input_file, success_count):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Results from: {input_file}\n")
            f.write(f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Total successful hosts: {success_count}\n")
            f.write("====================================================\n")
            for host in successful_hosts:
                f.write(f"https://{host}\n")
        return True
    except Exception as e:
        print_color(f"❌ Failed to save: {e}", Colors.RED)
        return False

def main():
    parser = argparse.ArgumentParser(description='Checking Bug Host')
    parser.add_argument('filename', help='File with domain list')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-t', '--timeout', type=int, default=15, help='Timeout in seconds')
    parser.add_argument('-d', '--delay', type=float, default=1.0, help='Delay Between Requests')
    parser.add_argument('-o', '--output', nargs='?', const='AUTO', help='Save results to file')
    
    args = parser.parse_args()
    
    if not validate_file(args.filename):
        sys.exit(1)
    
    domains = read_domains_from_file(args.filename)
    if not domains:
        print_color("❌ Invalid Domain!", Colors.RED)
        sys.exit(1)
    
    show_banner()
    print_color(f"Input file: {args.filename}", Colors.WHITE)
    print_color(f"Total domains: {len(domains)}", Colors.WHITE)
    print_color("=" * 52, Colors.CYAN)
    print()
    
    counters = {'total': 0, 'success': 0, 'redirect': 0, 'forbidden': 0, 'error': 0}
    successful_hosts = []
    
    print_color("Starting scan...", Colors.YELLOW)
    print()
    print_color(f"{'No.':4} {'Domain':40} Status", Colors.BOLD)
    print_color("-" * 53, Colors.CYAN)
    
    for i, host in enumerate(domains, 1):
        result = check_host(host, i, args.timeout, args.verbose)
        
        counters['total'] += 1
        if result['result_type'] == 'success':
            counters['success'] += 1
            successful_hosts.append(result['host'])
        elif result['result_type'] == 'redirect':
            counters['redirect'] += 1
        elif result['result_type'] == 'forbidden':
            counters['forbidden'] += 1
        else:
            counters['error'] += 1
        
        time.sleep(args.delay)
    
    print()
    print_color("SCAN SUMMARY", Colors.CYAN + Colors.BOLD)
    print_color("============", Colors.CYAN)
    print_color(f"Total processed: {counters['total']} domains", Colors.WHITE)
    print_color(f"Success (200 OK): {Colors.GREEN}{counters['success']}{Colors.END}", Colors.WHITE)
    print_color(f"Redirects: {Colors.YELLOW}{counters['redirect']}{Colors.END}", Colors.WHITE)
    print_color(f"Errors: {Colors.RED}{counters['error']}{Colors.END}", Colors.WHITE)
    
    if counters['total'] > 0:
        success_rate = (counters['success'] * 100) / counters['total']
        print_color(f"Success rate: {success_rate:.1f}%", Colors.WHITE)
    
    if args.output:
        if args.output == 'AUTO':
            output_file = get_auto_output_name(args.filename, counters['success'])
        else:
            output_file = args.output
        
        if successful_hosts and save_successful_hosts(successful_hosts, output_file, args.filename, counters['success']):
            print_color(f"Results saved to: {output_file}", Colors.GREEN)
    
    if successful_hosts:
        print()
        print_color("SUCCESSFUL HOSTS (200 OK):", Colors.GREEN + Colors.BOLD)
        for i, host in enumerate(successful_hosts, 1):
            print_color(f"{i:2d}. https://{host}", Colors.GREEN)

if __name__ == "__main__":
    main()