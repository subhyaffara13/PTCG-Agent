
def _import(module, reload=False):
    """
    Creates a global translation dictionary for module.

    The argument module has to be one of the following strings: "math","cmath"
    "mpmath", "numpy", "sympy", "tensorflow", "jax".
    These dictionaries map names of Python functions to their equivalent in
    other modules.
    """
    try:
        namespace, namespace_default, translations, import_commands = MODULES[
            module]
    except KeyError:
        raise NameError(
            "'%s' module cannot be used for lambdification" % module)

    # Clear namespace or exit
    if namespace != namespace_default:
        # The namespace was already generated, don't do it again if not forced.
        if reload:
            namespace.clear()
            namespace.update(namespace_default)
        else:
            return

    for import_command in import_commands:
        if import_command.startswith('import_module'):
            module = eval(import_command)

            if module is not None:
                namespace.update(module.__dict__)
                continue
        else:
            try:
                exec(import_command, {}, namespace)
                continue
            except ImportError:
                pass

        raise ImportError(
            "Cannot import '%s' with '%s' command" % (module, import_command))

    # Add translated names to namespace
    for sympyname, translation in translations.items():
        namespace[sympyname] = namespace[translation]

    # For computing the modulus of a SymPy expression we use the builtin abs
    # function, instead of the previously used fabs function for all
    # translation modules. This is because the fabs function in the math
    # module does not accept complex valued arguments. (see issue 9474). The
    # only exception, where we don't use the builtin abs function is the
    # mpmath translation module, because mpmath.fabs returns mpf objects in
    # contrast to abs().
    if 'Abs' not in namespace:
        namespace['Abs'] = abs

