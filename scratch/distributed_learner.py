import socket
import pickle
import time
import os

MASTER_HOST = os.getenv("MASTER_HOST", "localhost")

def pop_experience():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((MASTER_HOST, 5000))
        s.sendall(b"POP_EXP")
        resp = s.recv(1024)
        if resp == b"EMPTY":
            s.close()
            return None
        size = int.from_bytes(resp[:4], 'big')
        data = resp[4:]
        while len(data) < size:
            packet = s.recv(size - len(data))
            if not packet: break
            data += packet
        s.close()
        return pickle.loads(data)
    except Exception as e:
        print(f"Failed to pop experience: {e}")
        return None

def set_weights(weights):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((MASTER_HOST, 5000))
        s.sendall(b"SET_WEIGHTS")
        if s.recv(1024) == b"OK":
            data = pickle.dumps(weights)
            s.sendall(len(data).to_bytes(4, 'big') + data)
            s.recv(1024)
        s.close()
    except Exception as e:
        print(f"Failed to set weights: {e}")

def main():
    print("Distributed Learner running...")
    batch = []
    while True:
        exp = pop_experience()
        if exp:
            batch.append(exp)
            print(f"Received experience. Batch: {len(batch)}/5")
            if len(batch) >= 5:
                print("Optimizing policy network using batch of experiences...")
                time.sleep(0.5)
                set_weights({"dummy_weights": [0.1, 0.2, 0.3]})
                batch = []
        else:
            time.sleep(2)

if __name__ == "__main__":
    main()
