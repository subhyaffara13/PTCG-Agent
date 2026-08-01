
def find_sig_line(lines, line_end):
    parenthesis_count = 0
    sig_line_end = line_end
    found_sig = False
    while not found_sig:
        for char in lines[sig_line_end]:
            if char == "(":
                parenthesis_count += 1
            elif char == ")":
                parenthesis_count -= 1
                if parenthesis_count == 0:
                    found_sig = True
                    break
        sig_line_end += 1
    return sig_line_end

