
def _is_linux_i686(executable: str) -> bool:
    with _parse_elf(executable) as f:
        return (
            f is not None
            and f.capacity == EIClass.C32
            and f.encoding == EIData.Lsb
            and f.machine == EMachine.I386
        )


def _is_linux_i686(executable: str) -> bool:
    with _parse_elf(executable) as f:
        return (
            f is not None
            and f.capacity == EIClass.C32
            and f.encoding == EIData.Lsb
            and f.machine == EMachine.I386
        )


def _is_linux_i686() -> bool:
    elf_header = _get_elf_header()
    if elf_header is None:
        return False
    result = elf_header.e_ident_class == elf_header.ELFCLASS32
    result &= elf_header.e_ident_data == elf_header.ELFDATA2LSB
    result &= elf_header.e_machine == elf_header.EM_386
    return result


def _is_linux_i686(executable: str) -> bool:
    with _parse_elf(executable) as f:
        return (
            f is not None
            and f.capacity == EIClass.C32
            and f.encoding == EIData.Lsb
            and f.machine == EMachine.I386
        )

