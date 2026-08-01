
def remove_handles(text):
    """
    Remove Twitter username handles from text.
    """
    pattern = regex.compile(
        r"(?<![A-Za-z0-9_!@#\$%&*])@(([A-Za-z0-9_]){20}(?!@))|(?<![A-Za-z0-9_!@#\$%&*])@(([A-Za-z0-9_]){1,19})(?![A-Za-z0-9_]*@)"
    )
    # Substitute handles with ' ' to ensure that text on either side of removed handles are tokenized correctly
    return pattern.sub(" ", text)

