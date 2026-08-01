
def show_c(cfiles: list[list[tuple[str, str]]]) -> None:
    heading("Generated C")
    for group in cfiles:
        for cfile, ctext in group:
            print(f"== {cfile} ==")
            print_with_line_numbers(ctext)
    heading("End C")

