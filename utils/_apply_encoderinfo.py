from typing import Any

def _apply_encoderinfo(im: Image.Image, encoderinfo: dict[str, Any]) -> None:
    im.encoderconfig = (
        encoderinfo.get("optimize", False),
        encoderinfo.get("compress_level", -1),
        encoderinfo.get("compress_type", -1),
        encoderinfo.get("dictionary", b""),
    )

