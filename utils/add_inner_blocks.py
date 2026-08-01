
def add_inner_blocks(blocks):
    '''Process a list of blocks by adding all closures and inner classes as
    top-level blocks.
    '''
    new_blocks = []
    all_blocks = blocks[:]
    while all_blocks:
        block = all_blocks.pop()
        new_blocks.append(block)
        for inner_block in ('closures', 'inner_classes'):
            for i_block in getattr(block, inner_block, ()):
                named = i_block._replace(name=block.name + '.' + i_block.name)
                all_blocks.append(named)
                for meth in getattr(named, 'methods', ()):
                    m_named = meth._replace(classname=named.name)
                    all_blocks.append(m_named)
    return new_blocks

