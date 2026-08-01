
def types_table_metadata(dialect: str):
    from sqlalchemy import (
        TEXT,
        Boolean,
        Column,
        DateTime,
        Float,
        Integer,
        MetaData,
        Table,
    )

    date_type = TEXT if dialect == "sqlite" else DateTime
    bool_type = Integer if dialect == "sqlite" else Boolean
    metadata = MetaData()
    types = Table(
        "types",
        metadata,
        Column("TextCol", TEXT),
        # error: Cannot infer type argument 1 of "Column"
        Column("DateCol", date_type),  # type: ignore[misc]
        Column("IntDateCol", Integer),
        Column("IntDateOnlyCol", Integer),
        Column("FloatCol", Float),
        Column("IntCol", Integer),
        # error: Cannot infer type argument 1 of "Column"
        Column("BoolCol", bool_type),  # type: ignore[misc]
        Column("IntColWithNull", Integer),
        # error: Cannot infer type argument 1 of "Column"
        Column("BoolColWithNull", bool_type),  # type: ignore[misc]
    )
    return types

