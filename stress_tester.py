#!/usr/bin/env python3
"""
System Stress Test Tool
A comprehensive CLI tool for stress testing CPU, RAM, and Network
"""

import argparse
import multiprocessing
import sys
import time
import socket
import threading
from datetime import datetime
import os

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_status(text, status="info"):
    """Print status message with color"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    colors = {
        "info": Colors.OKBLUE,
        "success": Colors.OKGREEN,
        "warning": Colors.WARNING,
        "error": Colors.FAIL
    }
    color = colors.get(status, Colors.ENDC)
    print(f"[{timestamp}] {color}{text}{Colors.ENDC}")

# ============================================================================
# CPU STRESS TEST
# ============================================================================

def is_prime(n):
    """Check if number is prime (CPU intensive)"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def cpu_worker(worker_id, duration, start_time):
    """CPU worker process - calculates primes"""
    print_status(f"CPU Worker {worker_id} started", "success")
    count = 0
    num = 2
    
    while time.time() - start_time < duration:
        if is_prime(num):
            count += 1
        num += 1
    
    print_status(f"CPU Worker {worker_id} finished - Found {count} primes", "success")
    return count

def stress_cpu(cores=None, duration=60):
    """Stress test CPU cores"""
    if cores is None:
        cores = multiprocessing.cpu_count()
    
    print_header("CPU STRESS TEST")
    print_status(f"Starting CPU stress test on {cores} cores for {duration} seconds", "info")
    print_status(f"Total CPU cores available: {multiprocessing.cpu_count()}", "info")
    
    start_time = time.time()
    
    with multiprocessing.Pool(processes=cores) as pool:
        results = []
        for i in range(cores):
            result = pool.apply_async(cpu_worker, (i, duration, start_time))
            results.append(result)
        
        # Wait for all workers
        pool.close()
        pool.join()
    
    total_primes = sum(r.get() for r in results)
    elapsed = time.time() - start_time
    
    print_status(f"CPU stress test completed in {elapsed:.2f} seconds", "success")
    print_status(f"Total primes found: {total_primes}", "info")

# ============================================================================
# RAM STRESS TEST
# ============================================================================

def ram_worker(worker_id, size_mb, duration):
    """RAM worker - allocates and modifies memory"""
    print_status(f"RAM Worker {worker_id} started - Allocating {size_mb}MB", "success")
    
    # Allocate memory (list of bytes)
    chunk_size = 1024 * 1024  # 1MB chunks
    num_chunks = size_mb
    memory_blocks = []
    
    start_time = time.time()
    
    try:
        # Allocate memory
        for i in range(num_chunks):
            # Create 1MB of data
            block = bytearray(chunk_size)
            # Write data to ensure it's actually allocated
            for j in range(0, chunk_size, 4096):
                block[j] = (i + j) % 256
            memory_blocks.append(block)
            
            if (i + 1) % 100 == 0:
                print_status(f"Worker {worker_id}: Allocated {i+1}MB", "info")
        
        print_status(f"Worker {worker_id}: Successfully allocated {size_mb}MB", "success")
        
        # Keep memory allocated and perform operations
        while time.time() - start_time < duration:
            # Modify memory to prevent optimization
            for block in memory_blocks[::10]:  # Every 10th block
                block[0] = (block[0] + 1) % 256
            time.sleep(0.1)
        
        print_status(f"RAM Worker {worker_id} finished", "success")
    
    except MemoryError:
        print_status(f"Worker {worker_id}: Memory allocation failed!", "error")
    except Exception as e:
        print_status(f"Worker {worker_id}: Error - {e}", "error")

def stress_ram(size_mb=1024, duration=60, threads=4):
    """Stress test RAM"""
    print_header("RAM STRESS TEST")
    print_status(f"Starting RAM stress test: {size_mb}MB total for {duration} seconds", "info")
    print_status(f"Using {threads} threads", "info")
    
    size_per_thread = size_mb // threads
    
    workers = []
    for i in range(threads):
        worker = threading.Thread(
            target=ram_worker,
            args=(i, size_per_thread, duration)
        )
        worker.start()
        workers.append(worker)
    
    # Wait for all workers
    for worker in workers:
        worker.join()
    
    print_status("RAM stress test completed", "success")

# ============================================================================
# NETWORK STRESS TEST
# ============================================================================

def network_server(host, port, duration):
    """Network server for stress testing"""
    print_status(f"Starting network server on {host}:{port}", "info")
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    server_socket.settimeout(1.0)
    
    start_time = time.time()
    bytes_received = 0
    connections = 0
    
    print_status(f"Server listening on {host}:{port}", "success")
    
    try:
        while time.time() - start_time < duration:
            try:
                client_socket, addr = server_socket.accept()
                connections += 1
                print_status(f"Connection #{connections} from {addr}", "info")
                
                # Receive data
                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    bytes_received += len(data)
                    # Echo back
                    client_socket.sendall(data)
                
                client_socket.close()
            except socket.timeout:
                continue
            except Exception as e:
                print_status(f"Server error: {e}", "error")
    finally:
        server_socket.close()
    
    print_status(f"Server finished - {connections} connections, {bytes_received/1024/1024:.2f}MB received", "success")

