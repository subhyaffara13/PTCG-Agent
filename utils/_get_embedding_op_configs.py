
def _get_embedding_op_configs() -> list[BackendPatternConfig]:
    dtype_configs = [
        executorch_weight_only_quint8_dtype_config,
    ]
    embedding_op_configs = []
    for embedding_op, qat_embedding_op, ref_embedding_op in [
        (nn.Embedding, nnqat.Embedding, nnqr.Embedding),
        (nn.EmbeddingBag, nnqat.EmbeddingBag, nnqr.EmbeddingBag),
    ]:
        embedding_op_configs.append(
            BackendPatternConfig(embedding_op)
            .set_observation_type(
                ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT
            )  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_qat_module(qat_embedding_op)
            .set_root_module(embedding_op)
            .set_reference_quantized_module(ref_embedding_op)
        )
        # config for qat op
        embedding_op_configs.append(
            BackendPatternConfig(qat_embedding_op)
            .set_observation_type(
                ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT
            )  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(embedding_op)
            .set_reference_quantized_module(ref_embedding_op)
        )

        # config for functional embedding
        embedding_op_configs.append(
            BackendPatternConfig(torch.nn.functional.embedding)
            .set_observation_type(
                ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT
            )  # noqa: E131
            .set_dtype_configs(dtype_configs)
            ._set_input_type_to_index({"weight": 1})
        )
    return embedding_op_configs


def _get_embedding_op_configs(
    dtype_configs: list[DTypeConfig],
) -> list[BackendPatternConfig]:
    embedding_op_configs = []
    for embedding_op, qat_embedding_op, ref_embedding_op in [
        (nn.Embedding, nnqat.Embedding, nnqr.Embedding),
        (nn.EmbeddingBag, nnqat.EmbeddingBag, nnqr.EmbeddingBag),
    ]:
        embedding_op_configs.append(
            BackendPatternConfig(embedding_op)
            .set_observation_type(
                ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT
            )  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_qat_module(qat_embedding_op)
            .set_root_module(embedding_op)
            .set_reference_quantized_module(ref_embedding_op)
        )

        # config for qat op
        embedding_op_configs.append(
            BackendPatternConfig(qat_embedding_op)
            .set_observation_type(
                ObservationType.OUTPUT_USE_DIFFERENT_OBSERVER_AS_INPUT
            )  # noqa: E131
            .set_dtype_configs(dtype_configs)
            .set_root_module(embedding_op)
            .set_reference_quantized_module(ref_embedding_op)
        )
    return embedding_op_configs

