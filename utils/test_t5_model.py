import os
import time
from pathlib import Path


def test_t5_model(args: argparse.Namespace, sentences: list[str] | None = None):
    """Test T5 or MT5 model

    Args:
        args (argparse.Namespace): arguments parsed from command line
        sentences (Optional[List[str]], optional): input text. Defaults to None.

    Returns:
        Union[Dict[str, Any], None]: A dictionary with string with metric name, and value can be integer or string.
    """
    assert args.model_type in ["t5", "mt5"]

    if args.prefix_vocab_mask:
        logger.debug("Skipping parity test as prefix vocab mask is not implemented by Hugging Face")
        return None

    tokenizer = T5Tokenizer.from_pretrained(args.model_name_or_path, cache_dir=args.cache_dir)
    tokenizer.padding_side = "left"

    if args.model_type == "t5":
        model = T5ForConditionalGeneration.from_pretrained(
            args.model_name_or_path,
            cache_dir=args.cache_dir,
        )
    else:
        model = MT5ForConditionalGeneration.from_pretrained(
            args.model_name_or_path,
            cache_dir=args.cache_dir,
        )

    # Use different length sentences to test batching
    if sentences is None:
        sentences = [
            "translate English to French: The product is released",
            "summarize: research continues to show that pets bring real health benefits to their owners. Having a dog around can lead to lower levels of stress for both adults and kids.",
            # "summarize: I enjoy walking in the park. It makes my mind feel calm and refreshed. "
            # + "I enjoy looking at the trees, flowers, and wildlife around me, and listening to sound from natural.",
        ]

    inputs = tokenizer(sentences, return_tensors="pt", padding=True)
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    bad_words = "walk in park"
    bad_words_ids = tokenizer.encode(bad_words)[:-1]  # exclude the last token (EOS)
    bad_words_ids = [[word_id] for word_id in bad_words_ids]  # Convert to list of list
    if args.vocab_mask:
        logger.debug("bad_words_ids", bad_words_ids)  # noqa: PLE1205
    else:
        bad_words_ids = []

    config = model.config
    eos_token_id = config.eos_token_id
    pad_token_id = config.pad_token_id
    vocab_size = config.vocab_size
    logger.debug(f"eos_token_id:{eos_token_id}, pad_token_id:{pad_token_id}, vocab_size:{vocab_size}")

    torch_decoded_sequences = []
    if not args.disable_parity:
        print("-" * 50)
        print("Test PyTorch model and beam search with huggingface transformers...")
        beam_outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=args.max_length,
            min_length=args.min_length,
            num_beams=args.num_beams,
            early_stopping=args.early_stopping,
            no_repeat_ngram_size=args.no_repeat_ngram_size,
            eos_token_id=eos_token_id,
            pad_token_id=pad_token_id,
            num_return_sequences=args.num_return_sequences,
            length_penalty=args.length_penalty,
            repetition_penalty=args.repetition_penalty,
            bad_words_ids=bad_words_ids if bad_words_ids else None,
            return_dict_in_generate=True,
            output_scores=args.output_sequences_scores or args.output_token_scores,
        )

        print("input_ids", input_ids)
        print("huggingface transformers outputs:")
        print("sequences", beam_outputs.sequences)
        if args.output_sequences_scores:
            print("sequences_scores", beam_outputs.sequences_scores)
        if args.output_token_scores:
            print("scores", beam_outputs.scores)
        for i, sequence in enumerate(beam_outputs.sequences):
            decoded_sequence = tokenizer.decode(sequence, skip_special_tokens=True)
            torch_decoded_sequences.append(decoded_sequence)
            print(f"{i}: {decoded_sequence}")

    print("-" * 50)
    print("Testing beam search with onnxruntime...")

    vocab_mask = np.ones((vocab_size), dtype=np.int32)
    if args.vocab_mask:
        for bad_word_id in bad_words_ids:
            vocab_mask[bad_word_id] = 0

    inputs = {
        "input_ids": input_ids.cpu().numpy().astype(np.int32),
        "max_length": np.array([args.max_length], dtype=np.int32),
        "min_length": np.array([args.min_length], dtype=np.int32),
        "num_beams": np.array([args.num_beams], dtype=np.int32),
        "num_return_sequences": np.array([args.num_return_sequences], dtype=np.int32),
        "length_penalty": np.array([args.length_penalty], dtype=np.float32),
        "repetition_penalty": np.array([args.repetition_penalty], dtype=np.float32),
    }

    if args.vocab_mask:
        inputs["vocab_mask"] = vocab_mask

    if args.custom_attention_mask:
        inputs["attention_mask"] = create_attention_mask(input_ids, pad_token_id)

    if args.save_test_data:
        test_data_dir = Path(args.output).parent.as_posix()
        logger.debug("test_data_dir", test_data_dir)  # noqa: PLE1205
        from bert_test_data import output_test_data  # noqa: PLC0415

        all_inputs = [inputs]
        for i, inputs in enumerate(all_inputs):
            dir = os.path.join(test_data_dir, "test_data_set_" + str(i))
            output_test_data(dir, inputs)

    logger.debug("ORT inputs", inputs)  # noqa: PLE1205

    ort_session = create_ort_session(args.output, args.use_gpu, args.use_sln_strict_mode)

    # Test performance
    latency = []
    for _ in range(args.total_runs):
        start = time.time()
        result = ort_session.run(None, inputs)
        latency.append(time.time() - start)
    batch_size = input_ids.shape[0]
    from benchmark_helper import get_latency_result  # noqa: PLC0415

    output = get_latency_result(latency, batch_size)

    print("ORT outputs:")
    sequences = result[0]
    print("sequences", sequences)
    if args.output_sequences_scores:
        print("sequences_scores", result[1])
    if args.output_token_scores:
        print("scores", result[2])

    (batch_size, num_sequences, max_length) = sequences.shape
    ort_decoded_sequences = []
    for i in range(batch_size):
        for j in range(num_sequences):
            decoded_sequence = tokenizer.decode(sequences[i][j], skip_special_tokens=True)
            ort_decoded_sequences.append(decoded_sequence)
            print(f"batch {i} sequence {j}: {decoded_sequence}")

    if not args.disable_parity:
        torch_sequences = beam_outputs.sequences.reshape(batch_size, args.num_return_sequences, -1)
        ort_sequences = torch.LongTensor(sequences)
        print("-" * 50)
        print("Torch Sequences:")
        print(torch_sequences)
        print(torch_decoded_sequences)
        print("-" * 50)
        print("ORT Sequences:")
        print(ort_sequences)
        print(ort_decoded_sequences)
        print("-" * 50)
        # Compare the generated text instead of word IDs since ORT pads to max sequence length but Torch not.
        is_same = torch_decoded_sequences == ort_decoded_sequences
        print("Torch and ORT result is ", "same" if is_same else "different")
        output["parity"] = is_same

    if args.torch_performance:
        torch_latency_output = test_torch_performance(
            args,
            model,
            input_ids,
            attention_mask,
            eos_token_id,
            pad_token_id,
            bad_words_ids,
        )
        print("Torch Latency", torch_latency_output)

    print("ORT", output)
    return output

