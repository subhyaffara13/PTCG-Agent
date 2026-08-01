
def hashing(query, key, num_hash, hash_len):
    if len(query.size()) != 3:
        raise ValueError("Query has incorrect size.")
    if len(key.size()) != 3:
        raise ValueError("Key has incorrect size.")

    rmat = torch.randn(query.size(0), query.size(2), num_hash * hash_len, device=query.device)
    raise_pow = 2 ** torch.arange(hash_len, device=query.device)

    query_projection = torch.matmul(query, rmat).reshape(query.size(0), query.size(1), num_hash, hash_len)
    key_projection = torch.matmul(key, rmat).reshape(key.size(0), key.size(1), num_hash, hash_len)
    query_binary = (query_projection > 0).int()
    key_binary = (key_projection > 0).int()
    query_hash = torch.sum(query_binary * raise_pow, dim=-1)
    query_hash = torch.sum(key_binary * raise_pow, dim=-1)

    return query_hash.int(), query_hash.int()

