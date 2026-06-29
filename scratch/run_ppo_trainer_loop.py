import sys
import os
import time
import logging
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path
from threading import Event

from scratch.run_ppo_trainer_loop_parts import process_if_changed, TELEMETRY_PATH

FALLBACK_POLL_SECONDS = 1.0


def _run_watchdog_loop():
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

    changed = Event()
    watch_dir = TELEMETRY_PATH.parent
    watch_name = TELEMETRY_PATH.name

    class TelemetryHandler(FileSystemEventHandler):
        def on_created(self, event):
            if Path(event.src_path).name == watch_name:
                changed.set()

        def on_modified(self, event):
            if Path(event.src_path).name == watch_name:
                changed.set()

        def on_moved(self, event):
            if Path(event.dest_path).name == watch_name:
                changed.set()

    watch_dir.mkdir(parents=True, exist_ok=True)
    observer = Observer()
    observer.schedule(TelemetryHandler(), str(watch_dir), recursive=False)
    observer.start()
    print(f"Watching {TELEMETRY_PATH} with watchdog events.")

    last_mtime = process_if_changed(0.0)
    try:
        while True:
            changed.wait()
            changed.clear()
            last_mtime = process_if_changed(last_mtime)
    finally:
        observer.stop()
        observer.join()


def _run_polling_fallback():
    print(
        f"watchdog is not installed; falling back to {FALLBACK_POLL_SECONDS:.1f}s telemetry polling."
    )
    last_mtime = process_if_changed(0.0)
    while True:
        last_mtime = process_if_changed(last_mtime)
        time.sleep(FALLBACK_POLL_SECONDS)


def main():
    print("Starting Decoupled PPO Trainer Loop...")
    try:
        _run_watchdog_loop()
    except ImportError:
        _run_polling_fallback()


if __name__ == "__main__":
    main()
