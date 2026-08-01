
def test_row_object_is_named_tuple(sqlite_engine):
    conn = sqlite_engine
    # GH 40682
    # Test for the is_named_tuple() function
    # Placed here due to its usage of sqlalchemy

    from sqlalchemy import (
        Column,
        Integer,
        String,
    )
    from sqlalchemy.orm import (
        declarative_base,
        sessionmaker,
    )

    BaseModel = declarative_base()

    class Test(BaseModel):
        __tablename__ = "test_frame"
        id = Column(Integer, primary_key=True)
        string_column = Column(String(50))

    with conn.begin():
        BaseModel.metadata.create_all(conn)
    Session = sessionmaker(bind=conn)
    with Session() as session:
        df = DataFrame({"id": [0, 1], "string_column": ["hello", "world"]})
        assert (
            df.to_sql(name="test_frame", con=conn, index=False, if_exists="replace")
            == 2
        )
        session.commit()
        test_query = session.query(Test.id, Test.string_column)
        df = DataFrame(test_query)

    assert list(df.columns) == ["id", "string_column"]

