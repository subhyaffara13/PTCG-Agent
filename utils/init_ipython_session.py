
def init_ipython_session(shell=None, argv=[], auto_symbols=False, auto_int_to_Integer=False):
    """Construct new IPython session. """
    import IPython

    if version_tuple(IPython.__version__) >= version_tuple('0.11'):
        if not shell:
            # use an app to parse the command line, and init config
            # IPython 1.0 deprecates the frontend module, so we import directly
            # from the terminal module to prevent a deprecation message from being
            # shown.
            if version_tuple(IPython.__version__) >= version_tuple('1.0'):
                from IPython.terminal import ipapp
            else:
                from IPython.frontend.terminal import ipapp
            app = ipapp.TerminalIPythonApp()

            # don't draw IPython banner during initialization:
            app.display_banner = False
            app.initialize(argv)

            shell = app.shell

        if auto_symbols:
            enable_automatic_symbols(shell)
        if auto_int_to_Integer:
            enable_automatic_int_sympification(shell)

        return shell
    else:
        from IPython.Shell import make_IPython
        return make_IPython(argv)

