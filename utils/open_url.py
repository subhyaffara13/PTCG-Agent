
def open_url(url: str, wait: bool = False, locate: bool = False) -> int:
    import subprocess

    def _unquote_file(url: str) -> str:
        from urllib.parse import unquote

        if url.startswith("file://"):
            url = unquote(url[7:])

        return url

    if sys.platform == "darwin":
        args = ["open"]
        if wait:
            args.append("-W")
        if locate:
            args.append("-R")
        args.append(_unquote_file(url))
        null = open("/dev/null", "w")
        try:
            return subprocess.Popen(args, stderr=null).wait()
        finally:
            null.close()
    elif WIN:
        if locate:
            url = _unquote_file(url)
            args = ["explorer", "/select,", url]
            try:
                return subprocess.call(args)
            except OSError:
                return 127
        else:
            try:
                os.startfile(url)  # type: ignore[attr-defined]
            except OSError:
                return 127
            return 0
    elif CYGWIN:
        if locate:
            url = _unquote_file(url)
            args = ["cygstart", os.path.dirname(url)]
        else:
            args = ["cygstart"]
            if wait:
                args.append("-w")
            args.append(url)
        try:
            return subprocess.call(args)
        except OSError:
            # Command not found
            return 127

    try:
        if locate:
            url = os.path.dirname(_unquote_file(url)) or "."
        else:
            url = _unquote_file(url)
        c = subprocess.Popen(["xdg-open", url])
        if wait:
            return c.wait()
        return 0
    except OSError:
        if url.startswith(("http://", "https://")) and not locate and not wait:
            import webbrowser

            webbrowser.open(url)
            return 0
        return 1

