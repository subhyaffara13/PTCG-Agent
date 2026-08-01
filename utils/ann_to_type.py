
def ann_to_type(ann, loc, rcb=None):
    the_type = try_ann_to_type(ann, loc, rcb)
    if the_type is not None:
        return the_type
    raise ValueError(f"Unknown type annotation: '{ann}' at {loc.highlight()}")

