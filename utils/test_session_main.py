import os

def test_session_main(refimported):
    """test dump/load_module() for __main__, both in this process and in a subprocess"""
    extra_objects = {}
    if refimported:
        # Test unpickleable imported object in main.
        from sys import flags
        extra_objects['flags'] = flags

    with TestNamespace(**extra_objects) as ns:
        try:
            # Test session loading in a new session.
            dill.dump_module(session_file % refimported, refimported=refimported)
            from dill.tests.__main__ import python, shell, sp
            error = sp.call([python, __file__, '--child', str(refimported)], shell=shell)
            if error: sys.exit(error)
        finally:
            with suppress(OSError):
                os.remove(session_file % refimported)

        # Test session loading in the same session.
        session_buffer = BytesIO()
        dill.dump_module(session_buffer, refimported=refimported)
        session_buffer.seek(0)
        dill.load_module(session_buffer, module='__main__')
        ns.backup['_test_objects'](__main__, ns.backup, refimported)

