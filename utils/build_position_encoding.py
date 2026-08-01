
def build_position_encoding(config):
    if config.position_embedding_type == "sine":
        position_embedding = GroundingDinoSinePositionEmbedding(config)
    elif config.position_embedding_type == "learned":
        position_embedding = GroundingDinoLearnedPositionEmbedding(config)
    else:
        raise ValueError(f"Not supported {config.position_embedding_type}")

    return position_embedding


def build_position_encoding(config):
    if config.position_embedding_type == "sine":
        position_embedding = MMGroundingDinoSinePositionEmbedding(config)
    elif config.position_embedding_type == "learned":
        position_embedding = MMGroundingDinoLearnedPositionEmbedding(config)
    else:
        raise ValueError(f"Not supported {config.position_embedding_type}")

    return position_embedding


def build_position_encoding(
    position_encoding_type,
    out_channels=None,
    project_pos_dim=-1,
    trainable_position_encoding_kwargs=None,
    fourier_position_encoding_kwargs=None,
):
    """
    Builds the position encoding.

    Args:
    - out_channels: refers to the number of channels of the position encodings.
    - project_pos_dim: if specified, will project the position encodings to this dimension.

    """

    if position_encoding_type == "trainable":
        if not trainable_position_encoding_kwargs:
            raise ValueError("Make sure to pass trainable_position_encoding_kwargs")
        output_pos_enc = PerceiverTrainablePositionEncoding(**trainable_position_encoding_kwargs)
    elif position_encoding_type == "fourier":
        # We don't use the index_dims argument, as this is only known during the forward pass
        if not fourier_position_encoding_kwargs:
            raise ValueError("Make sure to pass fourier_position_encoding_kwargs")
        output_pos_enc = PerceiverFourierPositionEncoding(**fourier_position_encoding_kwargs)
    else:
        raise ValueError(f"Unknown position encoding type: {position_encoding_type}.")

    # Optionally, project the position encoding to a target dimension:
    positions_projection = nn.Linear(out_channels, project_pos_dim) if project_pos_dim > 0 else nn.Identity()

    return output_pos_enc, positions_projection


def build_position_encoding(config):
    n_steps = config.d_model // 2
    if config.position_embedding_type == "sine":
        # TODO find a better way of exposing other arguments
        position_embedding = TableTransformerSinePositionEmbedding(n_steps, normalize=True)
    elif config.position_embedding_type == "learned":
        position_embedding = TableTransformerLearnedPositionEmbedding(n_steps)
    else:
        raise ValueError(f"Not supported {config.position_embedding_type}")

    return position_embedding

