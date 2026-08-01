
def torchrun(script: str, nproc_per_node: int, is_torchrun: bool = True, env: dict | None = None):
    """Run the `script` using `torchrun` command for multi-processing in a subprocess. Captures errors as necessary."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".py") as tmp:
        tmp.write(script)
        tmp.flush()
        tmp.seek(0)
        if is_torchrun:
            cmd = (
                f"torchrun --nproc_per_node {nproc_per_node} --master_port {get_torch_dist_unique_port()} {tmp.name}"
            ).split()
        else:
            cmd = ["python3", tmp.name]

        # Note that the subprocess will be waited for here, and raise an error if not successful
        try:
            _ = subprocess.run(cmd, capture_output=True, env=env, text=True, check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(f"The following error was captured: {e.stderr}")

