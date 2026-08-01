
def explore_directories(start, exclude, ignore):
    '''Explore files and directories under `start`. `explore` and `ignore`
    arguments are the same as in :func:`iter_filenames`.
    '''
    for root, dirs, files in os.walk(start):
        dirs[:] = list(filter_out(dirs, ignore))
        fullpaths = (os.path.normpath(os.path.join(root, p)) for p in files)
        for filename in filter_out(fullpaths, exclude):
            if not os.path.basename(filename).startswith(
                '.'
            ) and _is_python_file(filename):
                yield filename

