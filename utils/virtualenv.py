
def virtualenv(python_executable: str = sys.executable) -> Iterator[tuple[str, str]]:
    """Context manager that creates a virtualenv in a temporary directory

    Returns the path to the created Python executable
    """
    with tempfile.TemporaryDirectory() as venv_dir:
        proc = subprocess.run(
            [python_executable, "-m", "venv", venv_dir], cwd=os.getcwd(), capture_output=True
        )
        if proc.returncode != 0:
            err = proc.stdout.decode("utf-8") + proc.stderr.decode("utf-8")
            raise Exception("Failed to create venv.\n" + err)
        if sys.platform == "win32":
            yield venv_dir, os.path.abspath(os.path.join(venv_dir, "Scripts", "python"))
        else:
            yield venv_dir, os.path.abspath(os.path.join(venv_dir, "bin", "python"))

