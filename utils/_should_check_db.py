
def _should_check_db(
    key: str, last_db_access_time: LimitedSizeOrderedDict, db_cache_expiry: int
) -> bool:
    """
    Prevent calling db repeatedly for items that don't exist in the db.
    """
    current_time = time.time()
    # if key doesn't exist in last_db_access_time -> check db
    if key not in last_db_access_time:
        return True
    elif (
        last_db_access_time[key][0] is not None
    ):  # check db for non-null values (for refresh operations)
        return True
    elif last_db_access_time[key][0] is None:
        if current_time - last_db_access_time[key] >= db_cache_expiry:
            return True
    return False

