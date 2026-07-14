import os

log_path = "logs/master_server.log"
if os.path.exists(log_path):
    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        
        connections = [line.strip() for line in lines if "Worker connected from" in line]
        print(f"=== Worker Connection Events (Total: {len(connections)}) ===")
        for conn in connections[-20:]:
            print(conn)
            
        disconnections = [line.strip() for line in lines if "Worker disconnected" in line or "connection closed" in line]
        print(f"\n=== Worker Disconnection Events (Total: {len(disconnections)}) ===")
        for dis in disconnections[-20:]:
            print(dis)
    except Exception as e:
        print(f"Error checking logs: {e}")
else:
    print(f"{log_path} not found.")
