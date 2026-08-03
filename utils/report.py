import json
import os
import re
import sys

def report() -> None:  # pragma: no cover
    """Print a report to the terminal with debugging information"""
    console = Console()
    inspect(console)
    features = get_windows_console_features()
    inspect(features)

    env_names = (
        "CLICOLOR",
        "COLORTERM",
        "COLUMNS",
        "JPY_PARENT_PID",
        "JUPYTER_COLUMNS",
        "JUPYTER_LINES",
        "LINES",
        "NO_COLOR",
        "TERM_PROGRAM",
        "TERM",
        "TTY_COMPATIBLE",
        "TTY_INTERACTIVE",
        "VSCODE_VERBOSE_LOGGING",
    )
    env = {name: os.getenv(name) for name in env_names}
    console.print(Panel.fit((Pretty(env)), title="[b]Environment Variables"))

    console.print(f'platform="{platform.system()}"')


def report() -> None:  # pragma: no cover
    """Print a report to the terminal with debugging information"""
    console = Console()
    inspect(console)
    features = get_windows_console_features()
    inspect(features)

    env_names = (
        "CLICOLOR",
        "COLORTERM",
        "COLUMNS",
        "JPY_PARENT_PID",
        "JUPYTER_COLUMNS",
        "JUPYTER_LINES",
        "LINES",
        "NO_COLOR",
        "TERM_PROGRAM",
        "TERM",
        "TTY_COMPATIBLE",
        "TTY_INTERACTIVE",
        "VSCODE_VERBOSE_LOGGING",
    )
    env = {name: os.getenv(name) for name in env_names}
    console.print(Panel.fit((Pretty(env)), title="[b]Environment Variables"))

    console.print(f'platform="{platform.system()}"')


def report(rule, location, description):
    global warnings
    warnings += 1
    print(f'{warnings:3}. {location}:  {description} [{rule}]')


def report(manager, fileobj, sev_level, conf_level, lines=-1):
    """Prints issues in CSV format

    :param manager: the bandit manager object
    :param fileobj: The output file object, which may be sys.stdout
    :param sev_level: Filtering severity level
    :param conf_level: Filtering confidence level
    :param lines: Number of lines to report, -1 for all
    """

    results = manager.get_issue_list(
        sev_level=sev_level, conf_level=conf_level
    )

    with fileobj:
        fieldnames = [
            "filename",
            "test_name",
            "test_id",
            "issue_severity",
            "issue_confidence",
            "issue_cwe",
            "issue_text",
            "line_number",
            "col_offset",
            "end_col_offset",
            "line_range",
            "more_info",
        ]

        writer = csv.DictWriter(
            fileobj, fieldnames=fieldnames, extrasaction="ignore"
        )
        writer.writeheader()
        for result in results:
            r = result.as_dict(with_code=False)
            r["issue_cwe"] = r["issue_cwe"]["link"]
            r["more_info"] = docs_utils.get_url(r["test_id"])
            writer.writerow(r)

    if fileobj.name != sys.stdout.name:
        LOG.info("CSV output written to file: %s", fileobj.name)


