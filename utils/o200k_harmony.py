
def o200k_harmony():
    base_enc = o200k_base()
    name = "o200k_harmony"
    pat_str = base_enc["pat_str"]
    mergeable_ranks = base_enc["mergeable_ranks"]
    special_tokens = {
        **base_enc["special_tokens"],
        "<|startoftext|>": 199998,
        "<|endoftext|>": 199999,
        "<|reserved_200000|>": 200000,
        "<|reserved_200001|>": 200001,
        "<|return|>": 200002,
        "<|constrain|>": 200003,
        "<|reserved_200004|>": 200004,
        "<|channel|>": 200005,
        "<|start|>": 200006,
        "<|end|>": 200007,
        "<|message|>": 200008,
        "<|reserved_200009|>": 200009,
        "<|reserved_200010|>": 200010,
        "<|reserved_200011|>": 200011,
        "<|call|>": 200012,
    } | {f"<|reserved_{i}|>": i for i in range(200013, 201088)}
    return {
        "name": name,
        "pat_str": pat_str,
        "mergeable_ranks": mergeable_ranks,
        "special_tokens": special_tokens,
    }

