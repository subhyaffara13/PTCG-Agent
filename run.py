"""
PTCG Agent Top-level Entrypoint.
Simplifies running the orchestration agent or master loop across all machines.

Usage:
  python run.py                <- Starts in auto-discovery mode (worker/master auto-election)
  python run.py --force master <- Force starts this machine as the Master server
"""
import sys
import os

if __name__ == "__main__":
    # Ensure current directory is in path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # Forward arguments and call orchestration_agent main
    from factory.orchestration_agent import main
    main()
