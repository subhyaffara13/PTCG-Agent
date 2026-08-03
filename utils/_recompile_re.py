import re

def _recompile_re() -> None:
    global SKIP_DIRS_RE
    SKIP_DIRS_RE = re.compile(
        rf"^[^\s<]*({'|'.join(re.escape(_as_posix_path(d)) for d in SKIP_DIRS)})"
    )

