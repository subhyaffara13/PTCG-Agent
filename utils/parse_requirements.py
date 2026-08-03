import os
from typing import Any, Dict, Optional, Union

def parse_requirements(
    filename: str,
    is_constraint: bool = False,
    include_nested: bool = True,
) -> Iterator[Union[
    ParsedRequirement,
    OptionLine,
    InvalidRequirementLine,
    CommentRequirementLine,
]]:
    """Parse a requirements file and yield ParsedRequirement,
    InvalidRequirementLine or CommentRequirementLine instances.

    :param filename:    Path or url of requirements file.
    :param is_constraint:  If true, parsing a constraint file rather than
        requirements file.
    :param include_nested: if true, also load and parse -r/--requirements
        and -c/--constraints nested files.
    """
    line_parser = get_line_parser()
    parser = RequirementsFileParser(line_parser)

    for parsed_line in parser.parse(
        filename=filename,
        is_constraint=is_constraint,
        include_nested=include_nested,
    ):

        if isinstance(parsed_line, ParsedLine):
            for parsed_req_or_opt in handle_line(parsed_line=parsed_line):
                if parsed_req_or_opt is not None:
                    yield parsed_req_or_opt

        else:
            assert isinstance(parsed_line, (InvalidRequirementLine, CommentRequirementLine,))
            yield parsed_line


def parse_requirements(
    filename: os.PathLike,
    options: Optional[Any] = None,
    include_invalid: bool = False,
    strict_hashes: bool = False,
) -> Dict[str, Union[Requirement, UnparsedRequirement]]:
    to_parse = {filename}
    parsed = set()
    name_to_req = {}

    while to_parse:
        filename = to_parse.pop()
        dirname = os.path.dirname(filename)
        parsed.add(filename)

        # Combine multi-line commands
        lines = "".join(_read_file(filename)).replace("\\\n", "").splitlines()
        lines_enum = enumerate(lines, 1)
        lines_enum = _ignore_comments(lines_enum)
        lines_enum = _skip_regex(lines_enum, options)

        for lineno, line in lines_enum:
            req: Optional[Union[Requirement, UnparsedRequirement]] = None
            known, _ = parser.parse_known_args(line.strip().split())

            hashes_by_kind = defaultdict(list)
            if known.hashes:
                for hsh in known.hashes:
                    kind, hsh = hsh.split(":", 1)
                    if kind not in VALID_HASHES:
                        raise PipError(
                            "Invalid --hash kind %s, expected one of %s"
                            % (kind, VALID_HASHES)
                        )
                    hashes_by_kind[kind].append(hsh)

            if known.req:
                req_str = str().join(known.req)
                try:
                    parsed_req_str = _parse_requirement_url(req_str)
                except PipError as e:
                    if include_invalid:
                        req = UnparsedRequirement(req_str, str(e), filename, lineno)
                    else:
                        raise

                try:  # Try to parse this as a requirement specification
                    if req is None:
                        req = Requirement(
                            parsed_req_str,
                            hashes=dict(hashes_by_kind),
                            filename=filename,
                            lineno=lineno,
                        )
                except requirements.InvalidRequirement:
                    try:
                        _check_invalid_requirement(req_str)
                    except PipError as e:
                        if include_invalid:
                            req = UnparsedRequirement(req_str, str(e), filename, lineno)
                        else:
                            raise

            elif known.requirement:
                full_path = os.path.join(dirname, known.requirement)
                if full_path not in parsed:
                    to_parse.add(full_path)
            elif known.editable:
                name, url = _parse_editable(known.editable)
                req = Requirement(
                    "%s @ %s" % (name, url),
                    filename=filename,
                    lineno=lineno,
                    editable=True,
                )
            else:
                pass  # This is an invalid requirement

            # If we've found a requirement, add it
            if req:
                if not isinstance(req, UnparsedRequirement):
                    req.comes_from = "-r {} (line {})".format(filename, lineno)  # type: ignore
                    if req.marker is not None and not req.marker.evaluate():
                        continue

                if req.name not in name_to_req:
                    name_to_req[req.name.lower()] = req
                else:
                    raise PipError(
                        "Double requirement given: %s (already in %s, name=%r)"
                        % (req, name_to_req[req.name], req.name)
                    )

    if strict_hashes:
        missing_hashes = [req for req in name_to_req.values() if not req.hashes]
        if len(missing_hashes) > 0:
            raise PipError(
                "Missing hashes for requirement in %s, line %s"
                % (missing_hashes[0].filename, missing_hashes[0].lineno)
            )

    return name_to_req


def parse_requirements(strs: _NestedStr) -> map[Requirement]:
    """
    Yield ``Requirement`` objects for each specification in `strs`.

    `strs` must be a string, or a (possibly-nested) iterable thereof.
    """
    return map(Requirement, join_continuation(map(drop_comment, yield_lines(strs))))


def parse_requirements(
    filename: str,
    session: PipSession,
    finder: PackageFinder | None = None,
    options: optparse.Values | None = None,
    constraint: bool = False,
) -> Generator[ParsedRequirement, None, None]:
    """Parse a requirements file and yield ParsedRequirement instances.

    :param filename:    Path or url of requirements file.
    :param session:     PipSession instance.
    :param finder:      Instance of pip.index.PackageFinder.
    :param options:     cli options.
    :param constraint:  If true, parsing a constraint file rather than
        requirements file.
    """
    line_parser = get_line_parser(finder)
    parser = RequirementsFileParser(session, line_parser)

    for parsed_line in parser.parse(filename, constraint):
        parsed_req = handle_line(
            parsed_line, options=options, finder=finder, session=session
        )
        if parsed_req is not None:
            yield parsed_req

