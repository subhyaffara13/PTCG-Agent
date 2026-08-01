
def writelines(path, lines, sep="\r"):
    with open(path, "w", encoding="ascii", newline=sep) as f:
        f.write("\n".join(lines) + "\n")

