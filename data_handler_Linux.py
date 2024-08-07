import platform
import psutil
import socket
import os
import subprocess
import datetime

# Collect system information
def collect_system_info():
    info = {}

    # System details
    info['System'] = platform.system()
    info['Node Name'] = platform.node()
    info['Release'] = platform.release()
    info['Version'] = platform.version()
    info['Machine'] = platform.machine()
    info['Processor'] = platform.processor()

    # CPU details
    info['CPU Cores'] = psutil.cpu_count(logical=False)
    info['Logical CPUs'] = psutil.cpu_count(logical=True)
    info['CPU Frequency'] = psutil.cpu_freq().current

    # Memory details
    mem = psutil.virtual_memory()
    info['Total Memory'] = mem.total
    info['Available Memory'] = mem.available
    info['Used Memory'] = mem.used

    # Disk usage
    disk = psutil.disk_usage('/')
    info['Total Disk Space'] = disk.total
    info['Used Disk Space'] = disk.used
    info['Free Disk Space'] = disk.free

    # Network information
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    info['Hostname'] = hostname
    info['IP Address'] = ip_address

    return info

# Collect user information
def collect_user_info():
    user_info = {}
    user_info['User'] = os.getlogin()
    user_info['UID'] = os.getuid()
    user_info['GID'] = os.getgid()
    user_info['Home Directory'] = os.path.expanduser("~")
    user_info['Current Directory'] = os.getcwd()
    return user_info

# Collect process information
def collect_process_info():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        processes.append(proc.info)
    return processes

# Collect Python environment information
def collect_python_info():
    python_info = {}
    python_info['Python Version'] = platform.python_version()
    python_info['Python Build'] = platform.python_build()
    python_info['Python Compiler'] = platform.python_compiler()
    python_info['Python Implementation'] = platform.python_implementation()
    return python_info

# Collect disk usage by mount point
def collect_disk_usage():
    disk_usage = {}
    partitions = psutil.disk_partitions()
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_usage[partition.mountpoint] = {
            'Total': usage.total,
            'Used': usage.used,
            'Free': usage.free,
            'Percent Used': usage.percent
        }
    return disk_usage

# Collect network interface details
def collect_network_interfaces():
    interfaces = psutil.net_if_addrs()
    network_info = {}
    for interface, addrs in interfaces.items():
        network_info[interface] = []
        for addr in addrs:
            network_info[interface].append({
                'Family': str(addr.family),
                'Address': addr.address,
                'Netmask': addr.netmask,
                'Broadcast': addr.broadcast
            })
    return network_info

# Collect system uptime
def collect_system_uptime():
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    now = datetime.datetime.now()
    uptime = now - boot_time
    return {
        'Boot Time': boot_time.strftime("%Y-%m-%d %H:%M:%S"),
        'Uptime': str(uptime)
    }

# Collect CPU utilization
def collect_cpu_utilization():
    cpu_usage = {}
    cpu_usage['Current CPU Usage'] = psutil.cpu_percent(interval=1)
    cpu_usage['CPU Usage per Core'] = psutil.cpu_percent(interval=1, percpu=True)
    return cpu_usage

# Collect memory utilization
def collect_memory_utilization():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        'Memory Utilization': {
            'Total': mem.total,
            'Available': mem.available,
            'Used': mem.used,
            'Percent Used': mem.percent
        },
        'Swap Utilization': {
            'Total': swap.total,
            'Free': swap.free,
            'Used': swap.used,
            'Percent Used': swap.percent
        }
    }

# Collect system load averages
def collect_load_averages():
    return {
        '1 Minute Load Average': os.getloadavg()[0],
        '5 Minute Load Average': os.getloadavg()[1],
        '15 Minute Load Average': os.getloadavg()[2]
    }

# Save collected information to a file
def save_info_to_file(info, filename='system_info.txt'):
    with open(filename, 'w') as file:
        for key, value in info.items():
            if isinstance(value, dict):
                file.write(f"{key}:\n")
                for sub_key, sub_value in value.items():
                    file.write(f"  {sub_key}: {sub_value}\n")
            else:
                file.write(f"{key}: {value}\n")
            file.write('\n')

# Main function to execute all information collection
def main():
    print("Collecting system information...")
    
    system_info = collect_system_info()
    user_info = collect_user_info()
    process_info = collect_process_info()
    python_info = collect_python_info()
    disk_usage = collect_disk_usage()
    network_interfaces = collect_network_interfaces()
    system_uptime = collect_system_uptime()
    cpu_utilization = collect_cpu_utilization()
    memory_utilization = collect_memory_utilization()
    load_averages = collect_load_averages()

    all_info = {
        'System Information': system_info,
        'User Information': user_info,
        'Process Information': process_info,
        'Python Environment Information': python_info,
        'Disk Usage by Mount Point': disk_usage,
        'Network Interfaces': network_interfaces,
        'System Uptime': system_uptime,
        'CPU Utilization': cpu_utilization,
        'Memory Utilization': memory_utilization,
        'Load Averages': load_averages
    }
    
    save_info_to_file(all_info)
    print("System information collected and saved to system_info.txt")

if __name__ == "__main__":
    main()
