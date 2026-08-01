
def get_connection(redis_node: Redis, *args, **options) -> Connection:
    return redis_node.connection or redis_node.connection_pool.get_connection()

