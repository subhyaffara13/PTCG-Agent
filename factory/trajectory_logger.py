import json
import gzip
import queue
import threading
import time
import logging
from pathlib import Path
from typing import Dict, Any
from factory.trajectory_helpers import get_new_file_path, prepare_match_record

logger = logging.getLogger(__name__)

class TrajectoryLogger:
    """Asynchronously logs game trajectories to disk in compressed JSONL format."""
    def __init__(self, log_dir: str = "logs/trajectories", max_records_per_file: int = 10000):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.max_records = max_records_per_file
        
        self.queue = queue.Queue()
        self.running = True
        self.current_file = None
        self.records_written_current = 0
        
        self.total_records_written = 0
        self.total_bytes_written = 0
        self.total_write_time = 0.0
        
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()

    def _worker_loop(self):
        while self.running or not self.queue.empty():
            try: record = self.queue.get(timeout=1.0)
            except queue.Empty: continue
                
            try:
                start_time = time.time()
                if self.current_file is None or self.records_written_current >= self.max_records:
                    if self.current_file is not None: self.current_file.close()
                    self.current_file = open(get_new_file_path(self.log_dir), 'at', encoding='utf-8')
                    self.records_written_current = 0
                
                json_str = json.dumps(record) + "\n"
                self.current_file.write(json_str)
                self.current_file.flush()
                
                self.records_written_current += 1
                self.total_records_written += 1
                self.total_bytes_written += len(json_str.encode('utf-8'))
                self.total_write_time += (time.time() - start_time)
            except Exception as e:
                logger.error(f"TrajectoryLogger failed to write record: {e}")
            finally:
                self.queue.task_done()
                
        if self.current_file is not None: self.current_file.close()

    def log_match(self, record: Dict[str, Any]):
        """Non-blocking put onto the background write queue."""
        self.queue.put(prepare_match_record(record))

    def flush(self):
        self.queue.join()
        if self.current_file is not None: self.current_file.flush()

    def shutdown(self):
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
