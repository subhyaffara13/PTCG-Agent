
def mysql_pymysql_conn_iris(mysql_pymysql_engine_iris):
    with mysql_pymysql_engine_iris.connect() as conn:
        yield conn

