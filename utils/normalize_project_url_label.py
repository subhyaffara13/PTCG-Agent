
def normalize_project_url_label(label: str) -> str:
    # This logic is from PEP 753 (Well-known Project URLs in Metadata).
    chars_to_remove = string.punctuation + string.whitespace
    removal_map = str.maketrans("", "", chars_to_remove)
    return label.translate(removal_map).lower()