def report(manager, fileobj, sev_level, conf_level, template=None):
    """Prints issues in custom format

    :param manager: the bandit manager object
    :param fileobj: The output file object, which may be sys.stdout
    :param sev_level: Filtering severity level
    :param conf_level: Filtering confidence level
    :param template: Output template with non-terminal tags <N>
                    (default: '{abspath}:{line}:
                    {test_id}[bandit]: {severity}: {msg}')
    """

    machine_output = {"results": [], "errors": []}
    for fname, reason in manager.get_skipped():
        machine_output["errors"].append({"filename": fname, "reason": reason})

    results = manager.get_issue_list(
        sev_level=sev_level, conf_level=conf_level
    )

    msg_template = template
    if template is None:
        msg_template = "{abspath}:{line}: {test_id}[bandit]: {severity}: {msg}"

    # Dictionary of non-terminal tags that will be expanded
    tag_mapper = {
        "abspath": lambda issue: os.path.abspath(issue.fname),
        "relpath": lambda issue: os.path.relpath(issue.fname),
        "line": lambda issue: issue.lineno,
        "col": lambda issue: issue.col_offset,
        "end_col": lambda issue: issue.end_col_offset,
        "test_id": lambda issue: issue.test_id,
        "severity": lambda issue: issue.severity,
        "msg": lambda issue: issue.text,
        "confidence": lambda issue: issue.confidence,
        "range": lambda issue: issue.linerange,
        "cwe": lambda issue: issue.cwe,
    }

    # Create dictionary with tag sets to speed up search for similar tags
    tag_sim_dict = {tag: set(tag) for tag, _ in tag_mapper.items()}

    # Parse the format_string template and check the validity of tags
    try:
        parsed_template_orig = list(string.Formatter().parse(msg_template))
        # of type (literal_text, field_name, fmt_spec, conversion)

        # Check the format validity only, ignore keys
        string.Formatter().vformat(msg_template, (), SafeMapper(line=0))
    except ValueError as e:
        LOG.error("Template is not in valid format: %s", e.args[0])
        sys.exit(2)

    tag_set = {t[1] for t in parsed_template_orig if t[1] is not None}
    if not tag_set:
        LOG.error("No tags were found in the template. Are you missing '{}'?")
        sys.exit(2)

    def get_similar_tag(tag):
        similarity_list = [
            (len(set(tag) & t_set), t) for t, t_set in tag_sim_dict.items()
        ]
        return sorted(similarity_list)[-1][1]

    tag_blacklist = []
    for tag in tag_set:
        # check if the tag is in dictionary
        if tag not in tag_mapper:
            similar_tag = get_similar_tag(tag)
            LOG.warning(
                "Tag '%s' was not recognized and will be skipped, "
                "did you mean to use '%s'?",
                tag,
                similar_tag,
            )
            tag_blacklist += [tag]

    # Compose the message template back with the valid values only
    msg_parsed_template_list = []
    for literal_text, field_name, fmt_spec, conversion in parsed_template_orig:
        if literal_text:
            # if there is '{' or '}', double it to prevent expansion
            literal_text = re.sub("{", "{{", literal_text)
            literal_text = re.sub("}", "}}", literal_text)
            msg_parsed_template_list.append(literal_text)

        if field_name is not None:
            if field_name in tag_blacklist:
                msg_parsed_template_list.append(field_name)
                continue
            # Append the fmt_spec part
            params = [field_name, fmt_spec, conversion]
            markers = ["", ":", "!"]
            msg_parsed_template_list.append(
                ["{"]
                + [f"{m + p}" if p else "" for m, p in zip(markers, params)]
                + ["}"]
            )

    msg_parsed_template = (
        "".join([item for lst in msg_parsed_template_list for item in lst])
        + "\n"
    )
    with fileobj:
        for defect in results:
            evaluated_tags = SafeMapper(
                (k, v(defect)) for k, v in tag_mapper.items()
            )
            output = msg_parsed_template.format(**evaluated_tags)

            fileobj.write(output)

    if fileobj.name != sys.stdout.name:
        LOG.info("Result written to file: %s", fileobj.name)


