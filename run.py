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
        from run_factory import run_team_pipeline
        run_team_pipeline(1)
