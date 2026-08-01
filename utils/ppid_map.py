
def ppid_map():
    """Obtain a {pid: ppid, ...} dict for all running processes in
    one shot. Used to speed up Process.children().
    """
    ret = {}
    procfs_path = get_procfs_path()
    for pid in pids():
        try:
            with open_binary(f"{procfs_path}/{pid}/stat") as f:
                data = f.read()
        except (FileNotFoundError, ProcessLookupError):
            pass
        except PermissionError as err:
            raise AccessDenied(pid) from err
        else:
            rpar = data.rfind(b')')
            dset = data[rpar + 2 :].split()
            ppid = int(dset[1])
            ret[pid] = ppid
    return ret

