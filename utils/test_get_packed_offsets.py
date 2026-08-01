
def test_get_packed_offsets(widths, total, sep, mode):
    # Check a (rather arbitrary) set of parameters due to successive similar
    # issue tickets (at least #10476 and #10784) related to corner cases
    # triggered inside this function when calling higher-level functions
    # (e.g. `Axes.legend`).
    # These are just some additional smoke tests. The output is untested.
    _get_packed_offsets(widths, total, sep, mode=mode)

