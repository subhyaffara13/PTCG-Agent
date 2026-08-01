
def mysql_pymysql_conn(mysql_pymysql_engine):
    with mysql_pymysql_engine.connect() as conn:
        yield conn

