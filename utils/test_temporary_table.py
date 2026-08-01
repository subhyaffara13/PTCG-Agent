
def test_temporary_table(conn, request):
    if conn == "sqlite_str":
        pytest.skip("test does not work with str connection")

    conn = request.getfixturevalue(conn)

    from sqlalchemy import (
        Column,
        Integer,
        Unicode,
        select,
    )
    from sqlalchemy.orm import (
        Session,
        declarative_base,
    )

    test_data = "Hello, World!"
    expected = DataFrame({"spam": [test_data]})
    Base = declarative_base()

    class Temporary(Base):
        __tablename__ = "temp_test"
        __table_args__ = {"prefixes": ["TEMPORARY"]}
        id = Column(Integer, primary_key=True)
        spam = Column(Unicode(30), nullable=False)

    with Session(conn) as session:
        with session.begin():
            conn = session.connection()
            Temporary.__table__.create(conn)
            session.add(Temporary(spam=test_data))
            session.flush()
            df = sql.read_sql_query(sql=select(Temporary.spam), con=conn)
    tm.assert_frame_equal(df, expected)

