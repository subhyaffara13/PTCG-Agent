import os
import re
import subprocess

def check_compiler_is_gcc(compiler) -> bool:
    if not IS_LINUX:
        return False

    env = os.environ.copy()
    env['LC_ALL'] = 'C'  # Don't localize output
    try:
        version_string = subprocess.check_output([compiler, '-v'], stderr=subprocess.STDOUT, env=env).decode(*SUBPROCESS_DECODE_ARGS)
    except (subprocess.CalledProcessError, OSError):
        try:
            version_string = subprocess.check_output([compiler, '--version'], stderr=subprocess.STDOUT, env=env).decode(*SUBPROCESS_DECODE_ARGS)
        except (subprocess.CalledProcessError, OSError):
            return False
    # Check for GCC by verifying both COLLECT_GCC and gcc version string are present
    # This works for c++, g++, gcc, and versioned variants like g++-13
    pattern = re.compile("^COLLECT_GCC=(.*)$", re.MULTILINE)
    has_collect_gcc = pattern.search(version_string) is not None
    if has_collect_gcc and 'gcc version' in version_string:
        return True
    return False

