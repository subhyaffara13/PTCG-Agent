
def cmd_exists(cmd):
    return shutil.which(cmd) is not None

