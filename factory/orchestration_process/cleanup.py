from . import logger

def cleanup(processes: list):
    logger.info("Cleaning up sub-tasks...")
    # First send terminate to all processes immediately to trigger fast shutdowns
    for p, f in processes:
        if p is not None:
            try:
                p.terminate()
            except Exception:
                pass
                
    # Now wait for them to exit, falling back to force-kill if interrupted
    for p, f in processes:
        if p is None:
            continue
        try:
            p.wait(timeout=2)
        except BaseException:
            try:
                p.kill()
            except Exception:
                pass
        if f is not None:
            try:
                f.close()
            except Exception:
                pass