def report(manager, fileobj, sev_level, conf_level, lines=-1):
    """Writes issues to 'fileobj' in HTML format

    :param manager: the bandit manager object
    :param fileobj: The output file object, which may be sys.stdout
    :param sev_level: Filtering severity level
    :param conf_level: Filtering confidence level
    :param lines: Number of lines to report, -1 for all
    """

    header_block = """
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<title>
    Bandit Report
</title>

<style>

html * {
    font-family: "Arial", sans-serif;
}

pre {
    font-family: "Monaco", monospace;
}

.bordered-box {
    border: 1px solid black;
    padding-top:.5em;
    padding-bottom:.5em;
    padding-left:1em;
}

.metrics-box {
    font-size: 1.1em;
    line-height: 130%;
}

.metrics-title {
    font-size: 1.5em;
    font-weight: 500;
    margin-bottom: .25em;
}

.issue-description {
    font-size: 1.3em;
    font-weight: 500;
}

.candidate-issues {
    margin-left: 2em;
    border-left: solid 1px; LightGray;
    padding-left: 5%;
    margin-top: .2em;
    margin-bottom: .2em;
}

.issue-block {
    border: 1px solid LightGray;
    padding-left: .5em;
    padding-top: .5em;
    padding-bottom: .5em;
    margin-bottom: .5em;
}

.issue-sev-high {
    background-color: Pink;
}

.issue-sev-medium {
    background-color: NavajoWhite;
}

.issue-sev-low {
    background-color: LightCyan;
}

</style>
</head>
"""

    report_block = """
<body>
{metrics}
{skipped}

<br>
<div id="results">
    {results}
</div>

</body>
</html>
"""

    issue_block = """
<div id="issue-{issue_no}">
<div class="issue-block {issue_class}">
    <b>{test_name}: </b> {test_text}<br>
    <b>Test ID:</b> {test_id}<br>
    <b>Severity: </b>{severity}<br>
    <b>Confidence: </b>{confidence}<br>
    <b>CWE: </b><a href="{cwe_link}" target="_blank">CWE-{cwe.id}</a><br>
    <b>File: </b><a href="{path}" target="_blank">{path}</a><br>
    <b>Line number: </b>{line_number}<br>
    <b>More info: </b><a href="{url}" target="_blank">{url}</a><br>
{code}
{candidates}
</div>
</div>
"""

    code_block = """
<div class="code">
<pre>
{code}
</pre>
</div>
"""

    candidate_block = """
<div class="candidates">
<br>
<b>Candidates: </b>
{candidate_list}
</div>
"""

    candidate_issue = """
<div class="candidate">
<div class="candidate-issues">
<pre>{code}</pre>
</div>
</div>
"""

    skipped_block = """
<br>
<div id="skipped">
<div class="bordered-box">
<b>Skipped files:</b><br><br>
{files_list}
</div>
</div>
"""

    metrics_block = """
<div id="metrics">
    <div class="metrics-box bordered-box">
        <div class="metrics-title">
            Metrics:<br>
        </div>
        Total lines of code: <span id="loc">{loc}</span><br>
        Total lines skipped (#nosec): <span id="nosec">{nosec}</span>
    </div>
</div>

"""

    issues = manager.get_issue_list(sev_level=sev_level, conf_level=conf_level)

    baseline = not isinstance(issues, list)

    # build the skipped string to insert in the report
    skipped_str = "".join(
        f"{fname} <b>reason:</b> {reason}<br>"
        for fname, reason in manager.get_skipped()
    )
    if skipped_str:
        skipped_text = skipped_block.format(files_list=skipped_str)
    else:
        skipped_text = ""

    # build the results string to insert in the report
    results_str = ""
    for index, issue in enumerate(issues):
        if not baseline or len(issues[issue]) == 1:
            candidates = ""
            safe_code = html_escape(
                issue.get_code(lines, True).strip("\n").lstrip(" ")
            )
            code = code_block.format(code=safe_code)
        else:
            candidates_str = ""
            code = ""
            for candidate in issues[issue]:
                candidate_code = html_escape(
                    candidate.get_code(lines, True).strip("\n").lstrip(" ")
                )
                candidates_str += candidate_issue.format(code=candidate_code)

            candidates = candidate_block.format(candidate_list=candidates_str)

        url = docs_utils.get_url(issue.test_id)
        results_str += issue_block.format(
            issue_no=index,
            issue_class=f"issue-sev-{issue.severity.lower()}",
            test_name=issue.test,
            test_id=issue.test_id,
            test_text=issue.text,
            severity=issue.severity,
            confidence=issue.confidence,
            cwe=issue.cwe,
            cwe_link=issue.cwe.link(),
            path=issue.fname,
            code=code,
            candidates=candidates,
            url=url,
            line_number=issue.lineno,
        )

    # build the metrics string to insert in the report
    metrics_summary = metrics_block.format(
        loc=manager.metrics.data["_totals"]["loc"],
        nosec=manager.metrics.data["_totals"]["nosec"],
    )

    # build the report and output it
    report_contents = report_block.format(
        metrics=metrics_summary, skipped=skipped_text, results=results_str
    )

    with fileobj:
        wrapped_file = utils.wrap_file_object(fileobj)
        wrapped_file.write(header_block)
        wrapped_file.write(report_contents)

    if fileobj.name != sys.stdout.name:
        LOG.info("HTML output written to file: %s", fileobj.name)


