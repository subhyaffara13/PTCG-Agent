from typing import Any

def _show(image: Image, **options: Any) -> None:
    from . import ImageShow

    deprecate("Image._show", 13, "ImageShow.show")
    ImageShow.show(image, **options)

