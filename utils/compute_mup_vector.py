
def compute_mup_vector(config):
    """
    Computes the MuP vector based on model configuration.

    FalconH1 applies different MuP multiplier for each dimension of the hidden states.
    The MuP vector is partitioned into chunks, and each chunk is multiplied with its
    corresponding projected dimension.

    Args:
        config: FalconH1Config object

    Returns:
        torch.Tensor: The computed MuP vector
    """
    # We'll need some values from the config to compute the vector dimensions
    intermediate_size = (
        config.mamba_d_ssm if config.mamba_d_ssm is not None else int(config.mamba_expand * config.hidden_size)
    )
    groups_time_state_size = config.mamba_n_groups * config.mamba_d_state
    num_heads = config.mamba_n_heads
    zxbcdt_multipliers = config.ssm_multipliers

    vector_shape = 2 * intermediate_size + 2 * groups_time_state_size + num_heads
    mup_vector = torch.ones(1, 1, vector_shape)

    # Apply multipliers to different sections of the vector
    mup_vector[:, :, :intermediate_size] *= zxbcdt_multipliers[0]
    mup_vector[:, :, intermediate_size : 2 * intermediate_size] *= zxbcdt_multipliers[1]
    mup_vector[:, :, 2 * intermediate_size : 2 * intermediate_size + groups_time_state_size] *= zxbcdt_multipliers[2]
    mup_vector[
        :, :, 2 * intermediate_size + groups_time_state_size : 2 * intermediate_size + 2 * groups_time_state_size
    ] *= zxbcdt_multipliers[3]
    mup_vector[:, :, 2 * intermediate_size + 2 * groups_time_state_size :] *= zxbcdt_multipliers[4]

    return mup_vector


def compute_mup_vector(config):
    """
    Computes the MuP vector based on model configuration.

    FalconH1 applies different MuP multiplier for each dimension of the hidden states.
    The MuP vector is partitioned into chunks, and each chunk is multiplied with its
    corresponding projected dimension.

    Args:
        config: FalconH1Config object

    Returns:
        torch.Tensor: The computed MuP vector
    """
    # We'll need some values from the config to compute the vector dimensions
    intermediate_size = (
        config.mamba_d_ssm if config.mamba_d_ssm is not None else int(config.mamba_expand * config.hidden_size)
    )
    groups_time_state_size = config.mamba_n_groups * config.mamba_d_state
    num_heads = config.mamba_n_heads
    zxbcdt_multipliers = config.ssm_multipliers

    vector_shape = 2 * intermediate_size + 2 * groups_time_state_size + num_heads
    mup_vector = torch.ones(1, 1, vector_shape)

    # Apply multipliers to different sections of the vector
    mup_vector[:, :, :intermediate_size] *= zxbcdt_multipliers[0]
    mup_vector[:, :, intermediate_size : 2 * intermediate_size] *= zxbcdt_multipliers[1]
    mup_vector[:, :, 2 * intermediate_size : 2 * intermediate_size + groups_time_state_size] *= zxbcdt_multipliers[2]
    mup_vector[
        :, :, 2 * intermediate_size + groups_time_state_size : 2 * intermediate_size + 2 * groups_time_state_size
    ] *= zxbcdt_multipliers[3]
    mup_vector[:, :, 2 * intermediate_size + 2 * groups_time_state_size :] *= zxbcdt_multipliers[4]

    return mup_vector

