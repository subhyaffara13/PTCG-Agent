
def makeSetup(**args):
    """Return distribution from 'setup(**args)', without executing commands"""

    distutils.core._setup_stop_after = "commandline"

    # Don't let system command line leak into tests!
    args.setdefault('script_args', ['install'])

    try:
        return setuptools.setup(**args)
    finally:
        distutils.core._setup_stop_after = None

