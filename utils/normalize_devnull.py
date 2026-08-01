
def normalize_devnull(line: str) -> str:
    return line.replace("/dev/null", os.devnull)

