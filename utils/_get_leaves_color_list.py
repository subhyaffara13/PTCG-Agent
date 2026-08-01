
def _get_leaves_color_list(R):
    leaves_color_list = [None] * len(R['leaves'])
    for link_x, link_y, link_color in zip(R['icoord'],
                                          R['dcoord'],
                                          R['color_list']):
        for (xi, yi) in zip(link_x, link_y):
            if yi == 0.0 and (xi % 5 == 0 and xi % 2 == 1):
                # if yi is 0.0 and xi is divisible by 5 and odd,
                # the point is a leaf
                # xi of leaves are      5, 15, 25, 35, ... (see `iv_ticks`)
                # index of leaves are   0,  1,  2,  3, ... as below
                leaf_index = (int(xi) - 5) // 10
                # each leaf has a same color of its link.
                leaves_color_list[leaf_index] = link_color
    return leaves_color_list

