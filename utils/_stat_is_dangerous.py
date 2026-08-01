
def _stat_is_dangerous(mode):
    return (
        mode & stat.S_IWOTH
        or mode & stat.S_IWGRP
        or mode & stat.S_IXGRP
        or mode & stat.S_IXOTH
    )

