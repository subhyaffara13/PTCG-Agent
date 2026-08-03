from pathlib import Path


def is_flux(source_dir: Path):
    return (
        (source_dir / "text_encoder_2").exists()
        and not (source_dir / "text_encoder_3").exists()
        and (source_dir / "transformer").exists()
    )

