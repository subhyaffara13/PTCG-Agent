
def _op_runtime_estimate_mult(snode):
    # Apply multipliers for faster experimentation.
    # TODO(ivankobzarev): Remove after confirmation that runtime estimations are correct.
    if contains_collective(snode):
        return config_comms.reorder_sink_runtime_estimations_comm_mult

    return config_comms.reorder_sink_runtime_estimations_non_comm_mult

