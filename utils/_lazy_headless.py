
def _lazy_headless():
    import os
    import sys

    backend, deps = sys.argv[1:]
    deps = deps.split(',')

    # make it look headless
    os.environ.pop('DISPLAY', None)
    os.environ.pop('WAYLAND_DISPLAY', None)
    for dep in deps:
        assert dep not in sys.modules

    # we should fast-track to Agg
    import matplotlib.pyplot as plt
    assert plt.get_backend() == 'agg'
    for dep in deps:
        assert dep not in sys.modules

    # make sure we really have dependencies installed
    for dep in deps:
        importlib.import_module(dep)
        assert dep in sys.modules

    # try to switch and make sure we fail with ImportError
    try:
        plt.switch_backend(backend)
    except ImportError:
        pass
    else:
        sys.exit(1)

