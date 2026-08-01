
def sqlite_str(temp_file):
    pytest.importorskip("sqlalchemy")
    return f"sqlite:///{temp_file}"

