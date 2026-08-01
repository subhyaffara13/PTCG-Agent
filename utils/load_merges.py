
def load_merges(merges_file):
    """Loads a merges file into a list."""
    merges = []
    with open(merges_file, "r", encoding="utf-8") as reader:
        for line in reader:
            line = line.strip()
            if line and not line.startswith("#"):
                merges.append(tuple(line.split()))
    return merges

