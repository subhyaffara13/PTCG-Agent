
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

