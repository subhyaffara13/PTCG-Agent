import sys

def _run_build(path, *flags):
    cmd = [sys.executable, "-m", "build", "--no-isolation", *flags, str(path)]
    return run(cmd, env={'DISTUTILS_DEBUG': ''})

