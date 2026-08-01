
def _has_tex_package(package):
    try:
        mpl.dviread.find_tex_file(f"{package}.sty")
        return True
    except (FileNotFoundError, OSError):
        return False

