
def make_writable(target) -> None:
    os.chmod(target, os.stat(target).st_mode | stat.S_IWRITE)

