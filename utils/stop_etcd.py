import subprocess

def stop_etcd(subprocess, data_dir: str | None = None):
    if subprocess and subprocess.poll() is None:
        logger.info("stopping etcd server")
        subprocess.terminate()
        subprocess.wait()

    if data_dir:
        logger.info("deleting etcd data dir: %s", data_dir)
        shutil.rmtree(data_dir, ignore_errors=True)

