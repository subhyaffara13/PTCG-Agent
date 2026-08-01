
def get_player(window_kaggle: dict[str, Any], renderer: tuple[str, str] | str) -> str:
    # TODO: resolve type alert here. Renderer is clearly not a string, but gets .strip() called.
    if isinstance(renderer, tuple) and renderer[0] == "html_path":
        key = "/*window.kaggle*/"
        value = f"""
window.kaggle = {json.dumps(window_kaggle, indent=2)};\n\n
        """
        return read_file(renderer[1]).replace(key, value)

    key = "/*window.kaggle*/"
    value = f"""
window.kaggle = {json.dumps(window_kaggle, indent=2)};\n\n
window.kaggle.renderer = {renderer.strip()};\n\n
    """
    return read_file(Path.joinpath(root_path, "static", "player.html")).replace(key, value)

