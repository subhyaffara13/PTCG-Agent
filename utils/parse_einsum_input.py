
def parse_einsum_input(operands: Any, shapes: bool = False) -> Tuple[str, str, List[ArrayType]]:
    """A reproduction of einsum c side einsum parsing in python.

    Parameters:
        operands: Intakes the same inputs as `contract_path`, but NOT the keyword args. The only
            supported keyword argument is:
        shapes: Whether ``parse_einsum_input`` should assume arrays (the default) or
            array shapes have been supplied.

    Returns:
        input_strings: Parsed input strings
        output_string: Parsed output string
        operands: The operands to use in the numpy contraction

    Examples:
        The operand list is simplified to reduce printing:

        ```python
        >>> a = np.random.rand(4, 4)
        >>> b = np.random.rand(4, 4, 4)
        >>> parse_einsum_input(('...a,...a->...', a, b))
        ('za,xza', 'xz', [a, b])

        >>> parse_einsum_input((a, [Ellipsis, 0], b, [Ellipsis, 0]))
        ('za,xza', 'xz', [a, b])
        ```
    """
    if len(operands) == 0:
        raise ValueError("No input operands")

    if isinstance(operands[0], str):
        subscripts = operands[0].replace(" ", "")
        if shapes:
            if any(hasattr(o, "shape") for o in operands[1:]):
                raise ValueError(
                    "shapes is set to True but given at least one operand looks like an array"
                    " (at least one operand has a shape attribute). "
                )
        operands = operands[1:]
    else:
        subscripts, operands = convert_interleaved_input(operands)

    if shapes:
        operand_shapes = operands
    else:
        operand_shapes = [get_shape(o) for o in operands]

    # Check for proper "->"
    if ("-" in subscripts) or (">" in subscripts):
        invalid = (subscripts.count("-") > 1) or (subscripts.count(">") > 1)
        if invalid or (subscripts.count("->") != 1):
            raise ValueError("Subscripts can only contain one '->'.")

    # Parse ellipses
    if "." in subscripts:
        used = subscripts.replace(".", "").replace(",", "").replace("->", "")
        ellipse_inds = "".join(gen_unused_symbols(used, max(len(x) for x in operand_shapes)))
        longest = 0

        # Do we have an output to account for?
        if "->" in subscripts:
            input_tmp, output_sub = subscripts.split("->")
            split_subscripts = input_tmp.split(",")
            out_sub = True
        else:
            split_subscripts = subscripts.split(",")
            out_sub = False

        for num, sub in enumerate(split_subscripts):
            if "." in sub:
                if (sub.count(".") != 3) or (sub.count("...") != 1):
                    raise ValueError("Invalid Ellipses.")

                # Take into account numerical values
                if operand_shapes[num] == ():
                    ellipse_count = 0
                else:
                    ellipse_count = max(len(operand_shapes[num]), 1) - (len(sub) - 3)

                if ellipse_count > longest:
                    longest = ellipse_count

                if ellipse_count < 0:
                    raise ValueError("Ellipses lengths do not match.")
                elif ellipse_count == 0:
                    split_subscripts[num] = sub.replace("...", "")
                else:
                    split_subscripts[num] = sub.replace("...", ellipse_inds[-ellipse_count:])

        subscripts = ",".join(split_subscripts)

        # Figure out output ellipses
        if longest == 0:
            out_ellipse = ""
        else:
            out_ellipse = ellipse_inds[-longest:]

        if out_sub:
            subscripts += "->" + output_sub.replace("...", out_ellipse)
        else:
            # Special care for outputless ellipses
            output_subscript = find_output_str(subscripts)
            normal_inds = "".join(sorted(set(output_subscript) - set(out_ellipse)))

            subscripts += "->" + out_ellipse + normal_inds

    # Build output string if does not exist
    if "->" in subscripts:
        input_subscripts, output_subscript = subscripts.split("->")
    else:
        input_subscripts, output_subscript = subscripts, find_output_str(subscripts)

    # Make sure output subscripts are unique and in the input
    for char in output_subscript:
        if output_subscript.count(char) != 1:
            raise ValueError(f"Output character '{char}' appeared more than once in the output.")
        if char not in input_subscripts:
            raise ValueError(f"Output character '{char}' did not appear in the input")

    # Make sure number operands is equivalent to the number of terms
    if len(input_subscripts.split(",")) != len(operands):
        raise ValueError(
            f"Number of einsum subscripts, {len(input_subscripts.split(','))}, must be equal to the "
            f"number of operands, {len(operands)}."
        )

    return input_subscripts, output_subscript, operands

