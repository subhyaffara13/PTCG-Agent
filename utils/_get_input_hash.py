from typing import List
from pathlib import Path


def _get_input_hash(file_list: List[str]) -> str:
    """Computes a hash of the input files (modification times + size).
    
    Using just path+mtime+size is much faster than hashing content.
    """
    hasher = hashlib.md5()
    # Sort to ensure deterministic order
    for file_path in sorted(file_list):
        path = Path(file_path)
        try:
            stat = path.stat()
            # Include path, mtime, size in hash
            # Relative path is better but absolute is safer if different machines (though cache is local)
            # We use absolute path here since it's local cache
            info = f"{path.absolute()}:{stat.st_mtime}:{stat.st_size}"
            hasher.update(info.encode('utf-8'))
        except OSError:
            pass  # Skip missing files

    return hasher.hexdigest()

