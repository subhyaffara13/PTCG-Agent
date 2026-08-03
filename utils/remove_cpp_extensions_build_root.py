import os
import subprocess

def remove_cpp_extensions_build_root():
    """
    Removes the default root folder under which extensions are built.
    """
    default_build_root = cpp_extension.get_default_build_root()
    if os.path.exists(default_build_root):
        if IS_WINDOWS:
            # rmtree returns permission error: [WinError 5] Access is denied
            # on Windows, this is a workaround
            subprocess.run(["rm", "-rf", default_build_root], stdout=subprocess.PIPE)
        else:
            shutil.rmtree(default_build_root, ignore_errors=True)

