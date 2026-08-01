
def partition_name(start: date) -> str:
    return f"{SPEND_LOGS_TABLE}_p{start.strftime('%Y%m%d')}"

