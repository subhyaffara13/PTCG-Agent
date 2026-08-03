import re

def get_linux_pkg_version(run_lambda, pkg_name):
    pkg_mgr = _detect_linux_pkg_manager()
    if pkg_mgr == "N/A":
        return "N/A"

    grep_version = {
        "dpkg": {
            "field_index": 2,
            "command": "dpkg -l | grep {}",
        },
        "dnf": {
            "field_index": 1,
            "command": "dnf list | grep {}",
        },
        "yum": {
            "field_index": 1,
            "command": "yum list | grep {}",
        },
        "zypper": {
            "field_index": 2,
            "command": "zypper info {} | grep Version",
        },
    }

    field_index: int = int(_cast(int, grep_version[pkg_mgr]["field_index"]))
    cmd: str = str(grep_version[pkg_mgr]["command"])
    cmd = cmd.format(pkg_name)
    ret = run_and_read_all(run_lambda, cmd)
    if ret is None or ret == "":
        return "N/A"
    lst = re.sub(" +", " ", ret).split(" ")
    if len(lst) <= field_index:
        return "N/A"
    return lst[field_index]

