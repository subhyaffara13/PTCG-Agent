
def handle_negative_axis(axis, rank):
    assert axis < rank and axis >= -rank
    return axis if axis >= 0 else rank + axis

