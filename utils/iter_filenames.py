import os

def iter_filenames(paths, exclude=None, ignore=None):
    '''A generator that yields all sub-paths of the ones specified in
    `paths`. Optional `exclude` filters can be passed as a comma-separated
    string of regexes, while `ignore` filters are a comma-separated list of
    directory names to ignore. Ignore patterns are can be plain names or glob
    patterns. If paths contains only a single hyphen, stdin is implied,
    returned as is.
    '''
    if set(paths) == set(('-',)):
        yield '-'
        return
    exclude = exclude.split(',') if exclude else []
    ignore = '.*,{0}'.format(ignore).split(',') if ignore else ['.*']
    for path in paths:
        if (
            os.path.isfile(path)
            and _is_python_file(path)
            and (
                not exclude
                or not any(fnmatch.fnmatch(path, p) for p in exclude)
            )
        ):
            yield path
            continue
        for filename in explore_directories(path, exclude, ignore):
            yield filename

