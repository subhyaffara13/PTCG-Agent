from . import Path, logger, subprocess, sys, time

def script_log_path(script: str) -> str:
    return f"logs/{Path(script).stem}.log"

def launch_processes(scripts: list) -> list:
    processes = []
    for i, script in enumerate(scripts):
        if i > 0:
            time.sleep(15)
        log_path = script_log_path(script)
        try:
            f = open(log_path, "a", encoding="utf-8")
            p = subprocess.Popen([sys.executable, script], stdout=f, stderr=f)
            processes.append((p, f))
            logger.info(f"Started: {script} (PID {p.pid}) -> {log_path}")
        except Exception as e:
            logger.error(f"Failed to start {script}: {e}")
            processes.append((None, None))
    return processes

def monitor_and_restart(processes: list, scripts: list):
    for i, (p, f) in enumerate(processes):
        if p is None or p.poll() is not None:
            logger.warning(f"Sub-task {scripts[i]} stopped. Restarting...")
            if f is not None:
                try:
                    f.close()
                except Exception:
                    pass
            try:
                log_path = script_log_path(scripts[i])
                f = open(log_path, "a", encoding="utf-8")
                p = subprocess.Popen([sys.executable, scripts[i]], stdout=f, stderr=f)
                processes[i] = (p, f)
                logger.info(f"Restarted: {scripts[i]} (PID {p.pid}) -> {log_path}")
            except Exception as e:
                logger.error(f"Failed to restart {scripts[i]}: {e}")
                processes[i] = (None, None)

