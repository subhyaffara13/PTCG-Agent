
def test_wrong_engine(engine_name):
    with pytest.raises(ValueError, match="Unknown engine "):
        DataFrame().apply(lambda x: x, engine=engine_name)

