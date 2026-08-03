import os
from pathlib import Path


def convert_generation_model(
    args: argparse.Namespace,
    generation_type: GenerationType = GenerationType.BEAMSEARCH,
):
    """Convert model according to command line arguments.

    Args:
        args (argparse.Namespace): arguments parsed from command line
    """
    is_gpt2: bool = args.model_type == "gpt2"
    is_beamsearch: bool = generation_type == GenerationType.BEAMSEARCH
    is_greedysearch: bool = generation_type == GenerationType.GREEDYSEARCH
    is_sampling: bool = generation_type == GenerationType.SAMPLING
    past_present_share_buffer: bool = args.past_present_share_buffer

    logger.info(f"**** past_present_share_buffer={past_present_share_buffer}")
    if len(args.op_block_list) == 1 and args.op_block_list[0] == "auto":
        if is_gpt2 and args.precision == Precision.FLOAT16.value:
            args.op_block_list = [
                "Add",
                "LayerNormalization",
                "SkipLayerNormalization",
                "FastGelu",
            ]
            logger.info(f"**** Setting op_block_list to {args.op_block_list}")
            logger.info("**** use --op_block_list if you want to override the block operator list.")
        else:
            args.op_block_list = []

    if is_greedysearch or is_sampling:
        if not is_gpt2:
            raise NotImplementedError("Currently only gpt2 with greedy search/sampling is supported")
        if args.output_sequences_scores:
            raise NotImplementedError("output_sequences_scores currently is not supported in greedy search/sampling")
        if args.output_token_scores:
            raise NotImplementedError("output_token_scores currently is not supported in greedy search/sampling")

    # For BeamSearch, sharing buffers for past and present states is only supported
    # when using `use_decoder_masked_attention`
    if past_present_share_buffer and is_beamsearch and not args.use_decoder_masked_attention:
        raise ValueError(
            "`use_decoder_masked_attention` MUST be turned on to use `past_present_share_buffer` in case of BeamSearch"
        )

    # For any kind of sampling, using decoder masked multihead attention is only supported
    # when using `past_present_share_buffer`
    if args.use_decoder_masked_attention and not past_present_share_buffer:
        raise ValueError("`past_present_share_buffer` MUST be turned on to use `use_decoder_masked_attention`")

    # For any kind of sampling, using decoder masked multihead attention is only supported
    # on GPUs
    if args.use_decoder_masked_attention and not args.use_gpu:
        raise ValueError("`use_decoder_masked_attention` option is only supported on GPUs")

    if is_gpt2:
        if args.decoder_onnx and os.path.exists(args.decoder_onnx):
            logger.info(f"skip convert_to_onnx since path existed: {args.decoder_onnx}")
        else:
            if not args.decoder_onnx:
                onnx_filename = f"{args.model_name_or_path}_past_{args.precision}.onnx"
                args.decoder_onnx = Path(Path(args.output).parent, onnx_filename).as_posix()

            logger.info(f"Convert GPT model {args.model_name_or_path} to onnx {args.decoder_onnx} ...")
            gpt2_to_onnx(args)
    else:  # t5 or mt5
        if args.decoder_onnx and args.encoder_decoder_init_onnx:
            logger.info(
                f"skip convert_to_onnx since paths specified: {args.decoder_onnx} and {args.encoder_decoder_init_onnx}"
            )
        else:
            logger.info(f"Convert model {args.model_name_or_path} to onnx ...")
            t5_to_onnx(args)

    # We only want to pad the logits MatMul weight in the decoder for fp16 models.
    # The inherent assumption is that fp16 models run on GPU for which all
    # dims need to be a multiple of 8 to leverage tensor cores.
    # NOTE: We currently only support padding the MatMul logits weight for GPT2 GreedySearch/BeamSearch.
    # This can be expanded to other models/decoding strategies later
    logits_matmul_weight_padded = False
    if (
        not args.disable_pad_vocab_size
        and args.precision == Precision.FLOAT16.value
        and is_gpt2
        and (is_beamsearch or is_greedysearch or is_sampling)
    ):
        logger.info(
            f"Pad logits MatMul weights for optimal MatMul perf in fp16 on {args.decoder_onnx}. "
            "The file will be overwritten."
        )
        logits_matmul_weight_padded = pad_weights_of_logits_matmul(args.decoder_onnx, args.use_external_data_format)
        if not logits_matmul_weight_padded:
            logger.warning(
                "Tried and failed to pad logits MatMul weights. Performance may be sub-optimal for this MatMul"
            )

    gpt2_init_decoder_generated = False
    gpt2_init_decoder_onnx_path = None
    if (
        not args.disable_separate_gpt2_decoder_for_init_run
        and is_gpt2
        and (is_beamsearch or is_greedysearch or is_sampling)
    ):
        logger.info(f"Creating an initial run GPT2 decoder from {args.decoder_onnx}. ")

        gpt2_init_decoder_onnx_filename = f"gpt2_init_past_{args.precision}.onnx"

        gpt2_init_decoder_onnx_path = Path(Path(args.output).parent, gpt2_init_decoder_onnx_filename).as_posix()

        gpt2_init_decoder_generated = generate_gpt2_init_decoder(
            args.decoder_onnx,
            gpt2_init_decoder_onnx_path,
            args.use_external_data_format,
        )

        if not gpt2_init_decoder_generated:
            logger.warning(
                "Tried and failed to generate the init decoder GPT2 model. "
                "Performance may be sub-optimal for the initial decoding run"
            )

        # Update the graph input shapes for the non-initial decoder model to account
        # for the fact that the sequence length will always be 1
        if gpt2_init_decoder_generated and not update_input_shapes_for_gpt2_decoder_model(
            args.decoder_onnx, args.use_external_data_format
        ):
            # Can't proceed further - better to raise an exception
            raise ValueError("Could not update the input shapes for the non-initial decoder subgraph.")

    # If the user explicitly requests running shape inference or if we padded/mutated
    # weight(s)/input shape(s) in the decoder, we want to run shape inference to capture the new
    # shapes
    if logits_matmul_weight_padded or args.run_shape_inference or gpt2_init_decoder_generated:
        logger.info(f"Run symbolic shape inference on {args.decoder_onnx}. The file will be overwritten.")
        shape_inference(args.decoder_onnx, args.use_external_data_format)
        if gpt2_init_decoder_generated:
            logger.info(f"Run symbolic shape inference on {gpt2_init_decoder_onnx_path}. The file will be overwritten.")
            shape_inference(gpt2_init_decoder_onnx_path, args.use_external_data_format)

    if is_gpt2:
        config = GPT2Config.from_pretrained(args.model_name_or_path, cache_dir=args.cache_dir)
    elif args.model_type == "t5":
        config = T5Config.from_pretrained(args.model_name_or_path, cache_dir=args.cache_dir)
    else:
        config = MT5Config.from_pretrained(args.model_name_or_path, cache_dir=args.cache_dir)

    if args.verbose:
        logger.info(f"Config={config}")

    eos_token_id = config.eos_token_id
    pad_token_id = config.eos_token_id if is_gpt2 else config.pad_token_id
    vocab_size = config.vocab_size

    # if vocab_size is given in parameters use that.
    if args.vocab_size != -1:
        vocab_size = args.vocab_size

    if args.eos_token_id != -1:
        eos_token_id = args.eos_token_id
    if args.pad_token_id != -1:
        pad_token_id = args.pad_token_id

    decoder_model = onnx.load_model(args.decoder_onnx, load_external_data=True)
    decoder_model.graph.name = f"{args.model_type} decoder"

    gpt2_init_decoder_model = None
    if args.model_type == "gpt2":
        verify_gpt2_subgraph(decoder_model.graph, args.precision)

        # If we generated the init decoder model, verify that as well
        if gpt2_init_decoder_generated:
            gpt2_init_decoder_model = onnx.load_model(gpt2_init_decoder_onnx_path, load_external_data=True)
            gpt2_init_decoder_model.graph.name = f"{args.model_type} init decoder"
            verify_gpt2_subgraph(gpt2_init_decoder_model.graph, args.precision)
    else:
        verify_t5_decoder_subgraph(decoder_model.graph, args.precision)

    inputs = None
    if is_beamsearch:
        inputs = [
            "input_ids",
            "max_length",
            "min_length",
            "num_beams",
            "num_return_sequences",
            "length_penalty",
            "repetition_penalty",
        ]
    elif is_greedysearch or is_sampling:
        inputs = [
            "input_ids",
            "max_length",
            "min_length",
            "repetition_penalty",
        ]

    if args.vocab_mask:
        inputs.append("vocab_mask")
    else:
        inputs.append("")

    if args.prefix_vocab_mask:
        inputs.append("prefix_vocab_mask")
    else:
        inputs.append("")

    if args.custom_attention_mask:
        inputs.append("attention_mask")
    else:
        inputs.append("")

    if is_sampling:
        if args.custom and args.presence_mask:
            inputs.append("presence_mask")
        else:
            inputs.append("")

        if args.seed:
            inputs.append("seed")

    outputs = ["sequences"]
    if args.output_sequences_scores:
        outputs.append("sequences_scores")

    if args.output_token_scores:
        assert args.output_sequences_scores, "--output_token_scores requires --output_sequences_scores"
        outputs.append("scores")

    node = None
    if is_beamsearch:
        node = onnx.helper.make_node(
            "BeamSearch",
            inputs=inputs,
            outputs=outputs,
            name=f"BeamSearch_{args.model_type}",
        )
    elif is_greedysearch:
        node = onnx.helper.make_node(
            "GreedySearch",
            inputs=inputs,
            outputs=outputs,
            name=f"GreedySearch_{args.model_type}",
        )
    elif is_sampling:
        node = onnx.helper.make_node(
            "Sampling",
            inputs=inputs,
            outputs=outputs,
            name=f"Sampling_{args.model_type}",
        )

    node.domain = "com.microsoft"

    attr_to_extend = None
    if is_beamsearch:
        attr_to_extend = [
            onnx.helper.make_attribute("eos_token_id", eos_token_id),
            onnx.helper.make_attribute("pad_token_id", pad_token_id),
            onnx.helper.make_attribute("no_repeat_ngram_size", args.no_repeat_ngram_size),
            onnx.helper.make_attribute("early_stopping", 1 if args.early_stopping else 0),
            onnx.helper.make_attribute("model_type", 0 if args.model_type == "gpt2" else 1),
        ]
    elif is_greedysearch:
        attr_to_extend = [
            onnx.helper.make_attribute("eos_token_id", eos_token_id),
            onnx.helper.make_attribute("pad_token_id", pad_token_id),
            onnx.helper.make_attribute("model_type", 0 if args.model_type == "gpt2" else 1),
            onnx.helper.make_attribute("no_repeat_ngram_size", args.no_repeat_ngram_size),
        ]
    elif is_sampling:
        attr_to_extend = [
            onnx.helper.make_attribute("eos_token_id", eos_token_id),
            onnx.helper.make_attribute("pad_token_id", pad_token_id),
            onnx.helper.make_attribute("model_type", 0 if args.model_type == "gpt2" else 1),
            onnx.helper.make_attribute("no_repeat_ngram_size", args.no_repeat_ngram_size),
            onnx.helper.make_attribute("temperature", args.temperature),
            onnx.helper.make_attribute("top_p", args.top_p),
            onnx.helper.make_attribute("filter_value", args.filter_value),
            onnx.helper.make_attribute("min_tokens_to_keep", args.min_tokens_to_keep),
            onnx.helper.make_attribute("custom", args.custom),
            onnx.helper.make_attribute("presence_penalty", args.presence_penalty),
        ]

    # Explicitly pass in the vocab size via an attribute
    if logits_matmul_weight_padded:
        attr_to_extend.extend([onnx.helper.make_attribute("vocab_size", vocab_size)])

    node.attribute.extend(attr_to_extend)

    initializers = []

    if args.model_type in ["t5", "mt5"]:
        if args.run_shape_inference:
            logger.info(f"Symbolic shape inference on {args.encoder_decoder_init_onnx}. The file will be overwritten.")
            shape_inference(args.encoder_decoder_init_onnx, args.use_external_data_format)
        encoder_model = onnx.load_model(args.encoder_decoder_init_onnx, load_external_data=True)
        suffix = "encoder" if len(encoder_model.graph.input) == 2 else "encoder and decoder init"
        encoder_model.graph.name = f"{args.model_type} {suffix}"
        verify_t5_encoder_decoder_init_subgraph(encoder_model.graph, args.precision)

        make_dim_proto_numeric_t5(encoder_model, config)
        make_dim_proto_numeric_t5(decoder_model, config)

        # Update decoder subgraph in preparation to use past present share buffer
        if past_present_share_buffer:
            if not args.use_decoder_masked_attention:
                raise ValueError("past_present_share_buffer is only supported with use_decoder_masked_attention")

            logger.info(
                "*****update t5 decoder subgraph to share past/present buffer and use decoder_masked_multihead_attention*****"
            )
            if update_decoder_subgraph_share_buffer_and_use_decoder_masked_mha(decoder_model.graph):
                logger.info("*****update t5 decoder subgraph successfully!!!*****")
            else:
                logger.info("*****DecoderMaskedMultiHeadAttention is not applied to T5 decoder*****")

            if pack_qkv_for_decoder_masked_mha(decoder_model):
                logger.info("*****pack qkv for decoder masked mha successfully!!!*****")
            else:
                logger.info("*****pack qkv for decoder masked mha failed!!!*****")

        if not args.disable_shared_initializers:
            # Unique shared initializers from the decoder and decoder_init could reduce memory usage in inference.
            initializers = get_shared_initializers(encoder_model, decoder_model)
            logger.info(
                f"{len(initializers)} shared initializers ({[i.name for i in initializers]}) in encoder and decoder subgraphs are moved to the main graph"
            )

            # TODO(tianleiwu): investigate the following which causes error in inference
            # Move initializer from subgraph to main graph could reduce memory usage in inference.
            # moved_initializers = move_initializers(encoder_model.graph)
            # logger.info(
            #     f"{len(moved_initializers)} initializers ({[i.name for i in moved_initializers]}) from the encoder are moved to the main graph"
            # )
            # initializers.extend(moved_initializers)

        assert config.decoder_start_token_id >= 0, "decoder_start_token_id should be >= 0"

        node.attribute.extend(
            [
                onnx.helper.make_attribute("encoder", encoder_model.graph),
                onnx.helper.make_attribute("decoder", decoder_model.graph),
                onnx.helper.make_attribute("decoder_start_token_id", config.decoder_start_token_id),
            ]
        )
    else:
        if gpt2_init_decoder_generated:
            # Move shared initializers (shared between init decoder and decoder models) to the main
            # graph and remove them from these models
            if not args.disable_shared_initializers:
                # Unique shared initializers from the decoder and decoder_init could reduce memory usage in inference.
                initializers = get_shared_initializers(gpt2_init_decoder_model, decoder_model)
                logger.info(
                    f"{len(initializers)} shared initializers ({[i.name for i in initializers]}) in decoder and init decoder subgraphs are moved to the main graph"
                )

            # Update init decoder subgraph in preparation to use past present share buffer
            if past_present_share_buffer:
                logger.info("*****update init decoder subgraph to make past and present share buffer******************")
                update_decoder_subgraph_past_present_share_buffer(gpt2_init_decoder_model.graph)

            # Update init decoder subgraph in preparation to use DecoderMaskedSelfAttention
            # NOTE: Even if we will not use DecoderMaskedSelfAttention in the init decoder subgraph
            # it makes the runtime changes cleaner if we keep both the init decoder and decoder subgraphs
            # same in terms of the subgraph inputs.
            if args.use_decoder_masked_attention and not update_decoder_subgraph_use_decoder_masked_attention(
                gpt2_init_decoder_model.graph, is_beamsearch, False
            ):
                raise ValueError("Could not update the init decoder subgraph to use DecoderMaskedSelfAttention")

            node.attribute.append(onnx.helper.make_attribute("init_decoder", gpt2_init_decoder_model.graph))
        else:
            # Move initializer from subgraph to main graph could reduce memory usage in inference.
            initializers = move_initializers(decoder_model.graph)
            logger.info(f"{len(initializers)} initializers from the decoder are moved to the main graph")

        # Update decoder subgraph in preparation to use past present share buffer
        if past_present_share_buffer:
            logger.info("*****update decoder subgraph to make past and present share buffer******************")
            update_decoder_subgraph_past_present_share_buffer(decoder_model.graph)

        # Update decoder subgraph in preparation to use DecoderMaskedSelfAttention
        if args.use_decoder_masked_attention and not update_decoder_subgraph_use_decoder_masked_attention(
            decoder_model.graph, is_beamsearch, True
        ):
            raise ValueError("Could not update the decoder subgraph to use DecoderMaskedSelfAttention")

        node.attribute.append(onnx.helper.make_attribute("decoder", decoder_model.graph))

    # graph inputs
    input_ids = onnx.helper.make_tensor_value_info("input_ids", TensorProto.INT32, ["batch_size", "sequence_length"])
    max_length = onnx.helper.make_tensor_value_info("max_length", TensorProto.INT32, [1])
    min_length = onnx.helper.make_tensor_value_info("min_length", TensorProto.INT32, [1])
    num_beams = onnx.helper.make_tensor_value_info("num_beams", TensorProto.INT32, [1])
    num_return_sequences = onnx.helper.make_tensor_value_info("num_return_sequences", TensorProto.INT32, [1])
    length_penalty = onnx.helper.make_tensor_value_info("length_penalty", TensorProto.FLOAT, [1])
    repetition_penalty = onnx.helper.make_tensor_value_info("repetition_penalty", TensorProto.FLOAT, [1])

    graph_inputs = None
    if is_beamsearch:
        graph_inputs = [
            input_ids,
            max_length,
            min_length,
            num_beams,
            num_return_sequences,
            length_penalty,
            repetition_penalty,
        ]
    elif is_greedysearch or is_sampling:
        graph_inputs = [
            input_ids,
            max_length,
            min_length,
            repetition_penalty,
        ]

    if args.vocab_mask:
        vocab_mask = onnx.helper.make_tensor_value_info("vocab_mask", TensorProto.INT32, [vocab_size])
        graph_inputs.append(vocab_mask)

    if args.prefix_vocab_mask:
        prefix_vocab_mask = onnx.helper.make_tensor_value_info(
            "prefix_vocab_mask", TensorProto.INT32, ["batch_size", vocab_size]
        )
        graph_inputs.append(prefix_vocab_mask)

    if args.custom_attention_mask:
        attention_mask = onnx.helper.make_tensor_value_info(
            "attention_mask", TensorProto.INT32, ["batch_size", "sequence_length"]
        )
        graph_inputs.append(attention_mask)

    if args.custom and args.presence_mask:
        presence_mask = onnx.helper.make_tensor_value_info(
            "presence_mask", TensorProto.INT32, ["batch_size", vocab_size]
        )
        graph_inputs.append(presence_mask)

    if is_sampling and args.seed:
        seed = onnx.helper.make_tensor_value_info("seed", TensorProto.INT32, [1])
        graph_inputs.append(seed)

    # graph outputs
    sequences = None
    if is_beamsearch:
        sequences = onnx.helper.make_tensor_value_info(
            "sequences",
            TensorProto.INT32,
            ["batch_size", "num_return_sequences", "max_length"],
        )
    elif is_greedysearch or is_sampling:
        sequences = onnx.helper.make_tensor_value_info(
            "sequences",
            TensorProto.INT32,
            ["batch_size", "max_length"],
        )

    graph_outputs = [sequences]

    if args.output_sequences_scores:
        sequences_scores = onnx.helper.make_tensor_value_info(
            "sequences_scores",
            TensorProto.FLOAT,
            ["batch_size", "num_return_sequences"],
        )
        graph_outputs.append(sequences_scores)

    if args.output_token_scores:
        scores = onnx.helper.make_tensor_value_info(
            "scores",
            TensorProto.FLOAT,
            ["max_length - sequence_length", "batch_size", "num_beams", vocab_size],
        )
        graph_outputs.append(scores)

    new_graph = onnx.helper.make_graph(
        [node],
        (f"{args.model_type} beam search" if not is_greedysearch else f"{args.model_type} greedy search"),
        graph_inputs,
        graph_outputs,
        initializers,
    )

    # Create the model
    new_model = onnx.helper.make_model(
        new_graph,
        producer_name="onnxruntime.transformers",
        opset_imports=decoder_model.opset_import,
    )

    # TODO(tianleiwu): move shared initializers from T5 encoder and decoder subgraphs to parent graph to save memory.
    if args.use_external_data_format:
        from packaging import version  # noqa: PLC0415

        if version.parse(onnx.__version__) < version.parse("1.12.0"):
            logger.warning("Require onnx >= 1.12 to save large (>2GB) model!")

        OnnxModel.save(
            new_model,
            args.output,
            save_as_external_data=True,
            all_tensors_to_one_file=True,
        )
    else:
        onnx.save(new_model, args.output)
    logger.info(f"model save to {args.output}")

