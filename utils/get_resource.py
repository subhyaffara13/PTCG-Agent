
def getResource(identifier, pkgname=__name__):
    """
    Acquire a readable object for a given package name and identifier.
    An IOError will be raised if the resource can not be found.

    For example:
        mydata = getResource('mypkgdata.jpg').read()

    Note that the package name must be fully qualified, if given, such
    that it would be found in sys.modules.

    In some cases, getResource will return a real file object.  In that
    case, it may be useful to use its name attribute to get the path
    rather than use it as a file-like object.  For example, you may
    be handing data off to a C API.
    """

    # When pyinstaller (or similar tools) are used, resource_exists may raise
    # NotImplemented error
    try:
        if resource_exists(pkgname, identifier):
            return resource_stream(pkgname, identifier)
    except NotImplementedError:
        pass

    mod = sys.modules[pkgname]
    path_to_file = getattr(mod, "__file__", None)
    if path_to_file is None:
        raise OSError(f"{repr(mod)} has no __file__!")
    path = os.path.join(os.path.dirname(path_to_file), identifier)

    # pylint: disable=consider-using-with
    return open(os.path.normpath(path), "rb")


def get_resource(identifier, pkgname=__name__):

    mod = sys.modules[pkgname]
    fn = getattr(mod, '__file__', None)
    if fn is None:
        raise OSError("%r has no __file__!")
    path = os.path.join(os.path.dirname(fn), identifier)
    loader = getattr(mod, '__loader__', None)
    if loader is not None:
        try:
            data = loader.get_data(path)
        except (OSError, AttributeError):
            pass
        else:
            return StringIO(data.decode('utf-8'))
    return open(os.path.normpath(path), 'rb')

