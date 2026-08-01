
def assert_link_to(file: Path, other: Path) -> None:
    if file.is_symlink():
        assert str(file.resolve()) == str(other.resolve())
    else:
        file_stat = file.stat()
        other_stat = other.stat()
        assert file_stat[stat.ST_INO] == other_stat[stat.ST_INO]
        assert file_stat[stat.ST_DEV] == other_stat[stat.ST_DEV]

