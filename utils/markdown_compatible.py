
def markdown_compatible(text: str) -> str:
    """
    Make text compatible with Markdown formatting.

    This function makes various text formatting adjustments to make it compatible with Markdown.

    Args:
        text (`str`):
            The input text to be made Markdown-compatible.

    Returns:
        `str`: The Markdown-compatible text.
    """
    # equation tag
    # Replace lines that start with a pattern like (decimal) \[some text\] with \[[some text] \tag{decimal}\].
    text = re.sub(r"^\(([\d.]+[a-zA-Z]?)\) \\\[(.+?)\\\]$", r"\[\2 \\tag{\1}\]", text, flags=re.MULTILINE)
    # Replace lines that start with a pattern like \[some text\] (decimal)  with \[[some text] \tag{decimal}\].
    text = re.sub(r"^\\\[(.+?)\\\] \(([\d.]+[a-zA-Z]?)\)$", r"\[\1 \\tag{\2}\]", text, flags=re.MULTILINE)
    # Replace lines that start with a pattern like \[some text\] (digits) \[another text\]  with \[[some text] \tag{digits}\] [another text].
    text = re.sub(
        r"^\\\[(.+?)\\\] \(([\d.]+[a-zA-Z]?)\) (\\\[.+?\\\])$",
        r"\[\1 \\tag{\2}\] \3",
        text,
        flags=re.MULTILINE,
    )
    # multi line
    text = text.replace(r"\. ", ". ")
    # bold formatting
    text = text.replace(r"\bm{", r"\mathbf{").replace(r"{\\bm ", r"\mathbf{")
    text = re.sub(r"\\mbox{ ?\\boldmath\$(.*?)\$}", r"\\mathbf{\1}", text)
    # Reformat urls (http, ftp and https only) to markdown [url](url) clickable format
    text = re.sub(
        r"((?:http|ftp|https):\/\/(?:[\w_-]+(?:(?:\.[\w_-]+)+))(?:[\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]))",
        r"[\1](\1)",
        text,
    )
    # algorithms
    text = re.sub(r"```\s*(.+?)\s*```", r"```\n\1\n```", text, flags=re.DOTALL)

    return text

