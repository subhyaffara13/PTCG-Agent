
def random_serial_number() -> int:
    return int.from_bytes(os.urandom(20), "big") >> 1

