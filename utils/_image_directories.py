
def _image_directories(func):
    """
    Compute the baseline and result image directories for testing *func*.

    For test module ``foo.bar.test_baz``, the baseline directory is at
    ``foo/bar/baseline_images/test_baz`` and the result directory at
    ``$(pwd)/result_images/test_baz``.  The result directory is created if it
    doesn't exist.
    """
    module_path = Path(inspect.getfile(func))
    baseline_dir = module_path.parent / "baseline_images" / module_path.stem
    result_dir = Path().resolve() / "result_images" / module_path.stem
    result_dir.mkdir(parents=True, exist_ok=True)
    return baseline_dir, result_dir