def report(manager, fileobj, sev_level, conf_level, lines=-1):
    """''Prints issues in JSON format

    :param manager: the bandit manager object
    :param fileobj: The output file object, which may be sys.stdout
    :param sev_level: Filtering severity level
    :param conf_level: Filtering confidence level
    :param lines: Number of lines to report, -1 for all
    """

    machine_output = {"results": [], "errors": []}
    for fname, reason in manager.get_skipped():
        machine_output["errors"].append({"filename": fname, "reason": reason})

    results = manager.get_issue_list(
        sev_level=sev_level, conf_level=conf_level
    )

    baseline = not isinstance(results, list)

    if baseline:
        collector = []
        for r in results:
            d = r.as_dict(max_lines=lines)
            d["more_info"] = docs_utils.get_url(d["test_id"])
            if len(results[r]) > 1:
                d["candidates"] = [
                    c.as_dict(max_lines=lines) for c in results[r]
                ]
            collector.append(d)

    else:
        collector = [r.as_dict(max_lines=lines) for r in results]
        for elem in collector:
            elem["more_info"] = docs_utils.get_url(elem["test_id"])

    itemgetter = operator.itemgetter
    if manager.agg_type == "vuln":
        machine_output["results"] = sorted(
            collector, key=itemgetter("test_name")
        )
    else:
        machine_output["results"] = sorted(
            collector, key=itemgetter("filename")
        )

    machine_output["metrics"] = manager.metrics.data

    # timezone agnostic format
    TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    time_string = datetime.datetime.now(datetime.timezone.utc).strftime(
        TS_FORMAT
    )
    machine_output["generated_at"] = time_string

    result = json.dumps(
        machine_output, sort_keys=True, indent=2, separators=(",", ": ")
    )

    with fileobj:
        fileobj.write(result)

    if fileobj.name != sys.stdout.name:
        LOG.info("JSON output written to file: %s", fileobj.name)


def report(manager, fileobj, sev_level, conf_level, lines=-1):
    """Prints issues in SARIF format

    :param manager: the bandit manager object
    :param fileobj: The output file object, which may be sys.stdout
    :param sev_level: Filtering severity level
    :param conf_level: Filtering confidence level
    :param lines: Number of lines to report, -1 for all
    """

    log = om.SarifLog(
        schema_uri=SCHEMA_URI,
        version=SCHEMA_VER,
        runs=[
            om.Run(
                tool=om.Tool(
                    driver=om.ToolComponent(
                        name="Bandit",
                        organization=bandit.__author__,
                        semantic_version=bandit.__version__,
                        version=bandit.__version__,
                    )
                ),
                invocations=[
                    om.Invocation(
                        end_time_utc=datetime.datetime.now(
                            datetime.timezone.utc
                        ).strftime(TS_FORMAT),
                        execution_successful=True,
                    )
                ],
                properties={"metrics": manager.metrics.data},
            )
        ],
    )

    run = log.runs[0]
    invocation = run.invocations[0]

    skips = manager.get_skipped()
    add_skipped_file_notifications(skips, invocation)

    issues = manager.get_issue_list(sev_level=sev_level, conf_level=conf_level)

    add_results(issues, run)

    serializedLog = to_json(log)

    with fileobj:
        fileobj.write(serializedLog)

    if fileobj.name != sys.stdout.name:
        LOG.info("SARIF output written to file: %s", fileobj.name)


def report(manager, fileobj, sev_level, conf_level, lines=-1):
    """Prints discovered issues formatted for screen reading

    This makes use of VT100 terminal codes for colored text.

    :param manager: the bandit manager object
    :param fileobj: The output file object, which may be sys.stdout
    :param sev_level: Filtering severity level
    :param conf_level: Filtering confidence level
    :param lines: Number of lines to report, -1 for all
    """

    if IS_WIN_PLATFORM and COLORAMA:
        colorama.init()

    bits = []
    if not manager.quiet or manager.results_count(sev_level, conf_level):
        bits.append(
            header(
                "Run started:%s", datetime.datetime.now(datetime.timezone.utc)
            )
        )

        if manager.verbose:
            bits.append(get_verbose_details(manager))

        bits.append(header("\nTest results:"))
        bits.append(get_results(manager, sev_level, conf_level, lines))
        bits.append(header("\nCode scanned:"))
        bits.append(
            "\tTotal lines of code: %i"
            % (manager.metrics.data["_totals"]["loc"])
        )

        bits.append(
            "\tTotal lines skipped (#nosec): %i"
            % (manager.metrics.data["_totals"]["nosec"])
        )

        bits.append(get_metrics(manager))
        skipped = manager.get_skipped()
        bits.append(header("Files skipped (%i):", len(skipped)))
        bits.extend(["\t%s (%s)" % skip for skip in skipped])
        do_print(bits)

    if fileobj.name != sys.stdout.name:
        LOG.info(
            "Screen formatter output was not written to file: %s, "
            "consider '-f txt'",
            fileobj.name,
        )

    if IS_WIN_PLATFORM and COLORAMA:
        colorama.deinit()


