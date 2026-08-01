
def battle_select(select_list: list[int]) -> dict:
    """Select option.

    Args:
        select_list:

    Returns:
        dict: Next observation.
    """
    if not isinstance(select_list, list) or not all(isinstance(i, int) for i in select_list):
        raise ValueError("select_list is not list[int]")
    arg = (ctypes.c_int * len(select_list))(*select_list)
    err = lib.Select(Battle.battle_ptr, arg, len(select_list))
    if err != 0:
        if err == 30:
            raise ValueError("battle_ptr broken.")
        else:
            raise IndexError()
    return _get_battle_data()

