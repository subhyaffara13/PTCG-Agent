
def VertGradientColumn(surf, topcolor, bottomcolor):
    "creates a new 3d vertical gradient array"
    topcolor = np.array(topcolor, copy=False)
    bottomcolor = np.array(bottomcolor, copy=False)
    diff = bottomcolor - topcolor
    width, height = surf.get_size()
    # create array from 0.0 to 1.0 triplets
    column = np.arange(height, dtype="float") / height
    column = np.repeat(column[:, np.newaxis], [3], 1)
    # create a single column of gradient
    column = topcolor + (diff * column).astype("int")
    # make the column a 3d image column by adding X
    column = column.astype("uint8")[np.newaxis, :, :]
    # 3d array into 2d array
    return pg.surfarray.map_array(surf, column)

