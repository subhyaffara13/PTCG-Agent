
def hal_report_to_terminal(report, base_indent=0):
    """Yield lines from the HalsteadReport to print to the terminal."""
    yield "h1: {}".format(report.h1), (), {"indent": 1 + base_indent}
    yield "h2: {}".format(report.h2), (), {"indent": 1 + base_indent}
    yield "N1: {}".format(report.N1), (), {"indent": 1 + base_indent}
    yield "N2: {}".format(report.N2), (), {"indent": 1 + base_indent}
    yield "vocabulary: {}".format(report.vocabulary), (), {
        "indent": 1 + base_indent
    }
    yield "length: {}".format(report.length), (), {"indent": 1 + base_indent}
    yield "calculated_length: {}".format(report.calculated_length), (), {
        "indent": 1 + base_indent
    }
    yield "volume: {}".format(report.volume), (), {"indent": 1 + base_indent}
    yield "difficulty: {}".format(report.difficulty), (), {
        "indent": 1 + base_indent
    }
    yield "effort: {}".format(report.effort), (), {"indent": 1 + base_indent}
    yield "time: {}".format(report.time), (), {"indent": 1 + base_indent}
    yield "bugs: {}".format(report.bugs), (), {"indent": 1 + base_indent}

