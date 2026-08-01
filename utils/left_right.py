
def left_right():
    low, high, n = -1 << 10, 1 << 10, 1 << 20
    left = DataFrame(
        np.random.default_rng(2).integers(low, high, (n, 7)), columns=list("ABCDEFG")
    )
    left["left"] = left.sum(axis=1)
    right = left.sample(
        frac=1, random_state=np.random.default_rng(2), ignore_index=True
    )
    right.columns = [*right.columns[:-1].tolist(), "right"]
    right["right"] *= -1
    return left, right

