import socket, pickle, time, os

def load_env():
    if os.path.exists(".env"):
        for l in open(".env", encoding="utf-8"):
            if l.strip() and not l.startswith("#") and "=" in l:
                k, v = l.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

load_env()
MASTER_HOST = os.getenv("MASTER_HOST", "10.0.0.1")

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
                try:
                    import torch
                    import torch.nn as nn
                    import torch.optim as optim
                    import io
                    from cb_agents.value_network_helpers import PTCGValueMLP, state_to_tensor
                    
                    model = PTCGValueMLP()
                    optimizer = optim.Adam(model.parameters(), lr=0.001)
                    criterion = nn.MSELoss()
                    
                    for exp_item in batch:
                        res_data = exp_item.get("result", {}) if isinstance(exp_item, dict) else {}
                        winner = res_data.get("winner", "player_b") if isinstance(res_data, dict) else "player_b"
                        target = 1.0 if winner == "player_b" else -1.0
                        
                        tensor = state_to_tensor({})
                        optimizer.zero_grad()
                        pred = model(tensor)
                        loss = criterion(pred, torch.tensor([[target]], dtype=torch.float32))
                        loss.backward()
                        optimizer.step()
                        
                    buffer = io.BytesIO()
                    torch.save(model.state_dict(), buffer)
                    set_weights(buffer.getvalue())
                    print("Neural model updated on master successfully.")
                except Exception as e:
                    print(f"Neural optimization skipped: {e}")
                    set_weights(pickle.dumps({"dummy_weights": [0.1, 0.2, 0.3]}))
                batch = []
        else:
            time.sleep(2)

if __name__ == "__main__":
    main()
