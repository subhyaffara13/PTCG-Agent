
def print_out(*args):
    if get_rank() == 0:
        print(*args)

