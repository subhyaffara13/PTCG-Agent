
def next_power_of_two(n):
    if n <= 0:
        return 1
    return 2 ** math.ceil(math.log2(n))

