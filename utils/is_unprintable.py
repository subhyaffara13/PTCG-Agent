
def is_unprintable(character: str) -> bool:
    return (
        character.isspace() is False  # includes \n \t \r \v
        and character.isprintable() is False
        and character != "\x1a"  # Why? Its the ASCII substitute character.
        and character != "\ufeff"  # bug discovered in Python,
        # Zero Width No-Break Space located in 	Arabic Presentation Forms-B, Unicode 1.1 not acknowledged as space.
    )

