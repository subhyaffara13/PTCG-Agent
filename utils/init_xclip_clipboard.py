import subprocess

def init_xclip_clipboard():
    DEFAULT_SELECTION = "c"
    PRIMARY_SELECTION = "p"

    def copy_xclip(text, primary=False):
        text = _stringifyText(text)  # Converts non-str values to str.
        selection = DEFAULT_SELECTION
        if primary:
            selection = PRIMARY_SELECTION
        with subprocess.Popen(
            ["xclip", "-selection", selection], stdin=subprocess.PIPE, close_fds=True
        ) as p:
            p.communicate(input=text.encode(ENCODING))

    def paste_xclip(primary=False):
        selection = DEFAULT_SELECTION
        if primary:
            selection = PRIMARY_SELECTION
        with subprocess.Popen(
            ["xclip", "-selection", selection, "-o"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
        ) as p:
            stdout = p.communicate()[0]
        # Intentionally ignore extraneous output on stderr when clipboard is empty
        return stdout.decode(ENCODING)

    return copy_xclip, paste_xclip

