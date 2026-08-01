
def get_usedict(block):
    usedict = {}
    if 'parent_block' in block:
        usedict = get_usedict(block['parent_block'])
    if 'use' in block:
        usedict.update(block['use'])
    return usedict

