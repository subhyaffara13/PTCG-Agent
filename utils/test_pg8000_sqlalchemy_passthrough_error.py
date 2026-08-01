
def test_pg8000_sqlalchemy_passthrough_error(request):
    pytest.importorskip("sqlalchemy")
    # using driver that will not be installed on CI to trigger error
    # in sqlalchemy.create_engine -> test passing of this error to user
    db_uri = "postgresql+pg8000://user:pass@host/dbname"
    with pytest.raises(ImportError, match="pg8000"):
        sql.read_sql("select * from table", db_uri)

