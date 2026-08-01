
def tquery(query, con=None):
    """Replace removed sql.tquery function"""
    with sql.pandasSQL_builder(con) as pandas_sql:
        res = pandas_sql.execute(query).fetchall()
    return None if res is None else list(res)

