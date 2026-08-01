
def _detect_linux_pkg_manager():
    if get_platform() != "linux":
        return "N/A"
    for mgr_name in ["dpkg", "dnf", "yum", "zypper"]:
        rc, _, _ = run(f"which {mgr_name}")
        if rc == 0:
            return mgr_name
    return "N/A"

