
def write_result(res):
    """A callback for completed jobs. Inserts and writes a calculated result
     to file."""
    index, set_key, result_dict = res
    res_dict[set_key].insert(index, result_dict)
    write_data()

