
def do_wordcount(s: str) -> int:
    """Count the words in that string."""
    return len(_word_re.findall(soft_str(s)))

