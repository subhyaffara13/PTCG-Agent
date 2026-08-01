
def is_sdxl(source_dir: Path):
    return (
        (source_dir / "text_encoder_2").exists()
        and not (source_dir / "text_encoder_3").exists()
        and not (source_dir / "transformer").exists()
    )

