import time
from typing import Any

def test_torch_performance(
    args: argparse.Namespace,
    model: GPT2LMHeadModel | T5ForConditionalGeneration,
    input_ids: torch.Tensor,
    attention_mask: torch.Tensor,
    eos_token_id: int,
    pad_token_id: int,
    bad_words_ids: list[list[int]],
) -> dict[str, Any]:
    """Test PyTorch performance of text generation.

    Args:
        args (argparse.Namespace): arguments parsed from command line
        model (Union[GPT2LMHeadModel, T5ForConditionalGeneration]): PyTorch model
        input_ids (torch.Tensor): input_ids
        attention_mask (torch.Tensor): Attention mask
        eos_token_id (int): EOS token ID
        pad_token_id (int): Padding token ID
        bad_words_ids (List[List[int]]): Words shall not be generated.

    Raises:
        RuntimeError: PyTorch with CUDA is not available for --use_gpu

    Returns:
        Dict[str, Any]: A dictionary with string with metric name, and value can be integer or string.
    """
    if args.use_gpu and not torch.cuda.is_available():
        raise RuntimeError("Please install PyTorch with Cuda for testing gpu performance.")

    if args.precision == Precision.FLOAT16.value:
        model.half()

    device = torch.device("cuda:0" if args.use_gpu else "cpu")
    model.to(device)

    torch.set_grad_enabled(False)
    input_ids = input_ids.to(device)
    attention_mask = attention_mask.to(device)

    torch_latency = []
    for _ in range(args.total_runs):
        start = time.time()
        _ = model.generate(
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
        torch_latency.append(time.time() - start)
    batch_size = input_ids.shape[0]
    from benchmark_helper import get_latency_result  # noqa: PLC0415

    return get_latency_result(torch_latency, batch_size)

