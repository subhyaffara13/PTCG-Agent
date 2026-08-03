import sys

def _c_compile(cfile, outputfilename, include_dirs, libraries,
               library_dirs):
    link_extra = []
    if sys.platform == 'win32':
        compile_extra = ["/we4013"]
        link_extra.append('/DEBUG')  # generate .pdb file
    elif sys.platform.startswith('linux'):
        compile_extra = [
            "-O0", "-g", "-Werror=implicit-function-declaration", "-fPIC"]
    else:
        compile_extra = []

    return build(
        cfile, outputfilename,
        compile_extra, link_extra,
        include_dirs, libraries, library_dirs)

