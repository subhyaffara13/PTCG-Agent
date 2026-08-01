import sys
import os
import signal

from utils._sigint_handler import _sigint_handler

try:
    signal.signal(signal.SIGINT, _sigint_handler)
except Exception:
    pass

if __name__ == "__main__":
    if "--worker" in sys.argv:
        from distributed.distributed_worker import main as worker_main
        worker_main()
    elif "--master" in sys.argv:
        from factory.orchestration_agent import main as master_main
        master_main()
    elif "--test" in sys.argv:
        import run_integration_test
    else:
        # Default zero-argument execution: Auto-Discovery Election Mode
        from factory.orchestration_agent import main as auto_discovery_main
        auto_discovery_main()
