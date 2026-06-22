import socket
import pickle
import time
import os
import sys

cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

from factory.game_runner import GameRunner, DEFAULT_DECK

MASTER_HOST = os.getenv("MASTER_HOST", "localhost")

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
        if not res_data:
            return "aggro", None
        arch, w_bytes = pickle.loads(res_data)
        return arch, pickle.loads(w_bytes)
    except Exception as e:
        print(f"--> [Worker] Failed to get config from master: {e}")
        return "aggro", None

def push_experience(payload):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(60.0)
        s.connect((MASTER_HOST, 5000))
        s.sendall(b"PUSH_EXP")
        ack = s.recv(1024)
        if ack == b"OK":
            s.sendall(len(payload).to_bytes(4, 'big') + payload)
            s.recv(1024)
        s.close()
    except Exception as e:
        print(f"--> [Worker] Failed to push experience: {e}")

def main():
    runner = GameRunner()
    print("--> Distributed Rollout Worker running...")
    while True:
        arch, weights = get_config()
        if weights is None:
            print("--> [Worker] Master offline or weights missing. Retrying in 10s...")
            time.sleep(10)
            continue
        try:
            res = runner.run_iteration(0, "base_v0", "new_v0", DEFAULT_DECK, DEFAULT_DECK, {}, {})
            payload = pickle.dumps({"archetype": arch, "result": res, "timestamp": time.time()})
            push_experience(payload)
            print("--> [Worker] Successfully pushed rollout trajectory to master.")
        except Exception as e:
            print(f"--> [Worker] Simulation error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
