import socket
import threading
import pickle

latest_weights = pickle.dumps({"dummy_weights": [0.0, 0.0, 0.0]})
latest_archetype = "aggro"
experience_queue = []

def handle_client(conn, addr):
    global latest_weights, latest_archetype, experience_queue
    try:
        conn.settimeout(60.0)
        req = conn.recv(1024)
        if not req: return
        cmd = req.decode('utf-8').strip()
        print(f"--> [Master] Connection from {addr} - Command: {cmd}")
        if cmd == "GET_CONFIG":
            conn.sendall(pickle.dumps((latest_archetype, latest_weights)))
        elif cmd == "PUSH_EXP":
            conn.sendall(b"OK")
            size_bytes = conn.recv(4)
            if len(size_bytes) < 4:
                print(f"--> [Master] Protocol error: size header too short from {addr}")
                return
            size = int.from_bytes(size_bytes, 'big')
            data = b""
            while len(data) < size:
                packet = conn.recv(min(size - len(data), 4096))
                if not packet: break
                data += packet
            if len(data) == size:
                experience_queue.append(data)
                conn.sendall(b"ACK")
            else:
                print(f"--> [Master] Incomplete payload from {addr}")
        elif cmd == "POP_EXP":
            if experience_queue:
                data = experience_queue.pop(0)
                conn.sendall(len(data).to_bytes(4, 'big') + data)
            else:
                conn.sendall(b"EMPTY")
        elif cmd == "SET_WEIGHTS":
            conn.sendall(b"OK")
            size_bytes = conn.recv(4)
            if len(size_bytes) < 4: return
            size = int.from_bytes(size_bytes, 'big')
            data = b""
            while len(data) < size:
                packet = conn.recv(min(size - len(data), 4096))
                if not packet: break
                data += packet
            if len(data) == size:
                latest_weights = data
                conn.sendall(b"ACK")
    except (socket.timeout, ConnectionResetError, BrokenPipeError) as e:
        print(f"--> [Master] Graceful disconnect/timeout from {addr}: {e}")
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 5000))
    s.listen(10)
    print("--> Distributed Master socket server running on port 5000...")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