def network_client(host, port, duration, worker_id):
    """Network client for stress testing"""
    print_status(f"Client Worker {worker_id} started", "success")
    
    start_time = time.time()
    bytes_sent = 0
    requests = 0
    
    data = b"X" * 1024  # 1KB per send
    
    try:
        while time.time() - start_time < duration:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(5.0)
                client_socket.connect((host, port))
                
                # Send data
                for _ in range(100):  # 100KB per connection
                    client_socket.sendall(data)
                    bytes_sent += len(data)
                    response = client_socket.recv(4096)
                
                requests += 1
                client_socket.close()
                
                if requests % 10 == 0:
                    print_status(f"Client {worker_id}: {requests} requests, {bytes_sent/1024/1024:.2f}MB sent", "info")
                
                time.sleep(0.1)
            except Exception as e:
                print_status(f"Client {worker_id} error: {e}", "error")
                time.sleep(1)
    finally:
        print_status(f"Client Worker {worker_id} finished - {requests} requests, {bytes_sent/1024/1024:.2f}MB sent", "success")

def stress_network(mode="server", host="127.0.0.1", port=9999, duration=60, clients=4):
    """Stress test network"""
    print_header("NETWORK STRESS TEST")
    
    if mode == "server":
        network_server(host, port, duration)
    elif mode == "client":
        print_status(f"Starting {clients} client workers connecting to {host}:{port}", "info")
        workers = []
        for i in range(clients):
            worker = threading.Thread(
                target=network_client,
                args=(host, port, duration, i)
            )
            worker.start()
            workers.append(worker)
            time.sleep(0.5)  # Stagger client starts
        
        for worker in workers:
            worker.join()
        
        print_status("Network stress test completed", "success")
    else:
        print_status("Invalid network mode. Use 'server' or 'client'", "error")

# ============================================================================
# MAIN CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="System Stress Test Tool - Test CPU, RAM, and Network",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # CPU stress test on all cores for 60 seconds
  %(prog)s cpu --duration 60
  
  # CPU stress test on 4 cores for 30 seconds
  %(prog)s cpu --cores 4 --duration 30
  
  # RAM stress test - allocate 2GB for 60 seconds
  %(prog)s ram --size 2048 --duration 60
  
  # Network server stress test
  %(prog)s network --mode server --port 9999 --duration 120
  
  # Network client stress test (run in another terminal)
  %(prog)s network --mode client --host 127.0.0.1 --port 9999 --clients 8 --duration 120
        """
    )
    
    subparsers = parser.add_subparsers(dest='test_type', help='Type of stress test')
    
    # CPU stress test
    cpu_parser = subparsers.add_parser('cpu', help='CPU stress test')
    cpu_parser.add_argument('--cores', type=int, default=None,
                           help='Number of CPU cores to use (default: all)')
    cpu_parser.add_argument('--duration', type=int, default=60,
                           help='Duration in seconds (default: 60)')
    
    # RAM stress test
    ram_parser = subparsers.add_parser('ram', help='RAM stress test')
    ram_parser.add_argument('--size', type=int, default=1024,
                           help='Memory to allocate in MB (default: 1024)')
    ram_parser.add_argument('--duration', type=int, default=60,
                           help='Duration in seconds (default: 60)')
    ram_parser.add_argument('--threads', type=int, default=4,
                           help='Number of threads (default: 4)')
    
    # Network stress test
    net_parser = subparsers.add_parser('network', help='Network stress test')
    net_parser.add_argument('--mode', choices=['server', 'client'], required=True,
                           help='Server or client mode')
    net_parser.add_argument('--host', default='127.0.0.1',
                           help='Host address (default: 127.0.0.1)')
    net_parser.add_argument('--port', type=int, default=9999,
                           help='Port number (default: 9999)')
    net_parser.add_argument('--duration', type=int, default=60,
                           help='Duration in seconds (default: 60)')
    net_parser.add_argument('--clients', type=int, default=4,
                           help='Number of client workers (client mode only, default: 4)')
    
    args = parser.parse_args()
    
    if not args.test_type:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.test_type == 'cpu':
            stress_cpu(cores=args.cores, duration=args.duration)
        elif args.test_type == 'ram':
            stress_ram(size_mb=args.size, duration=args.duration, threads=args.threads)
        elif args.test_type == 'network':
            stress_network(
                mode=args.mode,
                host=args.host,
                port=args.port,
                duration=args.duration,
                clients=args.clients
            )
    except KeyboardInterrupt:
        print_status("\n\nTest interrupted by user", "warning")
        sys.exit(0)
    except Exception as e:
        print_status(f"Error: {e}", "error")
        sys.exit(1)

if __name__ == "__main__":
    main()