import subprocess
import socket
import sys

def get_ethernet_ip():
    """Finds the active local IP address of the machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connects to a dummy external IP to force network interface selection
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def init_head_node():
    ip_address = get_ethernet_ip()
    print(f"--> Detected Head Node IP: {ip_address}")
    print("--> Initializing Ray Head Node for the cluster...")
    
    # Start Ray with dashboard exposed to the local network
    ray_command = "ray start --head --port=6379 --dashboard-host=0.0.0.0"
    
    try:
        subprocess.run(ray_command, shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to start Ray. Make sure 'ray' is installed (pip install ray).")
        sys.exit(1)

    print("\n" + "="*60)
    print("🚀 HEAD NODE ACTIVE. CLUSTER READY FOR POKÉMON TCG AGENTS.")
    print("="*60)
    print("\nNext steps:")
    print("Go to your 4 Wi-Fi worker machines and run the following command in their terminals:\n")
    print(f"ray start --address='{ip_address}:6379'")
    print("\n" + "="*60)

if __name__ == "__main__":
    init_head_node()
