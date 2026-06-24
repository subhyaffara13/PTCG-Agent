import socket
import pickle
import time
import os
import sys
import subprocess

cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

from factory.game_runner import GameRunner, DEFAULT_DECK

MASTER_HOST = os.getenv("MASTER_HOST", "10.0.0.1")

def get_config():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(60.0)
        s.connect((MASTER_HOST, 5000))
        s.sendall(b"GET_CONFIG")
        res_data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk: break
            res_data += chunk
        s.close()
        return pickle.loads(res_data) if res_data else ("aggro", None)
    except Exception as e:
        print(f"--> [Worker] Config fetch failed: {e}")
        return "aggro", None

def push_experience(payload):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(60.0)
        s.connect((MASTER_HOST, 5000))
        s.sendall(b"PUSH_EXP")
        if s.recv(1024) == b"OK":
            s.sendall(len(payload).to_bytes(4, 'big') + payload)
            s.recv(1024)
        s.close()
    except Exception as e:
        print(f"--> [Worker] Push experience failed: {e}")

def detect_connection_type() -> str:
    try:
        res = subprocess.run("netsh interface show interface", shell=True, capture_output=True, text=True)
        wifi, eth = False, False
        for line in res.stdout.splitlines():
            line_lower = line.lower()
            if "connected" in line_lower:
                if "wi-fi" in line_lower or "wireless" in line_lower: wifi = True
                elif "ethernet" in line_lower or "lan" in line_lower: eth = True
        if eth: return "ethernet"
        if wifi: return "wifi"
    except: pass
    return "ethernet"

def main():
    runner = GameRunner()
    conn_type = detect_connection_type()
    print(f"--> Distributed Rollout Worker running on {conn_type.upper()}...")
    
    weights_cache, arch_cache = None, "aggro"
    iteration_count = 0
    
    while True:
        iteration_count += 1
        query_master = True
        if conn_type == "wifi" and weights_cache is not None:
            if iteration_count % 5 != 0:
                query_master = False
                
        if query_master:
            arch, weights = get_config()
            if weights is not None:
                weights_cache, arch_cache = weights, arch
            elif weights_cache is None:
                print("--> [Worker] Master offline, retrying in 10s...")
                time.sleep(10)
                continue
        else:
            arch, weights = arch_cache, weights_cache
            
        try:
            res = runner.run_iteration(0, "base_v0", "new_v0", DEFAULT_DECK, DEFAULT_DECK, {}, {})
            payload = pickle.dumps({"archetype": arch, "result": res, "timestamp": time.time()})
            push_experience(payload)
            print("--> [Worker] Successfully pushed rollout trajectory.")
        except Exception as e:
            print(f"--> [Worker] Simulation error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
