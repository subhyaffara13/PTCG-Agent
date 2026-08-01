
def get_elements(n):
    # dict is deterministic without difficulty of comparing numpy ints
    elements = {}
    for element in generate_random_token():
        if element not in elements:
            elements[element] = len(elements)
            if len(elements) >= n:
                break
    return list(elements.keys())

