
def parse_client_info(value):
    """
    Parsing client-info in ACL Log in following format.
    "key1=value1 key2=value2 key3=value3"
    """
    client_info = {}
    for info in str_if_bytes(value).strip().split():
        key, value = info.split("=")
        client_info[key] = value

    # Those fields are defined as int in networking.c
    for int_key in {
        "id",
        "age",
        "idle",
        "db",
        "sub",
        "psub",
        "multi",
        "qbuf",
        "qbuf-free",
        "obl",
        "argv-mem",
        "oll",
        "omem",
        "tot-mem",
    }:
        if int_key in client_info:
            client_info[int_key] = int(client_info[int_key])
    return client_info

