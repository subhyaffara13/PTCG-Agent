import sys
import os

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
