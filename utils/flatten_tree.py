
def flatten_tree(tree):
    """Flatten nested dicts and lists into a full list of paths"""
    output = set()
    for node, contents in tree.items():
        if isinstance(contents, dict):
            contents = flatten_tree(contents)

        for elem in contents:
            if isinstance(elem, dict):
                output |= {os.path.join(node, val) for val in flatten_tree(elem)}
            else:
                output.add(os.path.join(node, elem))
    return output

