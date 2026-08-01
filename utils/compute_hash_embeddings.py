
def compute_hash_embeddings(
    local_encoder_tokens: torch.Tensor,
    local_encoder,
    encoder_hash_tok_embedding: nn.Embedding,
    encoder_hash_byte_group_nb_functions: int,
    encoder_hash_byte_group_size: list,
    encoder_hash_byte_group_vocab: int,
) -> torch.Tensor:
    """Compute token embeddings enhanced with hash-based embeddings."""
    # Available primes for hash functions
    primes = [
        1000000007,
        5915587277,
        1500450271,
        3267000013,
        5754853343,
        4093082899,
        9576890767,
        3628273133,
        2860486313,
        5463458053,
        3367900313,
    ]

    embeddings = local_encoder.embed_tokens(local_encoder_tokens)
    embedding_idx = 0
    for func_nb in range(encoder_hash_byte_group_nb_functions):
        prime = primes[func_nb % len(primes)]  # Cycle through primes if more functions than primes
        for group_size in encoder_hash_byte_group_size:
            hash_ids = byte_group_hash_function(local_encoder_tokens, group_size, prime, encoder_hash_byte_group_vocab)
            # Apply offset to get the correct slice of the fused embedding
            offset_hash_ids = hash_ids + embedding_idx * encoder_hash_byte_group_vocab
            embeddings += encoder_hash_tok_embedding(offset_hash_ids).to(embeddings.device)
            embedding_idx += 1

    return embeddings


def compute_hash_embeddings(
    local_encoder_tokens: torch.Tensor,
    local_encoder,
    encoder_hash_tok_embedding: nn.Embedding,
    encoder_hash_byte_group_nb_functions: int,
    encoder_hash_byte_group_size: list,
    encoder_hash_byte_group_vocab: int,
) -> torch.Tensor:
    """Compute token embeddings enhanced with hash-based embeddings."""
    # Available primes for hash functions
    primes = [
        1000000007,
        5915587277,
        1500450271,
        3267000013,
        5754853343,
        4093082899,
        9576890767,
        3628273133,
        2860486313,
        5463458053,
        3367900313,
    ]

    embeddings = local_encoder.embed_tokens(local_encoder_tokens)
    embedding_idx = 0
    for func_nb in range(encoder_hash_byte_group_nb_functions):
        prime = primes[func_nb % len(primes)]  # Cycle through primes if more functions than primes
        for group_size in encoder_hash_byte_group_size:
            hash_ids = byte_group_hash_function(local_encoder_tokens, group_size, prime, encoder_hash_byte_group_vocab)
            # Apply offset to get the correct slice of the fused embedding
            offset_hash_ids = hash_ids + embedding_idx * encoder_hash_byte_group_vocab
            embeddings += encoder_hash_tok_embedding(offset_hash_ids).to(embeddings.device)
            embedding_idx += 1

    return embeddings

