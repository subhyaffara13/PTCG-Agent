
def build_sphinx_html(source_dir, doctree_dir, html_dir, extra_args=None):
    # Build the pages with warnings turned into errors
    extra_args = [] if extra_args is None else extra_args
    cmd = [sys.executable, '-msphinx', '-W', '-b', 'html',
           '-d', str(doctree_dir), str(source_dir), str(html_dir), *extra_args]
    # On CI, gcov emits warnings (due to agg headers being included with the
    # same name in multiple extension modules -- but we don't care about their
    # coverage anyways); hide them using GCOV_ERROR_FILE.
    proc = subprocess_run_for_testing(
        cmd, capture_output=True, text=True,
        env={**os.environ, "MPLBACKEND": "", "GCOV_ERROR_FILE": os.devnull}
    )
    out = proc.stdout
    err = proc.stderr

    assert proc.returncode == 0, \
        f"sphinx build failed with stdout:\n{out}\nstderr:\n{err}\n"
    if err:
        pytest.fail(f"sphinx build emitted the following warnings:\n{err}")

    assert html_dir.is_dir()

