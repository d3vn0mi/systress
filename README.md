# Systress
## System Stress Test Tool

A comprehensive command-line tool for stress testing CPU, RAM, and Network resources on Linux systems. Perfect for system administrators, DevOps engineers, and anyone who needs to validate system performance under load.

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)

## 🎯 Features

- **CPU Stress Testing**: Utilizes multiple CPU cores with prime number calculations
- **RAM Stress Testing**: Allocates and actively uses memory with multi-threaded workers
- **Network Stress Testing**: Client/Server mode for bandwidth and connection testing
- **Real-time Monitoring**: Color-coded output with timestamps and progress updates
- **Zero Dependencies**: Uses only Python standard library
- **Flexible Configuration**: Customizable duration, cores, memory size, and more

## 📋 Requirements

- Python 3.6 or higher
- Linux operating system (tested on Ubuntu/Debian)
- Root/sudo access recommended for certain stress levels

## 🚀 Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourusername/stress-test-tool.git
cd stress-test-tool

# Make the script executable
chmod +x stress_test.py

# Run it!
./stress_test.py --help
```

### System-wide Installation (Optional)

```bash
# Copy to /usr/local/bin for system-wide access
sudo cp stress_test.py /usr/local/bin/stress-test
sudo chmod +x /usr/local/bin/stress-test

# Now you can run it from anywhere
stress-test cpu --duration 30
```

## 📖 Usage

### CPU Stress Test

Test your CPU cores with intensive prime number calculations:

```bash
# Use all available CPU cores for 60 seconds
./stress_test.py cpu --duration 60

# Use specific number of cores
./stress_test.py cpu --cores 4 --duration 30

# Longer stress test
./stress_test.py cpu --cores 8 --duration 300
```

**Parameters:**
- `--cores`: Number of CPU cores to use (default: all available)
- `--duration`: Test duration in seconds (default: 60)

### RAM Stress Test

Allocate and actively use system memory:

```bash
# Allocate 1GB of RAM for 60 seconds
./stress_test.py ram --size 1024 --duration 60

# Allocate 4GB with 8 threads
./stress_test.py ram --size 4096 --threads 8 --duration 120

# Heavy memory test
./stress_test.py ram --size 8192 --threads 16 --duration 300
```

**Parameters:**
- `--size`: Memory to allocate in MB (default: 1024)
- `--threads`: Number of worker threads (default: 4)
- `--duration`: Test duration in seconds (default: 60)

### Network Stress Test

Test network bandwidth and connection handling:

#### Server Mode

```bash
# Start server on default port (9999)
./stress_test.py network --mode server --duration 120

# Custom host and port
./stress_test.py network --mode server --host 0.0.0.0 --port 8888 --duration 300
```

#### Client Mode

```bash
# Connect to local server with 4 clients
./stress_test.py network --mode client --host 127.0.0.1 --port 9999 --clients 4 --duration 120

# Connect to remote server with 8 clients
./stress_test.py network --mode client --host 192.168.1.100 --port 9999 --clients 8 --duration 300
```

**Parameters:**
- `--mode`: `server` or `client` (required)
- `--host`: Host address (default: 127.0.0.1)
- `--port`: Port number (default: 9999)
- `--clients`: Number of concurrent clients (client mode only, default: 4)
- `--duration`: Test duration in seconds (default: 60)

## 💡 Use Cases

### 1. **System Performance Testing**
Validate that your server can handle expected workloads:
```bash
# Simulate high CPU load
./stress_test.py cpu --cores 16 --duration 600
```

### 2. **Memory Leak Detection**
Monitor system behavior under sustained memory pressure:
```bash
# Watch htop in another terminal while running
./stress_test.py ram --size 8192 --duration 1800
```

### 3. **Network Capacity Testing**
Test network throughput and connection limits:
```bash
# Terminal 1 (Server)
./stress_test.py network --mode server --port 9999 --duration 300

# Terminal 2 (Client)
./stress_test.py network --mode client --port 9999 --clients 16 --duration 300
```

### 4. **Load Balancer Testing**
Verify load balancer behavior under stress:
```bash
# Point multiple clients at your load balancer
./stress_test.py network --mode client --host lb.example.com --port 80 --clients 50 --duration 600
```

### 5. **Thermal Testing**
Test cooling solutions under sustained load:
```bash
# Watch temperatures with: watch -n 1 sensors
./stress_test.py cpu --duration 1800
```

## 📊 Monitoring

### Real-time Monitoring with htop

```bash
# Install htop if not already installed
sudo apt-get install htop

# Run in another terminal
htop
```

### Memory Monitoring

```bash
# Watch memory usage
watch -n 1 free -h
```

### Network Monitoring

```bash
# Monitor network connections
watch -n 1 'ss -s'

# Monitor bandwidth
sudo apt-get install iftop
sudo iftop -i eth0
```

## 🎨 Sample Output

```
============================================================
                     CPU STRESS TEST                      
============================================================

[14:23:45] Starting CPU stress test on 8 cores for 60 seconds
[14:23:45] Total CPU cores available: 8
[14:23:45] CPU Worker 0 started
[14:23:45] CPU Worker 1 started
[14:23:45] CPU Worker 2 started
...
[14:24:45] CPU Worker 0 finished - Found 12847 primes
[14:24:45] CPU Worker 1 finished - Found 12851 primes
[14:24:45] CPU stress test completed in 60.03 seconds
[14:24:45] Total primes found: 102784
```

## ⚠️ Safety Warnings

- **Start Small**: Begin with shorter durations and fewer resources
- **Monitor Temperature**: Watch CPU/GPU temperatures during stress tests
- **Save Your Work**: Close important applications before running stress tests
- **Resource Limits**: Don't allocate more RAM than physically available
- **Production Systems**: Use caution on production servers - run during maintenance windows

## 🛠️ Troubleshooting

### "MemoryError: Unable to allocate..."
You're trying to allocate more memory than available. Reduce the `--size` parameter.

### "Address already in use" (Network test)
The port is already in use. Choose a different port with `--port` or stop the conflicting service.

### Script runs but no CPU usage
Make sure you have permission to create processes. Try with `sudo` if needed.

### Permission denied
Make the script executable: `chmod +x stress_test.py`

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Ideas for Contributions
- Add disk I/O stress testing
- Add GPU stress testing
- Add JSON output format for monitoring tools
- Add web dashboard for remote monitoring
- Add Docker container support
- Add configuration file support

## 📝 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👨‍💻 Author

Created with ❤️ for the DevOps and SysAdmin community

## 🔗 Links

- Report bugs: [Issues](https://github.com/yourusername/stress-test-tool/issues)
- Request features: [Issues](https://github.com/yourusername/stress-test-tool/issues)
- Documentation: [Wiki](https://github.com/yourusername/stress-test-tool/wiki)

## ⭐ Star History

If you find this tool useful, please consider giving it a star on GitHub!

---

**Note**: This tool is intended for legitimate system testing purposes. Always ensure you have permission before stress testing any system.