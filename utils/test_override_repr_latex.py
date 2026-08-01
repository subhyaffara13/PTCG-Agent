
def test_override_repr_latex():
    # Initialize and setup IPython session
    app = init_ipython_session()
    app.run_cell("import IPython")
    app.run_cell("ip = get_ipython()")
    app.run_cell("inst = ip.instance()")
    app.run_cell("format = inst.display_formatter.format")
    app.run_cell("inst.display_formatter.formatters['text/latex'].enabled = True")
    app.run_cell("from sympy import init_printing")
    app.run_cell("from sympy import Symbol")
    app.run_cell("init_printing(use_latex=True)")
    app.run_cell("""\
    class SymbolWithOverload(Symbol):
        def _repr_latex_(self):
            return r"Hello " + super()._repr_latex_() + " world"
    """)
    app.run_cell("a = format(SymbolWithOverload('s'))")

    if int(ipython.__version__.split(".")[0]) < 1:
        latex = app.user_ns['a']['text/latex']
    else:
        latex = app.user_ns['a'][0]['text/latex']
    assert latex == r'Hello $\displaystyle s$ world'

