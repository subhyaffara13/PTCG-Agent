
def update_from_first_child(tgt, src):
    first_child = next(iter(src.get_children()), None)
    if first_child is not None:
        tgt.update_from(first_child)

