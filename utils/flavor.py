
def flavor(conn_name):
    if "postgresql" in conn_name:
        return "postgresql"
    elif "sqlite" in conn_name:
        return "sqlite"
    elif "mysql" in conn_name:
        return "mysql"

    raise ValueError(f"unsupported connection: {conn_name}")

