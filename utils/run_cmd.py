
def run_cmd(input: str) -> tuple[int, str]:
    if input[1:].startswith("mypy run --") and "--show-error-codes" not in input:
        input += " --hide-error-codes"
    if input.startswith("dmypy "):
        input = sys.executable + " -m mypy." + input
    if input.startswith("mypy "):
        input = sys.executable + " -m" + input
    env = os.environ.copy()
    env["PYTHONPATH"] = PREFIX
    try:
        output = subprocess.check_output(
            input, shell=True, stderr=subprocess.STDOUT, text=True, cwd=test_temp_dir, env=env
        )
        return 0, output
    except subprocess.CalledProcessError as err:
        return err.returncode, err.output

