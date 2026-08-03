import os

def _hash_containing_file(filepath: str) -> str:
    # if the file does not exists we consider filepath to be the hash.
    if not os.path.exists(filepath):
        return filepath

    with open(filepath, "rb") as file:
        content = file.read()
        crc32_value = zlib.crc32(content)
        hash = format(crc32_value & 0xFFFFFFFF, "08x")
        return hash

