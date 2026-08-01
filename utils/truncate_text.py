
def truncate_text(txt, max_length=100):
    return textwrap.shorten(
        text=txt, width=max_length, placeholder="...", break_long_words=True
    )

