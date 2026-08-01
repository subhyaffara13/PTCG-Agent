
def create_vendor_txt_map() -> dict[str, str]:
    with open_text_resource("pip._vendor", "vendor.txt") as f:
        # Purge non version specifying lines.
        # Also, remove any space prefix or suffixes (including comments).
        lines = [
            line.strip().split(" ", 1)[0] for line in f.readlines() if "==" in line
        ]

    # Transform into "module" -> version dict.
    return dict(line.split("==", 1) for line in lines)

