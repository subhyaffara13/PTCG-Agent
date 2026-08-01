
def find_f2py_commands():
    if sys.platform == 'win32':
        exe_dir = dirname(sys.executable)
        if exe_dir.endswith('Scripts'):  # virtualenv
            return [os.path.join(exe_dir, 'f2py')]
        else:
            return [os.path.join(exe_dir, "Scripts", 'f2py')]
    else:
        # Three scripts are installed in Unix-like systems:
        # 'f2py', 'f2py{major}', and 'f2py{major.minor}'. For example,
        # if installed with python3.9 the scripts would be named
        # 'f2py', 'f2py3', and 'f2py3.9'.
        version = sys.version_info
        major = str(version.major)
        minor = str(version.minor)
        return ['f2py', 'f2py' + major, 'f2py' + major + '.' + minor]

