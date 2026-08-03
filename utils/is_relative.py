import os
import sys

def is_relative(modname: str, from_file: str) -> bool:
    """Return true if the given module name is relative to the given
    file name.

    :param modname: name of the module we are interested in

    :param from_file:
      path of the module from which modname has been imported

    :return:
      true if the module has been imported relatively to `from_file`
    """
    if not os.path.isdir(from_file):
        from_file = os.path.dirname(from_file)
    if from_file in sys.path:
        return False
    return bool(
        importlib.machinery.PathFinder.find_spec(
            modname.split(".", maxsplit=1)[0], [from_file]
        )
    )

