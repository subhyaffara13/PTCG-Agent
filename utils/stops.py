
def stops(support, count=10):
    a, b, c = support

    return (
        [a + (b - a) * i / count for i in range(count)]
        + [b + (c - b) * i / count for i in range(count)]
        + [c]
    )

