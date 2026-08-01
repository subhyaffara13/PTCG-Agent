
def _void_scalar_to_string(x, is_repr=True):
    """
    Implements the repr for structured-void scalars. It is called from the
    scalartypes.c.src code, and is placed here because it uses the elementwise
    formatters defined above.
    """
    options = format_options.get().copy()

    if options["legacy"] <= 125:
        return StructuredVoidFormat.from_data(array(x), **options)(x)

    if options.get('formatter') is None:
        options['formatter'] = {}
    options['formatter'].setdefault('float_kind', str)
    val_repr = StructuredVoidFormat.from_data(array(x), **options)(x)
    if not is_repr:
        return val_repr
    cls = type(x)
    cls_fqn = cls.__module__.replace("numpy", "np") + "." + cls.__name__
    void_dtype = np.dtype((np.void, x.dtype))
    return f"{cls_fqn}({val_repr}, dtype={void_dtype!s})"

