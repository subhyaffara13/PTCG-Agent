import os
from pathlib import Path


def break_lock_file(lock_file: str, mtime_before: float, ino_before: int) -> None:
    """
    Atomically break a stale lock file that was judged stale at modification time *mtime_before*.

    The file is renamed to a process-private name before being unlinked, so two processes breaking the same lock
    cannot delete each other's work (only one rename of a given inode succeeds; the loser gets ``OSError``). After the
    rename the file is re-checked: a newer modification time, or a different inode than *ino_before*, means a peer
    recreated the lock between the stale decision and the rename, so we grabbed a live file and must abort, leaving the
    renamed file in place rather than rolling back (a rollback rename is itself racy — same trade-off as the soft
    read/write marker break). The inode check matters because filesystems with coarse modification-time granularity
    (NFS, FAT) can give a same-second recreation the old mtime, so mtime alone would not catch it and a live lock would
    be unlinked; the inode is the reliable identity, mirroring the token re-check in the soft read/write marker break.
    ``lstat`` is used so a hostile symlink swapped in after the decision is not followed.

    :param lock_file: path to the lock file to break.
    :param mtime_before: modification time observed when the lock was judged stale.
    :param ino_before: inode number observed when the lock was judged stale.

    :raises OSError: if the rename fails (e.g. the file vanished or is not owned in a sticky directory).

    """
    break_path = f"{lock_file}.break.{os.getpid()}"
    Path(lock_file).rename(break_path)
    try:
        st_after = os.lstat(break_path)
    except OSError:
        return
    if st_after.st_mtime > mtime_before or st_after.st_ino != ino_before:
        return
    Path(break_path).unlink()

