import socket
import time
import json
import threading

ELECTION_PORT = 9871
ELECTION_TIMEOUT = 5

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def run_election():
    local_ip = get_local_ip()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(('', ELECTION_PORT))
    sock.settimeout(2)

    peers = set([local_ip])
    end_time = time.time() + ELECTION_TIMEOUT

    def broadcast_election():
        while time.time() < end_time:
            msg = json.dumps({'type': 'election', 'ip': local_ip})
            try:
                sock.sendto(msg.encode(), ('<broadcast>', ELECTION_PORT))
            except:
                pass
            time.sleep(1)

    threading.Thread(target=broadcast_election, daemon=True).start()

    while time.time() < end_time:
        try:
            data, addr = sock.recvfrom(1024)
            msg = json.loads(data.decode())
            if msg.get('type') == 'election':
                peers.add(msg['ip'])
        except socket.timeout:
            continue
        except Exception:
            pass
            
    sock.close()
    
    # Lowest IP wins
    sorted_peers = sorted(list(peers))
    winner = sorted_peers[0]
    
    return winner == local_ip, winner
