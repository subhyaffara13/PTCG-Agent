
def test_read_view_sqlite(sqlite_buildin):
    # GH 52969
    create_table = """
CREATE TABLE groups (
   group_id INTEGER,
   name TEXT
);
"""
    insert_into = """
INSERT INTO groups VALUES
    (1, 'name');
"""
    create_view = """
CREATE VIEW group_view
AS
SELECT * FROM groups;
"""
    sqlite_buildin.execute(create_table)
    sqlite_buildin.execute(insert_into)
    sqlite_buildin.execute(create_view)
    result = pd.read_sql("SELECT * FROM group_view", sqlite_buildin)
    expected = DataFrame({"group_id": [1], "name": "name"})
    tm.assert_frame_equal(result, expected)

