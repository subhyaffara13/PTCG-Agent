
def get_outfnames(fname: str, split: bool) -> list[str]:
    suffixes = ["_train", "_valid"] if split else [""]
    i = 0
    while True:
        index_suffix = f" ({i})" if i > 0 else ""
        candidate_fnames = [f"{os.path.splitext(fname)[0]}_prepared{suffix}{index_suffix}.jsonl" for suffix in suffixes]
        if not any(os.path.isfile(f) for f in candidate_fnames):
            return candidate_fnames
        i += 1

