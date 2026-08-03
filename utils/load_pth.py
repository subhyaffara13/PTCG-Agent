from pathlib import Path


def load_pth(path):
    """Load a PyTorch state_dict from a .pth/.pt file into numpy arrays.
    Handles both zip-based (PyTorch >=1.6) and old pickle formats.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")

    raw = path.read_bytes()

    # zip-based format  (PyTorch >= 1.6)
    if raw[:2] == b"PK":
        return _load_zip_state(path)

    # old pickle format (fallback)
    return _load_pickle_state(raw)

