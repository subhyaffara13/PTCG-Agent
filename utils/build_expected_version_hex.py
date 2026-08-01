
def build_expected_version_hex(matches: Dict[str, str]) -> str:
    patch_level_serial = matches["PATCH"]
    serial = None
    major = int(matches["MAJOR"])
    minor = int(matches["MINOR"])
    flds = patch_level_serial.split(".")
    if flds:
        patch = int(flds[0])
        if len(flds) == 1:
            level = "0"
            serial = 0
        elif len(flds) == 2:
            level_serial = flds[1]
            for level in ("a", "b", "c", "dev"):
                if level_serial.startswith(level):
                    serial = int(level_serial[len(level) :])
                    break
    if serial is None:
        msg = f'Invalid PYBIND11_VERSION_PATCH: "{patch_level_serial}"'
        raise RuntimeError(msg)
    version_hex_str = f"{major:02x}{minor:02x}{patch:02x}{level[:1]}{serial:x}"
    return f"0x{version_hex_str.upper()}"

