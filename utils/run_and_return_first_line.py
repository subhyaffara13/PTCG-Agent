
def run_and_return_first_line(run_lambda, command):
    """Run command using run_lambda and returns first line if output is not empty."""
    rc, out, _ = run_lambda(command)
    if rc != 0:
        return None
    return out.split("\n")[0]

