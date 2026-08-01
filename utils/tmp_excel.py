
def tmp_excel(ext, tmp_path):
    tmp = tmp_path / f"{uuid.uuid4()}{ext}"
    tmp.touch()
    return str(tmp)


def tmp_excel(ext, tmp_path):
    tmp = tmp_path / f"{uuid.uuid4()}{ext}"
    tmp.touch()
    return str(tmp)


def tmp_excel(read_ext, tmp_path):
    tmp = tmp_path / f"{uuid.uuid4()}{read_ext}"
    tmp.touch()
    return str(tmp)


def tmp_excel(tmp_path):
    tmp = tmp_path / f"{uuid.uuid4()}.xlsx"
    tmp.touch()
    return str(tmp)


def tmp_excel(ext, tmp_path):
    """
    Fixture to open file for use in each test case.
    """
    tmp = tmp_path / f"{uuid.uuid4()}{ext}"
    tmp.touch()
    return str(tmp)


def tmp_excel(ext, tmp_path):
    tmp = tmp_path / f"{uuid.uuid4()}{ext}"
    tmp.touch()
    return str(tmp)

