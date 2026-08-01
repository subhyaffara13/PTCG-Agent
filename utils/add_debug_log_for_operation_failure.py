
def add_debug_log_for_operation_failure(connection: "AbstractConnection"):
    logger.debug(
        f"Operation failed, "
        f"with connection: {connection}, details: {connection.extract_connection_details() if connection else 'no connection'}",
    )

