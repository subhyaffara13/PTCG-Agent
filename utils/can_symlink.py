import os

def can_symlink(tmpdir):
    """
    Skip if cannot create a symbolic link
    """
    link_fn = 'link'
    target_fn = 'target'
    try:
        os.symlink(target_fn, link_fn)
    except (OSError, NotImplementedError, AttributeError):
        pytest.skip("Cannot create symbolic links")
    os.remove(link_fn)

