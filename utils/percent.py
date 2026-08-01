
def PERCENT(string: str) -> str:
    return "".join([f"%{byte:02X}" for byte in string.encode("utf-8")])

