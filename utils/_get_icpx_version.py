
def _get_icpx_version() -> str:
    icpx = 'icx' if IS_WINDOWS else 'icpx'
    compiler_info = subprocess.check_output([icpx, '--version'])
    match = re.search(r'(\d+)\.(\d+)\.(\d+)', compiler_info.decode().strip())
    version = ['0', '0', '0'] if match is None else list(match.groups())
    version = list(map(int, version))
    if len(version) != 3:
        raise AssertionError("Failed to parse DPC++ compiler version")
    # Aligning version format with what torch.version.xpu() returns
    return f"{version[0]}{version[1]:02}{version[2]:02}"

