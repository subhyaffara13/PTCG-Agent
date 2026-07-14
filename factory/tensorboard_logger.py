"""
factory/tensorboard_logger.py

Singleton TensorBoard logger. Falls back to no-op if tensorboard is not installed.
Usage: TBLogger.get().log_scalar('train/loss', 0.5, step=100)
"""
import logging
import threading
import json
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    from torch.utils.tensorboard import SummaryWriter
    HAS_TB = True
except ImportError:
    HAS_TB = False
    logger.info("TensorBoard not available. Logging will be no-op.")


class TBLogger:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self._writer = None
        self._step_path = Path("models/tb_global_step.json")
        self._global_step = self._load_step()
        if HAS_TB:
            try:
                self._writer = SummaryWriter(log_dir="runs/ptcg_training")
                logger.info("TensorBoard logger initialized. Log dir: runs/ptcg_training/")
            except Exception as e:
                logger.warning(f"Failed to create TensorBoard writer: {e}")

    @classmethod
    def get(cls) -> "TBLogger":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def _load_step(self) -> int:
        try:
            if self._step_path.exists():
                data = json.loads(self._step_path.read_text(encoding="utf-8"))
                return int(data.get("global_step", 0))
        except Exception:
            pass
        return 0

    def _save_step(self):
        try:
            self._step_path.parent.mkdir(parents=True, exist_ok=True)
            self._step_path.write_text(
                json.dumps({"global_step": self._global_step}), encoding="utf-8"
            )
        except Exception:
            pass

    @property
    def global_step(self) -> int:
        return self._global_step

    def increment_step(self) -> int:
        self._global_step += 1
        self._save_step()
        return self._global_step

    def log_scalar(self, tag: str, value: float, step: int = None):
        if self._writer is None:
            return
        if step is None:
            step = self._global_step
        try:
            self._writer.add_scalar(tag, value, step)
        except Exception as e:
            logger.debug(f"TBLogger.log_scalar failed: {e}")

    def log_scalars(self, main_tag: str, tag_dict: dict, step: int = None):
        if self._writer is None:
            return
        if step is None:
            step = self._global_step
        try:
            self._writer.add_scalars(main_tag, tag_dict, step)
        except Exception as e:
            logger.debug(f"TBLogger.log_scalars failed: {e}")

    def log_histogram(self, tag: str, values, step: int = None):
        if self._writer is None:
            return
        if step is None:
            step = self._global_step
        try:
            self._writer.add_histogram(tag, values, step)
        except Exception as e:
            logger.debug(f"TBLogger.log_histogram failed: {e}")

    def flush(self):
        if self._writer is not None:
            try:
                self._writer.flush()
            except Exception:
                pass

    def close(self):
        if self._writer is not None:
            try:
                self._writer.close()
            except Exception:
                pass
