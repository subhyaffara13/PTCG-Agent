import pathlib
from typing import Callable

def _get_html_renderer_content(
    open_spiel_short_name: str, base_path_for_custom_renderers: pathlib.Path, default_renderer_func: Callable[[], str]
) -> str:
    """Tries to load a custom HTML/JS renderer for the game, falls back to default."""
    # Prefer the built Vite visualizer at games/<name>/visualizer/default/dist/index.html
    dist_index_path = pathlib.Path(
        base_path_for_custom_renderers,
        open_spiel_short_name,
        "visualizer",
        "default",
        "dist",
        "index.html",
    )
    if dist_index_path.is_file():
        try:
            with open(dist_index_path, "r", encoding="utf-8") as f:
                content = f.read()
            _log.debug(f"Using built HTML visualizer for {open_spiel_short_name} from {dist_index_path}")
            return content
        except Exception as e:  # pylint: disable=broad-exception-caught
            _log.debug(e)
    # Fallback to legacy single-file JS renderer at games/<name>/<name>.js
    custom_renderer_js_path = pathlib.Path(
        base_path_for_custom_renderers,
        open_spiel_short_name,
        f"{open_spiel_short_name}.js",
    )
    if custom_renderer_js_path.is_file():
        try:
            with open(custom_renderer_js_path, "r", encoding="utf-8") as f:
                content = f.read()
            _log.debug(f"Using custom HTML renderer for {open_spiel_short_name} from {custom_renderer_js_path}")
            return content
        except Exception as e:  # pylint: disable=broad-exception-caught
            _log.debug(e)
    return default_renderer_func()

