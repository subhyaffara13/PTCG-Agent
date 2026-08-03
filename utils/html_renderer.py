import os

def html_renderer():
    dir_path = os.path.dirname(__file__)
    htmlpath = os.path.join(dir_path, "visualizer", "default", "dist", "index.html")
    if os.path.exists(htmlpath):
        with open(htmlpath, encoding="utf-8") as f:
            return f.read()
    jspath = os.path.abspath(os.path.join(dir_path, "cabt.js"))
    if os.path.exists(jspath):
        with open(jspath, encoding="utf-8") as f:
            return f.read()
    return ""


def html_renderer():
    htmlpath = path.join(dirpath, "visualizer", "default", "dist", "index.html")
    if path.exists(htmlpath):
        with open(htmlpath, encoding="utf-8") as f:
            return f.read()
    jspath = path.abspath(path.join(dirpath, "connectx.js"))
    if path.exists(jspath):
        with open(jspath, encoding="utf-8") as f:
            return f.read()
    return ""


def html_renderer(env, mode):
    # In ipython/notebook mode, use the lightweight single-file JS renderer
    if mode == "ipython":
        js_path = path.abspath(path.join(dir_path, "crawl.js"))
        if path.exists(js_path):
            with open(js_path, encoding="utf-8") as js_file:
                return js_file.read()
    # Default: use the full Vite-built visualizer
    jspath = path.join(dir_path, "visualizer", "default", "dist", "index.html")
    if path.exists(jspath):
        with open(jspath, encoding="utf-8") as f:
            return f.read()
    # Fallback to single-file JS renderer
    js_path = path.abspath(path.join(dir_path, "crawl.js"))
    if path.exists(js_path):
        with open(js_path, encoding="utf-8") as js_file:
            return js_file.read()
    return ""


def html_renderer(env):
    try_get_video(env, keep_running=True)
    if not env.football_video_path:
        raise Exception("No video found. Was environment created with save_video enabled?")

    from base64 import b64encode

    from IPython.display import HTML, display

    video = open(env.football_video_path, "rb").read()
    env.football_video_path = None
    data_url = "data:video/webm;base64," + b64encode(video).decode()

    html = (
        """
<video width=800 controls>
  <source src="%s" type="video/webm">
</video>
"""
        % data_url
    )
    display(HTML(html))
    return ""


def html_renderer():
    html_path = path.join(dir_path, "visualizer", "default", "dist", "index.html")
    if path.exists(html_path):
        with open(html_path, encoding="utf-8") as f:
            return f.read()
    js_path = path.abspath(path.join(dir_path, "halite.js"))
    if path.exists(js_path):
        with open(js_path, encoding="utf-8") as js_file:
            return js_file.read()
    return ""


def html_renderer():
    htmlpath = path.join(dirpath, "visualizer", "default", "dist", "index.html")
    if path.exists(htmlpath):
        with open(htmlpath, encoding="utf-8") as f:
            return f.read()
    jspath = path.abspath(path.join(dirpath, "hungry_geese.js"))
    if path.exists(jspath):
        with open(jspath, encoding="utf-8") as f:
            return f.read()
    return ""


def html_renderer(env, mode):
    jspath = path.join(dirpath, "visualizer", "default", "dist", "index.html")
    if path.exists(jspath):
        with open(jspath, encoding="utf-8") as f:
            return f.read()
    return ""


def html_renderer(env, mode):
    jspath = path.join(dirpath, "visualizer", "default", "dist", "index.html")
    if path.exists(jspath):
        with open(jspath, encoding="utf-8") as f:
            return f.read()
    return ""


def html_renderer():
    html_path = path.join(dir_path, "visualizer", "default", "dist", "index.html")
    if path.exists(html_path):
        with open(html_path, encoding="utf-8") as f:
            return f.read()
    js_path = path.abspath(path.join(dir_path, "kore_fleets.js"))
    if path.exists(js_path):
        with open(js_path, encoding="utf-8") as js_file:
            return js_file.read()
    return ""


def html_renderer():
    html_path = path.abspath(path.join(dir_path, "index.html"))
    return ("html_path", html_path)


def html_renderer():
    html_path = path.abspath(path.join(dir_path, "index.html"))
    return ("html_path", html_path)


def html_renderer():
    html_path = path.join(dir_path, "visualizer", "default", "dist", "index.html")
    if path.exists(html_path):
        with open(html_path, encoding="utf-8") as f:
            return f.read()
    js_path = path.abspath(path.join(dir_path, "mab.js"))
    if path.exists(js_path):
        with open(js_path, encoding="utf-8") as js_file:
            return js_file.read()
    return ""


def html_renderer(env, mode):
    # In ipython/notebook mode, use the lightweight single-file JS renderer
    if mode == "ipython":
        js_path = path.abspath(path.join(dir_path, "orbit_wars.js"))
        if path.exists(js_path):
            with open(js_path, encoding="utf-8") as js_file:
                return js_file.read()
    # Default: use the full Vite-built visualizer
    jspath = path.join(dir_path, "visualizer", "default", "dist", "index.html")
    if path.exists(jspath):
        with open(jspath, encoding="utf-8") as f:
            return f.read()
    # Fallback to single-file JS renderer
    js_path = path.abspath(path.join(dir_path, "orbit_wars.js"))
    if path.exists(js_path):
        with open(js_path, encoding="utf-8") as js_file:
            return js_file.read()
    return ""


def html_renderer():
    html_path = path.join(dir_path, "visualizer", "default", "dist", "index.html")
    if path.exists(html_path):
        with open(html_path, encoding="utf-8") as f:
            return f.read()
    return ""


def html_renderer():
    """Return the built visualizer HTML, or an empty string if not built yet."""
    htmlpath = path.join(_dirpath, "visualizer", "default", "dist", "index.html")
    if path.exists(htmlpath):
        with open(htmlpath, encoding="utf-8") as f:
            return f.read()
    return ""


def html_renderer():
    html_path = path.join(dir_path, "visualizer", "default", "dist", "index.html")
    if path.exists(html_path):
        with open(html_path, encoding="utf-8") as f:
            return f.read()
    js_path = path.abspath(path.join(dir_path, "rps.js"))
    if path.exists(js_path):
        with open(js_path, encoding="utf-8") as js_file:
            return js_file.read()
    return ""


def html_renderer():
    # TODO: fully remove the need for this empty function in a future cleanup pass.
    pass


def html_renderer():
    """Reads the built web visualizer output and serves it for rendering."""
    jspath = path.join(dir_path, "visualizer", "default", "dist", "index.html")
    if path.exists(jspath):
        with open(jspath, encoding="utf-8") as f:
            return f.read()
    return ""

