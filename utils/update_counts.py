
def update_counts(s, counts):
    r"""Adds one to the counts of each appearance of characters in s,
        for characters in counts"""
    for char in s:
        if char in counts:
            counts[char] += 1

