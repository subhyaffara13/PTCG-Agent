
def _output_issue_str(
    issue, indent, show_lineno=True, show_code=True, lines=-1
):
    # returns a list of lines that should be added to the existing lines list
    bits = []
    bits.append(
        "%s%s>> Issue: [%s:%s] %s"
        % (
            indent,
            COLOR[issue.severity],
            issue.test_id,
            issue.test,
            issue.text,
        )
    )

    bits.append(
        "%s   Severity: %s   Confidence: %s"
        % (
            indent,
            issue.severity.capitalize(),
            issue.confidence.capitalize(),
        )
    )

    bits.append(f"{indent}   CWE: {str(issue.cwe)}")

    bits.append(f"{indent}   More Info: {docs_utils.get_url(issue.test_id)}")

    bits.append(
        "%s   Location: %s:%s:%s%s"
        % (
            indent,
            issue.fname,
            issue.lineno if show_lineno else "",
            issue.col_offset if show_lineno else "",
            COLOR["DEFAULT"],
        )
    )

    if show_code:
        bits.extend(
            [indent + line for line in issue.get_code(lines, True).split("\n")]
        )

    return "\n".join([bit for bit in bits])


def _output_issue_str(
    issue, indent, show_lineno=True, show_code=True, lines=-1
):
    # returns a list of lines that should be added to the existing lines list
    bits = []
    bits.append(
        f"{indent}>> Issue: [{issue.test_id}:{issue.test}] {issue.text}"
    )

    bits.append(
        "%s   Severity: %s   Confidence: %s"
        % (
            indent,
            issue.severity.capitalize(),
            issue.confidence.capitalize(),
        )
    )

    bits.append(f"{indent}   CWE: {str(issue.cwe)}")

    bits.append(f"{indent}   More Info: {docs_utils.get_url(issue.test_id)}")

    bits.append(
        "%s   Location: %s:%s:%s"
        % (
            indent,
            issue.fname,
            issue.lineno if show_lineno else "",
            issue.col_offset if show_lineno else "",
        )
    )

    if show_code:
        bits.extend(
            [indent + line for line in issue.get_code(lines, True).split("\n")]
        )

    return "\n".join([bit for bit in bits])

