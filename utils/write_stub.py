
def write_stub(resource, pyfile) -> None:
    _stub_template = textwrap.dedent(
        """
        def __bootstrap__():
            global __bootstrap__, __loader__, __file__
            import sys, importlib.resources as irs, importlib.util
            with irs.as_file(irs.files(__name__).joinpath(%r)) as __file__:
                __loader__ = None; del __bootstrap__, __loader__
                spec = importlib.util.spec_from_file_location(__name__,__file__)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
        __bootstrap__()
        """
    ).lstrip()
    with open(pyfile, 'w', encoding="utf-8") as f:
        f.write(_stub_template % resource)

