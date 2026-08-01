
def test_get_schema2(test_frame1):
    # without providing a connection object (available for backwards comp)
    create_sql = sql.get_schema(test_frame1, "test")
    assert "CREATE" in create_sql