def report(manager, fileobj, sev_level, conf_level, lines=-1):
    """Prints discovered issues in the text format

    :param manager: the bandit manager object
    :param fileobj: The output file object, which may be sys.stdout
    :param sev_level: Filtering severity level
    :param conf_level: Filtering confidence level
    :param lines: Number of lines to report, -1 for all
    """

    bits = []

    if not manager.quiet or manager.results_count(sev_level, conf_level):
        bits.append(
            f"Run started:{datetime.datetime.now(datetime.timezone.utc)}"
        )

        if manager.verbose:
            bits.append(get_verbose_details(manager))

        bits.append("\nTest results:")
        bits.append(get_results(manager, sev_level, conf_level, lines))
        bits.append("\nCode scanned:")
        bits.append(
            "\tTotal lines of code: %i"
            % (manager.metrics.data["_totals"]["loc"])
        )

        bits.append(
            "\tTotal lines skipped (#nosec): %i"
            % (manager.metrics.data["_totals"]["nosec"])
        )
        bits.append(
            "\tTotal potential issues skipped due to specifically being "
            "disabled (e.g., #nosec BXXX): %i"
            % (manager.metrics.data["_totals"]["skipped_tests"])
        )

        skipped = manager.get_skipped()
        bits.append(get_metrics(manager))
        bits.append(f"Files skipped ({len(skipped)}):")
        bits.extend(["\t%s (%s)" % skip for skip in skipped])
        result = "\n".join([bit for bit in bits]) + "\n"

        with fileobj:
            wrapped_file = utils.wrap_file_object(fileobj)
            wrapped_file.write(result)

    if fileobj.name != sys.stdout.name:
        LOG.info("Text output written to file: %s", fileobj.name)


def report(manager, fileobj, sev_level, conf_level, lines=-1):
    """Prints issues in XML format

    :param manager: the bandit manager object
    :param fileobj: The output file object, which may be sys.stdout
    :param sev_level: Filtering severity level
    :param conf_level: Filtering confidence level
    :param lines: Number of lines to report, -1 for all
    """

    issues = manager.get_issue_list(sev_level=sev_level, conf_level=conf_level)
    root = ET.Element("testsuite", name="bandit", tests=str(len(issues)))

    for issue in issues:
        test = issue.test
        testcase = ET.SubElement(
            root, "testcase", classname=issue.fname, name=test
        )

        text = (
            "Test ID: %s Severity: %s Confidence: %s\nCWE: %s\n%s\n"
            "Location %s:%s"
        )
        text %= (
            issue.test_id,
            issue.severity,
            issue.confidence,
            issue.cwe,
            issue.text,
            issue.fname,
            issue.lineno,
        )
        ET.SubElement(
            testcase,
            "error",
            more_info=docs_utils.get_url(issue.test_id),
            type=issue.severity,
            message=issue.text,
        ).text = text

    tree = ET.ElementTree(root)

    if fileobj.name == sys.stdout.name:
        fileobj = sys.stdout.buffer
    elif fileobj.mode == "w":
        fileobj.close()
        fileobj = open(fileobj.name, "wb")

    with fileobj:
        tree.write(fileobj, encoding="utf-8", xml_declaration=True)

    if fileobj.name != sys.stdout.name:
        LOG.info("XML output written to file: %s", fileobj.name)


def report(manager, fileobj, sev_level, conf_level, lines=-1):
    """Prints issues in YAML format

    :param manager: the bandit manager object
    :param fileobj: The output file object, which may be sys.stdout
    :param sev_level: Filtering severity level
    :param conf_level: Filtering confidence level
    :param lines: Number of lines to report, -1 for all
    """

    machine_output = {"results": [], "errors": []}
    for fname, reason in manager.get_skipped():
        machine_output["errors"].append({"filename": fname, "reason": reason})

    results = manager.get_issue_list(
        sev_level=sev_level, conf_level=conf_level
    )

    collector = [r.as_dict(max_lines=lines) for r in results]
    for elem in collector:
        elem["more_info"] = docs_utils.get_url(elem["test_id"])

    itemgetter = operator.itemgetter
    if manager.agg_type == "vuln":
        machine_output["results"] = sorted(
            collector, key=itemgetter("test_name")
        )
    else:
        machine_output["results"] = sorted(
            collector, key=itemgetter("filename")
        )

    machine_output["metrics"] = manager.metrics.data

    for result in machine_output["results"]:
        if "code" in result:
            code = result["code"].replace("\n", "\\n")
            result["code"] = code

    # timezone agnostic format
    TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    time_string = datetime.datetime.now(datetime.timezone.utc).strftime(
        TS_FORMAT
    )
    machine_output["generated_at"] = time_string

    yaml.safe_dump(machine_output, fileobj, default_flow_style=False)

    if fileobj.name != sys.stdout.name:
        LOG.info("YAML output written to file: %s", fileobj.name)

