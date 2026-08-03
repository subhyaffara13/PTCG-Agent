import os

def _stat_key(s: str) -> tuple[int, int]:
    # same as what's used by samefile / samestat
    st = os.stat(s)
    return st.st_ino, st.st_dev

