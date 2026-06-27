import psutil
import os

def cleanup():
    current_pid = os.getpid()
    print(f"Current process PID: {current_pid}")
    
    count = 0
    for p in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Kill any python process that is not our current script execution
            if p.info.get('name') and 'python' in p.info['name'].lower():
                pid = p.info['pid']
                if pid != current_pid:
                    print(f"Killing python process PID {pid}: {p.info.get('cmdline')}")
                    p.kill()
                    count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    print(f"Cleaned up {count} python processes.")

if __name__ == "__main__":
    cleanup()
