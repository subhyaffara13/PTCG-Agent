
def is_line_commented(line: bytes) -> bool:
    """Checks if a `# symbol that is not part of a string was found in line."""
    comment_idx = line.find(b"#")
    if comment_idx == -1:
        return False
    if comment_part_of_string(line, comment_idx):
        return is_line_commented(line[:comment_idx] + line[comment_idx + 1 :])
    return True

