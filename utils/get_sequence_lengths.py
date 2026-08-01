
def get_sequence_lengths(args: argparse.Namespace, config: AutoConfig):
    past_sequence_length, curr_sequence_length = (8, 1) if args.use_past_kv else (0, 8)
    max_sequence_length = config.max_position_embeddings
    return past_sequence_length, curr_sequence_length, max_sequence_length

