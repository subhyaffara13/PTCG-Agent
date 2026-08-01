
def _transfer_ranges(fs, blocks, paths, starts, ends):
    # Use cat_ranges to gather the data byte_ranges
    ranges = (paths, starts, ends)
    for path, start, stop, data in zip(*ranges, fs.cat_ranges(*ranges)):
        blocks[path][(start, stop)] = data

