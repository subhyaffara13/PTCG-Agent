import os

def stat_proxy(path: str) -> os.stat_result:
    try:
        st = orig_stat(path)
    except OSError as err:
        print(f"stat({path!r}) -> {err}")
        raise
    else:
        print(
            "stat(%r) -> (st_mode=%o, st_mtime=%d, st_size=%d)"
            % (path, st.st_mode, st.st_mtime, st.st_size)
        )
        return st

