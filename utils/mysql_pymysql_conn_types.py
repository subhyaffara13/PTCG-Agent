
def mysql_pymysql_conn_types(mysql_pymysql_engine_types):
    with mysql_pymysql_engine_types.connect() as conn:
        yield conn

