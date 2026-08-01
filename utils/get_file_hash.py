
def get_file_hash(path, block_size=2 ** 20):
    sha256 = hashlib.sha256(usedforsecurity=False)
    with open(path, 'rb') as fd:
        while True:
            data = fd.read(block_size)
            if not data:
                break
            sha256.update(data)

    if Path(path).suffix == '.pdf':
        sha256.update(str(mpl._get_executable_info("gs").version).encode('utf-8'))
    elif Path(path).suffix == '.svg':
        sha256.update(str(mpl._get_executable_info("inkscape").version).encode('utf-8'))

    return sha256.hexdigest()


def get_file_hash(filepath: str) -> str:
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

