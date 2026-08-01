
def enable_automatic_int_sympification(shell):
    """
    Allow IPython to automatically convert integer literals to Integer.
    """
    import ast
    old_run_cell = shell.run_cell

    def my_run_cell(cell, *args, **kwargs):
        try:
            # Check the cell for syntax errors.  This way, the syntax error
            # will show the original input, not the transformed input.  The
            # downside here is that IPython magic like %timeit will not work
            # with transformed input (but on the other hand, IPython magic
            # that doesn't expect transformed input will continue to work).
            ast.parse(cell)
        except SyntaxError:
            pass
        else:
            cell = int_to_Integer(cell)
        return old_run_cell(cell, *args, **kwargs)

    shell.run_cell = my_run_cell

