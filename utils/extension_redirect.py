import os
import sys

def extension_redirect(mod, path):
    """
    Tests will fail to tear down an extension module if it's been imported.

    Before importing, copy the file to a temporary directory that won't
    be cleaned up. Yield the new path.
    """
    if platform.system() != "Windows" and sys.platform != "cygwin":
        yield path
        return
    with import_helper.DirsOnSysPath(path):
        spec = importlib.util.find_spec(mod)
    filename = os.path.basename(spec.origin)
    trash_dir = tempfile.mkdtemp(prefix='deleteme')
    dest = os.path.join(trash_dir, os.path.basename(filename))
    shutil.copy(spec.origin, dest)
    yield trash_dir

