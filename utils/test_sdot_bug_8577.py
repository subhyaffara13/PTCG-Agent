
def test_sdot_bug_8577():
    # Regression test that loading certain other libraries does not
    # result to wrong results in float32 linear algebra.
    #
    # There's a bug gh-8577 on OSX that can trigger this, and perhaps
    # there are also other situations in which it occurs.
    #
    # Do the check in a separate process.

    bad_libs = ['PyQt5.QtWidgets', 'IPython']

    template = textwrap.dedent("""
    import sys
    {before}
    try:
        import {bad_lib}
    except ImportError:
        sys.exit(0)
    {after}
    x = np.ones(2, dtype=np.float32)
    sys.exit(0 if np.allclose(x.dot(x), 2.0) else 1)
    """)

    for bad_lib in bad_libs:
        code = template.format(before="import numpy as np", after="",
                               bad_lib=bad_lib)
        run_subprocess([sys.executable, "-c", code])

        # Swapped import order
        code = template.format(after="import numpy as np", before="",
                               bad_lib=bad_lib)
        run_subprocess([sys.executable, "-c", code])

