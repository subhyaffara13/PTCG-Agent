
def enabled():
    """
    Allow selection of distutils by environment variable.
    """
    which = os.environ.get('SETUPTOOLS_USE_DISTUTILS', 'local')
    if which == 'stdlib':
        import warnings

        warnings.warn(
            "Reliance on distutils from stdlib is deprecated. Users "
            "must rely on setuptools to provide the distutils module. "
            "Avoid importing distutils or import setuptools first, "
            "and avoid setting SETUPTOOLS_USE_DISTUTILS=stdlib. "
            f"Register concerns at {report_url}"
        )
    return which == 'local'


def enabled():
    """
    Only enabled for Python 3.9 framework homebrew builds
    except ensurepip and venv.
    """
    PY39 = (3, 9) < sys.version_info < (3, 10)
    framework = sys.platform == 'darwin' and sys._framework
    homebrew = "Cellar" in sysconfig.get_config_var('projectbase')
    venv = sys.prefix != sys.base_prefix
    ensurepip = os.environ.get("ENSUREPIP_OPTIONS")
    return PY39 and framework and homebrew and not venv and not ensurepip

