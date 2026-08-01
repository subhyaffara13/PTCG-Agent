
def test_options_get_engine(fp, pa):
    assert isinstance(get_engine("pyarrow"), PyArrowImpl)
    assert isinstance(get_engine("fastparquet"), FastParquetImpl)

    with pd.option_context("io.parquet.engine", "pyarrow"):
        assert isinstance(get_engine("auto"), PyArrowImpl)
        assert isinstance(get_engine("pyarrow"), PyArrowImpl)
        assert isinstance(get_engine("fastparquet"), FastParquetImpl)

    with pd.option_context("io.parquet.engine", "fastparquet"):
        assert isinstance(get_engine("auto"), FastParquetImpl)
        assert isinstance(get_engine("pyarrow"), PyArrowImpl)
        assert isinstance(get_engine("fastparquet"), FastParquetImpl)

    with pd.option_context("io.parquet.engine", "auto"):
        assert isinstance(get_engine("auto"), PyArrowImpl)
        assert isinstance(get_engine("pyarrow"), PyArrowImpl)
        assert isinstance(get_engine("fastparquet"), FastParquetImpl)


def test_options_get_engine():
    pytest.importorskip("sqlalchemy")
    assert isinstance(get_engine("sqlalchemy"), SQLAlchemyEngine)

    with pd.option_context("io.sql.engine", "sqlalchemy"):
        assert isinstance(get_engine("auto"), SQLAlchemyEngine)
        assert isinstance(get_engine("sqlalchemy"), SQLAlchemyEngine)

    with pd.option_context("io.sql.engine", "auto"):
        assert isinstance(get_engine("auto"), SQLAlchemyEngine)
        assert isinstance(get_engine("sqlalchemy"), SQLAlchemyEngine)

