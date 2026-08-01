
def get_knight_dir(diff):
    dx, dy = diff
    counter = 0
    for x in range(-2, 2 + 1):
        for y in range(-2, 2 + 1):
            if abs(x) + abs(y) == 3:
                if dx == x and dy == y:
                    return counter
                counter += 1
    assert False, "bad knight move inputted"

