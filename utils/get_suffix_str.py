
def get_suffix_str(number):
    # Find the index of the appropriate suffix based on the number of digits
    # with some additional overflow.
    # i.e. 1.01B should be displayed as 1001M, not 1.001B
    index = max(0, min(len(suffixes) - 1, (len(str(number)) - 2) // 3))
    return suffixes[index]

