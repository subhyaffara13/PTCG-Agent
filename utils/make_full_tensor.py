
def make_full_tensor(dtensor_input):
    """wrapper function to support DTensor.full_tensor"""
    return redistribute(
        dtensor_input, dtensor_input.device_mesh, placements=None, shard_order=()
    ).to_local()

