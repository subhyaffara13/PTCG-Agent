
def create_tree(base_dir, files, mode=0o777, verbose=True):
    """Create all the empty directories under 'base_dir' needed to put 'files'
    there.

    'base_dir' is just the name of a directory which doesn't necessarily
    exist yet; 'files' is a list of filenames to be interpreted relative to
    'base_dir'.  'base_dir' + the directory portion of every file in 'files'
    will be created if it doesn't already exist.  'mode' and 'verbose'
    flags are as for 'mkpath()'.
    """
    # First get the list of directories to create
    need_dir = set(os.path.join(base_dir, os.path.dirname(file)) for file in files)

    # Now create them
    for dir in sorted(need_dir):
        mkpath(dir, mode, verbose=verbose)

