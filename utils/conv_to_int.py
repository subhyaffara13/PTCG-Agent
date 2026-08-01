
def conv_to_int(num):
    if isinstance(num, float) and num.is_integer():
        return int(num)
    return num

