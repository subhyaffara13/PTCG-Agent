
def _vectorize_statistic(statistic):
    """Vectorize an n-sample statistic"""
    # This is a little cleaner than np.nditer at the expense of some data
    # copying: concatenate samples together, then use np.apply_along_axis
    def stat_nd(*data, axis=0):
        lengths = [sample.shape[axis] for sample in data]
        split_indices = np.cumsum(lengths)[:-1]
        z = _broadcast_concatenate(data, axis)

        # move working axis to position 0 so that new dimensions in the output
        # of `statistic` are _prepended_. ("This axis is removed, and replaced
        # with new dimensions...")
        z = np.moveaxis(z, axis, 0)

        def stat_1d(z):
            data = np.split(z, split_indices)
            return statistic(*data)

        return np.apply_along_axis(stat_1d, 0, z)[()]
    return stat_nd

