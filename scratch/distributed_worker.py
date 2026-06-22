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
        s.connect((MASTER_HOST, 5000))
        s.sendall(b"GET_CONFIG")
        arch, w_bytes = pickle.loads(s.recv(4096))
        s.close()
        return arch, pickle.loads(w_bytes)
    except Exception as e:
        print(f"Failed to get config: {e}")
        return "aggro", None

def push_experience(payload):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((MASTER_HOST, 5000))
        s.sendall(b"PUSH_EXP")
        if s.recv(1024) == b"OK":
            s.sendall(len(payload).to_bytes(4, 'big') + payload)
            s.recv(1024)
        s.close()
    except Exception as e:
        print(f"Failed to push experience: {e}")

def main():
    runner = GameRunner()
    print("Distributed Rollout Worker running...")
    while True:
        arch, weights = get_config()
        try:
            res = runner.run_iteration(0, "base_v0", "new_v0", DEFAULT_DECK, DEFAULT_DECK, {}, {})
            payload = pickle.dumps({"archetype": arch, "result": res, "timestamp": time.time()})
            push_experience(payload)
            print("Successfully pushed rollout trajectory to master.")
        except Exception as e:
            print(f"Simulation error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
