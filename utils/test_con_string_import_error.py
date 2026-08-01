
def test_con_string_import_error():
    conn = "mysql://root@localhost/pandas"
    msg = "Using URI string without sqlalchemy installed"
    with pytest.raises(ImportError, match=msg):
        sql.read_sql("SELECT * FROM iris", conn)

