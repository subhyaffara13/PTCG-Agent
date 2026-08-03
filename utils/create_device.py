import sys

def create_device(interface=None, lazy_init: bool = False):
    if sys.platform == "win32" or interface is None:
        return c10d.ProcessGroupGloo.create_device(
            hostname="127.0.0.1", lazy_init=lazy_init
        )
    else:
        return c10d.ProcessGroupGloo.create_device(
            interface=interface, lazy_init=lazy_init
        )

