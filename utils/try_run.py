
def try_run(commands):
    """Run a series of commands and only return True if all ran fine."""
    if IS_WASM:
        return False
    with open(os.devnull, 'w') as null:
        for command in commands:
            retcode = subprocess.call(command, stdout=null, shell=True,
                    stderr=subprocess.STDOUT)
            if retcode != 0:
                return False
    return True

