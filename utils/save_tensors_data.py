
def save_tensors_data(tensors_data: "TensorsData", path: "str | Path", *, smooth_quant: bool = False) -> None:
    """Serialize calibration tensor ranges to a JSON file at *path*.

    :param smooth_quant: whether the producing run used SmoothQuant.  Stored in
        the cache so a later load can detect a mismatch and recompute.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=".calibcache_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as f:
            payload = tensors_data.to_dict()
            payload["smooth_quant"] = smooth_quant
            json.dump(payload, f, cls=CalibrationCacheEncoder)
            f.flush()
        os.replace(tmp_name, path)
    except BaseException:
        with contextlib.suppress(FileNotFoundError):
            os.unlink(tmp_name)
        raise

