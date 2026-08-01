
def log_list(lst, *args, **kwargs):
    '''Log an entire list, line by line. All the arguments are directly passed
    to :func:`~radon.cli.log`.
    '''
    for line in lst:
        log(line, *args, **kwargs)

