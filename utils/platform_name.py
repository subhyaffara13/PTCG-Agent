
def platform_name():
    return "_".join(
        [
            str(pandas.__version__),
            str(pl.machine()),
            str(pl.system().lower()),
            str(pl.python_version()),
        ]
    )

