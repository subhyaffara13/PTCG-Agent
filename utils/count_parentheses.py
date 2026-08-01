
def count_parentheses(current_parentheses_count: int, token_text: str) -> int:
    """Count the number of parentheses."""
    if token_text in "([{":  # nosec
        return current_parentheses_count + 1
    elif token_text in "}])":  # nosec
        return current_parentheses_count - 1
    return current_parentheses_count

