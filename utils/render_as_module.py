
def render_as_module(definitions, name, declarations=(), printer_settings=None):
    """ Creates a ``Module`` instance and renders it as a string.

    This generates Fortran source code for a module with the correct ``use`` statements.

    Parameters
    ==========

    definitions : iterable
        Passed to :class:`sympy.codegen.fnodes.Module`.
    name : str
        Passed to :class:`sympy.codegen.fnodes.Module`.
    declarations : iterable
        Passed to :class:`sympy.codegen.fnodes.Module`. It will be extended with
        use statements, 'implicit none' and public list generated from ``definitions``.
    printer_settings : dict
        Passed to ``FCodePrinter`` (default: ``{'standard': 2003, 'source_format': 'free'}``).

    """
    printer_settings = printer_settings or {'standard': 2003, 'source_format': 'free'}
    printer = FCodePrinter(printer_settings)
    dummy = Dummy()
    if isinstance(definitions, Module):
        raise ValueError("This function expects to construct a module on its own.")
    mod = Module(name, chain(declarations, [dummy]), definitions)
    fstr = printer.doprint(mod)
    module_use_str = '   %s\n' % '   \n'.join(['use %s, only: %s' % (k, ', '.join(v)) for
                                                k, v in printer.module_uses.items()])
    module_use_str += '   implicit none\n'
    module_use_str += '   private\n'
    module_use_str += '   public %s\n' % ', '.join([str(node.name) for node in definitions if getattr(node, 'name', None)])
    return fstr.replace(printer.doprint(dummy), module_use_str)


def render_as_module(content, standard='python3'):
    """Renders Python code as a module (with the required imports).

    Parameters
    ==========

    standard :
        See the parameter ``standard`` in
        :meth:`sympy.printing.pycode.pycode`
    """

    printer = PythonCodePrinter({'standard':standard})
    pystr = printer.doprint(content)
    if printer._settings['fully_qualified_modules']:
        module_imports_str = '\n'.join('import %s' % k for k in printer.module_imports)
    else:
        module_imports_str = '\n'.join(['from %s import %s' % (k, ', '.join(v)) for
                                        k, v in printer.module_imports.items()])
    return module_imports_str + '\n\n' + pystr

