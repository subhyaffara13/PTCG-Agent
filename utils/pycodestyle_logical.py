from typing import Any

def pycodestyle_logical(
    blank_before: Any,
    blank_lines: Any,
    checker_state: Any,
    hang_closing: Any,
    indent_char: Any,
    indent_level: Any,
    indent_size: Any,
    line_number: Any,
    lines: Any,
    logical_line: Any,
    max_doc_length: Any,
    noqa: Any,
    previous_indent_level: Any,
    previous_logical: Any,
    previous_unindented_logical_line: Any,
    tokens: Any,
    verbose: Any,
) -> Generator[tuple[int, str]]:
    """Run pycodestyle logical checks."""
    yield from _ambiguous_identifier(logical_line, tokens)
    yield from _bare_except(logical_line, noqa)
    yield from _blank_lines(logical_line, blank_lines, indent_level, line_number, blank_before, previous_logical, previous_unindented_logical_line, previous_indent_level, lines)  # noqa: E501
    yield from _break_after_binary_operator(logical_line, tokens)
    yield from _break_before_binary_operator(logical_line, tokens)
    yield from _comparison_negative(logical_line)
    yield from _comparison_to_singleton(logical_line, noqa)
    yield from _comparison_type(logical_line, noqa)
    yield from _compound_statements(logical_line)
    yield from _continued_indentation(logical_line, tokens, indent_level, hang_closing, indent_char, indent_size, noqa, verbose)  # noqa: E501
    yield from _explicit_line_join(logical_line, tokens)
    yield from _extraneous_whitespace(logical_line)
    yield from _imports_on_separate_lines(logical_line)
    yield from _indentation(logical_line, previous_logical, indent_char, indent_level, previous_indent_level, indent_size)  # noqa: E501
    yield from _maximum_doc_length(logical_line, max_doc_length, noqa, tokens)
    yield from _missing_whitespace(logical_line, tokens)
    yield from _missing_whitespace_after_keyword(logical_line, tokens)
    yield from _module_imports_on_top_of_file(logical_line, indent_level, checker_state, noqa)  # noqa: E501
    yield from _python_3000_invalid_escape_sequence(logical_line, tokens, noqa)
    yield from _whitespace_around_comma(logical_line)
    yield from _whitespace_around_keywords(logical_line)
    yield from _whitespace_around_named_parameter_equals(logical_line, tokens)
    yield from _whitespace_around_operator(logical_line)
    yield from _whitespace_before_comment(logical_line, tokens)
    yield from _whitespace_before_parameters(logical_line, tokens)

