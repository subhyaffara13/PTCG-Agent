
def get_queen_dir(diff):
    dx, dy = diff
    assert dx == 0 or dy == 0 or abs(dx) == abs(dy)
    magnitude = max(abs(dx), abs(dy)) - 1

    assert magnitude < 8 and magnitude >= 0
    counter = 0
    for x in range(-1, 1 + 1):
        for y in range(-1, 1 + 1):
            if x == 0 and y == 0:
                continue
            if x == sign(dx) and y == sign(dy):
                return magnitude, counter
            counter += 1
    assert False, "bad queen move inputted"

