
def _compose_deltas(deltas, deltas_name):
    """Takes a list of deltas matches (a dictionary) and a string (the expected delta list name),
    and processes its elements to compose a tuple of integers representing the deltas"""
    if deltas_name not in deltas:
        return None
    out_deltas = deltas.get(deltas_name)
    if out_deltas is not None and out_deltas.strip():
        elems = out_deltas.split(',')
    # Convert each element in the list elems to an integer 
    # after stripping whitespace and create a tuple from these integers.
    out_deltas_tuple = tuple(int(x.strip()) for x in elems)
    return out_deltas_tuple

