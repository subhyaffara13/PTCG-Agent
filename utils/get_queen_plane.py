
def get_queen_plane(diff):
    NUM_COUNTERS = 8
    mag, counter = get_queen_dir(diff)
    return mag * NUM_COUNTERS + counter

