
def _table2():
    # If nested sqrt's are worse than un-evaluation
    # you can require q to be in (1, 2, 3, 4, 6, 12)
    # q <= 12, q=15, q=20, q=24, q=30, q=40, q=60, q=120 return
    # expressions with 2 or fewer sqrt nestings.
    return {
        12: (3, 4),
        20: (4, 5),
        30: (5, 6),
        15: (6, 10),
        24: (6, 8),
        40: (8, 10),
        60: (20, 30),
        120: (40, 60)
    }

