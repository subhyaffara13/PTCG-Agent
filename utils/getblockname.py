
def getblockname(block, unknown='unknown'):
    if 'name' in block:
        return block['name']
    return unknown

