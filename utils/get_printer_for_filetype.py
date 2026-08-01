
def get_printer_for_filetype(filetype: str) -> type[Printer]:
    return filetype_to_printer.get(filetype, DotPrinter)

