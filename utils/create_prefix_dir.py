
def create_prefix_dir(nb_file, fmt, log):
    """Create directory if fmt has a prefix"""
    if "prefix" in fmt:
        nb_dir = os.path.dirname(nb_file) + os.path.sep
        if not os.path.isdir(nb_dir):
            if log is not None:
                log(f"[jupytext] creating missing directory {nb_dir}")
            else:
                logging.log(logging.WARNING, "[jupytext] creating missing directory %s", nb_dir)
            os.makedirs(nb_dir)

