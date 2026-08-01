
def _block_format_index(index):
    """
    Convert a list of indices ``[0, 1, 2]`` into ``"arrays[0][1][2]"``.
    """
    idx_str = ''.join(f'[{i}]' for i in index if i is not None)
    return 'arrays' + idx_str

