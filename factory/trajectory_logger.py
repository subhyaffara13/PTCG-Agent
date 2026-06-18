import json
import gzip
import queue
import threading
import time
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TrajectoryLogger:
    """
    Asynchronously logs game trajectories to disk in compressed JSONL format.
    
    Prevents the simulation loop from bottlenecking on disk I/O by pushing records
    to a background queue. The worker thread compresses and batches these records,
    auto-rotating files to prevent massive single-file log blobs.
    """
    def __init__(self, log_dir: str = "logs/trajectories", max_records_per_file: int = 10000):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.max_records = max_records_per_file
        
        self.queue = queue.Queue()
        self.running = True
        self.current_file = None
        self.records_written_current = 0
        
        # Stats
        self.total_records_written = 0
        self.total_bytes_written = 0
        self.total_write_time = 0.0
        
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        
    def _get_new_file_path(self) -> Path:
        timestamp = int(time.time())
        return self.log_dir / f"trajectory_{timestamp}.jsonl.gz"

    def _worker_loop(self):
        while self.running or not self.queue.empty():
            try:
                # Block for up to 1 second
                record = self.queue.get(timeout=1.0)
            except queue.Empty:
                continue
                
            try:
                start_time = time.time()
                
                # Rotate file if needed
                if self.current_file is None or self.records_written_current >= self.max_records:
                    if self.current_file is not None:
                        self.current_file.close()
                    path = self._get_new_file_path()
                    self.current_file = gzip.open(path, 'at', encoding='utf-8')
                    self.records_written_current = 0
                
                # Write record
                json_str = json.dumps(record) + "\n"
                self.current_file.write(json_str)
                
                # Update stats
                self.records_written_current += 1
                self.total_records_written += 1
                self.total_bytes_written += len(json_str.encode('utf-8'))
                self.total_write_time += (time.time() - start_time)
                
            except Exception as e:
                logger.error(f"TrajectoryLogger failed to write record: {e}")
            finally:
                self.queue.task_done()
                
        # Cleanup on shutdown
        if self.current_file is not None:
            self.current_file.close()

    def log_match(self, record: Dict[str, Any]):
        """Non-blocking put onto the background write queue."""
        self.queue.put(record)

    def flush(self):
        """Blocks until the queue is fully drained."""
        self.queue.join()
        if self.current_file is not None:
            self.current_file.flush()

    def shutdown(self):
        """Gracefully shuts down the background thread."""
        self.running = False
        self.flush()
        self.worker_thread.join(timeout=5.0)
        
    def get_stats(self) -> Dict[str, Any]:
        avg_time = self.total_write_time / max(1, self.total_records_written)
        return {
            "total_records": self.total_records_written,
            "total_bytes": self.total_bytes_written,
            "queue_size": self.queue.qsize(),
            "avg_write_time_ms": avg_time * 1000
        }
