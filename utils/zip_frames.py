
def zip_frames(frames: list[DataFrame], axis: AxisInt = 1) -> DataFrame:
    """
    take a list of frames, zip them together under the
    assumption that these all have the first frames' index/columns.

    Returns
    -------
    new_frame : DataFrame
    """
    if axis == 1:
        columns = frames[0].columns
        zipped = [f.loc[:, c] for c in columns for f in frames]
        return concat(zipped, axis=1)
    else:
        index = frames[0].index
        zipped = [f.loc[i, :] for i in index for f in frames]
        return DataFrame(zipped)

