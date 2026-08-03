import sys

def print_paired_paths(nb_file, fmt):
    """Display the paired paths for this notebook"""
    formats = get_formats_from_notebook_path(nb_file, fmt)
    if formats:
        for path, _ in paired_paths(nb_file, fmt, formats):
            if path != nb_file:
                sys.stdout.write(path + "\n")

