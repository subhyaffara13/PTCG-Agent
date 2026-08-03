import sys
from .workerclient import WorkerClient

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    WorkerClient(host=host).start()
