import psutil
import platform
from datetime import datetime
import colorama
from colorama import Fore
colorama.init()


boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
uname = platform.uname()
svmem = psutil.virtual_memory()
svcpu = psutil.cpu_count(logical=True)

home = f"""
{Fore.BLUE}
███████╗██╗   ██╗███████╗    ██╗███╗   ██╗███████╗ ██████╗ 
██╔════╝╚██╗ ██╔╝██╔════╝    ██║████╗  ██║██╔════╝██╔═══██╗
███████╗ ╚████╔╝ ███████╗    ██║██╔██╗ ██║█████╗  ██║   ██║
╚════██║  ╚██╔╝  ╚════██║    ██║██║╚██╗██║██╔══╝  ██║   ██║
███████║   ██║   ███████║    ██║██║ ╚████║██║     ╚██████╔╝
╚══════╝   ╚═╝   ╚══════╝    ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ 
{Fore.RESET}
Basic Info
{Fore.RED} |{Fore.RESET} System: {uname.system}
{Fore.RED} |{Fore.RESET} Processor: {uname.processor}
{Fore.RED} |{Fore.RESET} Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}
{Fore.RED} |{Fore.RESET} CPU Cores: {svcpu}
{Fore.RED} |{Fore.RESET} RAM: {svmem.total}bytes
{Fore.RED} |{Fore.RESET} Storage: {Fore.YELLOW}Coming Soon{Fore.RESET}

More In Depth View
[1]: {Fore.BLUE}Sysytem{Fore.RESET}
[2]: {Fore.RED}CPU{Fore.RESET}
[3]: {Fore.GREEN}RAM{Fore.RESET}
[4]: {Fore.MAGENTA}Storage{Fore.RESET}
[5]: {Fore.YELLOW}Network{Fore.RESET}
"""

def Menu(home):
    print(home)
    print("\n Please input a number that you would like to see [1-5]")
    option = input("> ")
    if option ==  "1":
        System()
    elif option == "2":
        CPU()
    elif option == "3":
        RAM()
    elif option == "4":
        Storage()
    elif option == "5":
        Network()
    else:
        Menu(home)

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def System():
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")
    print("\n Press B to go back to menu")
    sys = input("> ")
    if sys == "B":
        Menu(home)
    elif sys == "b":
        Menu(home)
    else:
        print("Not a option")
def CPU():
    # number of cores
    print("Physical cores:", psutil.cpu_count(logical=False))
    print("Total cores:", psutil.cpu_count(logical=True))
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    # CPU usage
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")
    print("\n Press B to go back to menu")
    sys = input("> ")
    if sys == "B":
        Menu(home)
    elif sys == "b":
        Menu(home)
    else:
        print("Not a option")
def RAM():
    svmem1 = psutil.virtual_memory()
    print(f"Total: {get_size(svmem1.total)}")
    print(f"Available: {get_size(svmem1.available)}")
    print(f"Used: {get_size(svmem1.used)}")
    print(f"Percentage: {svmem1.percent}%")
    print("=" * 20, "SWAP", "=" * 20)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    print(f"Total: {get_size(swap.total)}")
    print(f"Free: {get_size(swap.free)}")
    print(f"Used: {get_size(swap.used)}")
    print(f"Percentage: {swap.percent}%")
    print("\n Press B to go back to menu")
    sys = input("> ")
    if sys == "B":
        Menu(home)
    elif sys == "b":
        Menu(home)
    else:
        print("Not a option")
def Storage():
    print("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        print(f"  Total Size: {get_size(partition_usage.total)}")
        print(f"  Used: {get_size(partition_usage.used)}")
        print(f"  Free: {get_size(partition_usage.free)}")
        print(f"  Percentage: {partition_usage.percent}%")
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print(f"Total read: {get_size(disk_io.read_bytes)}")
    print(f"Total write: {get_size(disk_io.write_bytes)}")
    print("\n Press B to go back to menu")
    sys = input("> ")
    if sys == "B":
        Menu(home)
    elif sys == "b":
        Menu(home)
    else:
        print("Not a option")
def Network():
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            print(f"=== Interface: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IP Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"  MAC Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast MAC: {address.broadcast}")
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
    print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")
    print("\n Press B to go back to menu")
    sys = input("> ")
    if sys == "b":
        Menu(home)
    elif sys == "B":
        Menu(home)
    else:
        print("Not a option")

Menu(home)