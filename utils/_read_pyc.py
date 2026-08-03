import os
from typing import Callable
from pathlib import Path


def _read_pyc(
    source: Path, pyc: Path, trace: Callable[[str], None] = lambda x: None
) -> types.CodeType | None:
    """Possibly read a pytest pyc containing rewritten code.

    Return rewritten code if successful or None if not.
    """
    try:
        fp = open(pyc, "rb")
    except OSError:
        return None
    with fp:
        try:
            stat_result = os.stat(source)
            mtime = int(stat_result.st_mtime)
            size = stat_result.st_size
            data = fp.read(16)
        except OSError as e:
            trace(f"_read_pyc({source}): OSError {e}")
            return None
        # Check for invalid or out of date pyc file.
        if len(data) != (16):
            trace(f"_read_pyc({source}): invalid pyc (too short)")
            return None
        if data[:4] != importlib.util.MAGIC_NUMBER:
            trace(f"_read_pyc({source}): invalid pyc (bad magic number)")
            return None
        if data[4:8] != b"\x00\x00\x00\x00":
            trace(f"_read_pyc({source}): invalid pyc (unsupported flags)")
            return None
        mtime_data = data[8:12]
        if int.from_bytes(mtime_data, "little") != mtime & 0xFFFFFFFF:
            trace(f"_read_pyc({source}): out of date")
            return None
        size_data = data[12:16]
        if int.from_bytes(size_data, "little") != size & 0xFFFFFFFF:
            trace(f"_read_pyc({source}): invalid pyc (incorrect size)")
            return None
        try:
            co = marshal.load(fp)
        except Exception as e:
            trace(f"_read_pyc({source}): marshal.load error {e}")
            return None
        if not isinstance(co, types.CodeType):
            trace(f"_read_pyc({source}): not a code object")
            return None
        return co

