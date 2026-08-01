
def _merge_candidate_labels_text(text: list[str]) -> str:
    """
    Merge candidate labels text into a single string. Ensure all labels are lowercase.
    For example, ["A cat", "a dog"] -> "a cat. a dog."
    """
    labels = [t.strip().lower() for t in text]  # ensure lowercase
    merged_labels_str = ". ".join(labels) + "."  # join with dot and add a dot at the end
    return merged_labels_str

