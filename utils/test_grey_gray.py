
def test_grey_gray():
    color_mapping = mcolors._colors_full_map
    for k in color_mapping.keys():
        if 'grey' in k:
            assert color_mapping[k] == color_mapping[k.replace('grey', 'gray')]
        if 'gray' in k:
            assert color_mapping[k] == color_mapping[k.replace('gray', 'grey')]

