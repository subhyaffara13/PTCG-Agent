import os

def symlink_or_skip_test(src, dst):
    try:
        os.symlink(src, dst)
    except (OSError, NotImplementedError):
        pytest.skip("symlink not supported in OS")
        return None
    return dst

