
def skip_if_no_pandas_parser(parser):
    if parser != "pandas":
        pytest.skip(f"cannot evaluate with parser={parser}")

