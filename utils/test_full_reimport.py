
def test_full_reimport():
    # Reimporting numpy like this is not safe due to use of global C state,
    # and has unexpected side effects. Test that an ImportError is raised.
    # When all extension modules are isolated, this should test that clearing
    # sys.modules and reimporting numpy works without error.

    # Test within a new process, to ensure that we do not mess with the
    # global state during the test run (could lead to cryptic test failures).
    # This is generally unsafe, especially, since we also reload the C-modules.
    code = textwrap.dedent(r"""
        import sys
        import numpy as np

        for k in [k for k in sys.modules if k.startswith('numpy')]:
            del sys.modules[k]

        try:
            import numpy as np
        except ImportError as err:
            if str(err) != "cannot load module more than once per process":
                raise SystemExit(f"Unexpected ImportError: {err}")
        else:
            raise SystemExit("DID NOT RAISE ImportError")
        """)
    run_subprocess((sys.executable, '-c', code))

