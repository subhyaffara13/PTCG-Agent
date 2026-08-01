
def _create_file_view(file: io.IOBase, offset: int, length: int) -> io.IOBase:
    # FIXME (kumpera) torch.load fails if we wrap with io.BufferedReader
    return _ReaderView(file, offset, length)

