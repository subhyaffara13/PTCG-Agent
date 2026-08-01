
def _is_armhf():
    # Check if the current platform is ARMHF (32-bit ARM architecture)
    architecture = platform.architecture()
    return platform.machine().startswith('arm') and architecture[0] == '32bit'

