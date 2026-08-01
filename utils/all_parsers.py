
def all_parsers(request):
    """
    Fixture all of the CSV parsers.
    """
    parser = request.param()
    if parser.engine == "pyarrow":
        pytest.importorskip("pyarrow", VERSIONS["pyarrow"])
        # Try finding a way to disable threads all together
        # for more stable CI runs
        import pyarrow

        pyarrow.set_cpu_count(1)
    return parser

