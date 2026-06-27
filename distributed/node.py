import time
import logging
from .discovery import WorkerListener, MasterBeacon
from .election import run_election
from .code_sync import sync_code

logging.basicConfig(level=logging.INFO)

def start_node():
    logging.info("Starting node...")
    
    # Check if master exists
    listener = WorkerListener()
    logging.info("Listening for existing master...")
    master_ip, master_version = listener.listen_for_master()
    
    if master_ip:
        logging.info(f"Found master at {master_ip}")
        sync_code(master_version)
        # Placeholder for subagent 2 implementation
        logging.info("Launching worker client (mocked)")
    else:
        logging.info("No master found. Running election...")
        is_master, winner_ip = run_election()
        
        if is_master:
            logging.info(f"Elected as master ({winner_ip}). Starting beacon...")
            # Get local version
            from .code_sync import get_local_version
            version = get_local_version() or "unknown"
            
            beacon = MasterBeacon(code_version=version)
            beacon.start()
            
            # Placeholder for subagent 2 implementation
            logging.info("Launching master server (mocked)")
            
            # Keep alive
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                beacon.stop()
        else:
            logging.info(f"Elected worker. Master is {winner_ip}. Waiting for beacon...")
            master_ip, master_version = listener.listen_for_master()
            if master_version:
                sync_code(master_version)
            
            # Placeholder for subagent 2 implementation
            logging.info("Launching worker client (mocked)")

if __name__ == "__main__":
    start_node()
