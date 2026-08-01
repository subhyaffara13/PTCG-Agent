
def create_onnxruntime_input(vocab_size, batch_size, sequence_length, input_names, config, data_type=numpy.int64):
    if config.model_type in ["vit", "swin"]:
        input_ids = numpy.random.rand(batch_size, 3, config.image_size, config.image_size).astype(numpy.float32)
        inputs = {"pixel_values": input_ids}
        return inputs

    input_ids = numpy.random.randint(low=0, high=vocab_size - 1, size=(batch_size, sequence_length), dtype=data_type)
    inputs = {"input_ids": input_ids}

    if "attention_mask" in input_names:
        attention_mask = numpy.ones([batch_size, sequence_length], dtype=data_type)
        inputs["attention_mask"] = attention_mask

    if "token_type_ids" in input_names:
        segment_ids = numpy.zeros([batch_size, sequence_length], dtype=data_type)
        inputs["token_type_ids"] = segment_ids

    if config.is_encoder_decoder:
        inputs["decoder_input_ids"] = input_ids

    if isinstance(config, LxmertConfig):
        inputs["visual_feats"] = numpy.random.randn(1, 1, config.visual_feat_dim).astype(numpy.float32)
        inputs["visual_pos"] = numpy.random.randn(1, 1, config.visual_pos_dim).astype(numpy.float32)
    if isinstance(config, TransfoXLConfig):
        inputs["tf_transfo_xl_model/transformer/pos_emb/einsum/Einsum/inputs_1:0"] = numpy.zeros(
            [config.hidden_size], dtype=numpy.float32
        )
    return inputs

