
def _hash_ranks_to_str(ranks: list[int]) -> str:
    rank_join: str = "_".join(map(str, ranks))
    # In case there is already a PG with the same rank composition
    unique_str = "_".join([rank_join, str(len(_world.pg_names))])
    return hashlib.sha1(bytes(unique_str, "utf-8"), usedforsecurity=False).hexdigest()

