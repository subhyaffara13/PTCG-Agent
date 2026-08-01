
def distance_box(a, b, p, boxsize):
    diff = a - b
    diff[diff > 0.5 * boxsize] -= boxsize
    diff[diff < -0.5 * boxsize] += boxsize
    d = minkowski(diff, 0, p)
    return d

