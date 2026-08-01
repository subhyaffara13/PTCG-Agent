
def mysql_pymysql_engine_iris(mysql_pymysql_engine, iris_path):
    create_and_load_iris(mysql_pymysql_engine, iris_path)
    create_and_load_iris_view(mysql_pymysql_engine)
    return mysql_pymysql_engine

