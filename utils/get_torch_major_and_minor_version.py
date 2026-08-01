
def get_torch_major_and_minor_version() -> str:
    torch_version = get_torch_version()
    if torch_version == "N/A":
        return "N/A"
    parsed_version = version.parse(torch_version)
    return str(parsed_version.major) + "." + str(parsed_version.minor)

