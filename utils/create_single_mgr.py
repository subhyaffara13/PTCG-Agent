
def create_single_mgr(typestr, num_rows=None):
    if num_rows is None:
        num_rows = N

    return SingleBlockManager(
        create_block(typestr, placement=slice(0, num_rows), item_shape=()),
        Index(np.arange(num_rows)),
    )

