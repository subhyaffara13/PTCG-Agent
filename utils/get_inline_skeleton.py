
def get_inline_skeleton():
    """Get a fully-inlined skeleton of the frontend.

    The returned HTML page has no external network dependencies for code.
    It can load model_info.json over HTTP, or be passed to burn_in_info.
    """

    import importlib.resources

    # pyrefly: ignore [bad-argument-type]
    skeleton = importlib.resources.read_text(__package__, "skeleton.html")
    # pyrefly: ignore [bad-argument-type]
    js_code = importlib.resources.read_text(__package__, "code.js")
    for js_module in ["preact", "htm"]:
        # pyrefly: ignore [bad-argument-type]
        js_lib = importlib.resources.read_binary(__package__, f"{js_module}.mjs")
        js_url = "data:application/javascript," + urllib.parse.quote(js_lib)
        js_code = js_code.replace(f"https://unpkg.com/{js_module}?module", js_url)
    skeleton = skeleton.replace(' src="./code.js">', ">\n" + js_code)
    return skeleton

