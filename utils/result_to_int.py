
def result_to_int(result_str):
    if result_str == "1-0":
        return 1
    elif result_str == "0-1":
        return -1
    elif result_str == "1/2-1/2":
        return 0
    else:
        assert False, "bad result"

