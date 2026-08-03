import re

def notebooks_in_git_index(fmt):
    """Return the list of modified and deleted ipynb files in the git index that match the given format"""
    git_status = system("git", "status", "--porcelain")
    re_modified = re.compile(r"^[AM]+\s+(?P<name>.*)", re.MULTILINE)
    modified_files_in_git_index = re_modified.findall(git_status)
    files = []
    for nb_file in modified_files_in_git_index:
        if nb_file.startswith('"') and nb_file.endswith('"'):
            nb_file = nb_file[1:-1]
        try:
            base_path(nb_file, fmt)
            files.append(nb_file)
        except InconsistentPath:
            continue
    return files

