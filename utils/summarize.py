import itertools
import json
from typing import List, Optional, Tuple
from pathlib import Path


def summarize(report_path: str):
    p = Path(report_path)
    if not p.exists():
        raise FileNotFoundError(f"Report file not found: {p.resolve()}")

    data = json.loads(p.read_text())
    tests = data.get("tests", [])

    # Overall counts
    outcomes = Counter(t.get("outcome", "unknown") for t in tests)

    # Filter failures (pytest-json-report uses "failed" and may have "error")
    failed = [t for t in tests if t.get("outcome") in ("failed", "error")]

    # 1) Failures per test file
    failures_per_file = Counter(_file_path(t.get("nodeid", "")) for t in failed)

    # 2) Failures per class (if any; otherwise "NO_CLASS")
    failures_per_class = Counter((_class_name(t.get("nodeid", "")) or "NO_CLASS") for t in failed)

    # 3) Failures per base test name (function), aggregating parametrized cases
    failures_per_testname = Counter(_base_test_name(t.get("nodeid", "")) for t in failed)

    # 4) Failures per test_modeling_xxx (derived from filename)
    failures_per_modeling_key = Counter()
    for t in failed:
        key = _modeling_key(_file_path(t.get("nodeid", "")))
        if key:
            failures_per_modeling_key[key] += 1

    return {
        "outcomes": outcomes,
        "failures_per_file": failures_per_file,
        "failures_per_class": failures_per_class,
        "failures_per_testname": failures_per_testname,
        "failures_per_modeling_key": failures_per_modeling_key,
    }


def summarize(source_info: SourceInfo, num_frames=1) -> str:
  frames = itertools.islice(user_frames(source_info.traceback), num_frames)
  frame_strs = [_summarize_frame(frame) if frame else "unknown"
                for frame in frames]
  return '\n'.join(reversed(frame_strs))


def summarize(
    file1: str,
    file2: str,
    include_tables: Optional[List[str]] = None,
    exclude_tables: Optional[List[str]] = None,
    font_number_1: int = -1,
    font_number_2: int = -1,
) -> Tuple[bool, str]:
    from fontTools.ttLib import TTFont

    with (
        TTFont(file1, lazy=True, fontNumber=font_number_1) as font1,
        TTFont(file2, lazy=True, fontNumber=font_number_2) as font2,
    ):
        tags1 = {str(tag) for tag in font1.reader.keys()}
        tags2 = {str(tag) for tag in font2.reader.keys()}

        all_tags = sorted(
            set(
                _iter_filtered_table_tags(
                    tags1 | tags2,
                    include_tables=include_tables,
                    exclude_tables=exclude_tables,
                )
            )
        )

        only1 = [tag for tag in all_tags if tag in tags1 and tag not in tags2]
        only2 = [tag for tag in all_tags if tag in tags2 and tag not in tags1]
        both = [tag for tag in all_tags if tag in tags1 and tag in tags2]

        identical = True
        lines: List[str] = []

        lines.append(f"Binary table summary:\n")
        lines.append(f"  file1: {file1}\n")
        lines.append(f"  file2: {file2}\n")

        if only1:
            identical = False
            lines.append(f"\nTables only in file1 ({len(only1)}):\n")
            for tag in only1:
                lines.append(f"- {tag} ({len(font1.reader[tag])} bytes)\n")
        if only2:
            identical = False
            lines.append(f"\nTables only in file2 ({len(only2)}):\n")
            for tag in only2:
                lines.append(f"+ {tag} ({len(font2.reader[tag])} bytes)\n")

        lines.append(f"\nTables in both ({len(both)}):\n")
        for tag in both:
            data1 = font1.reader[tag]
            data2 = font2.reader[tag]
            if data1 == data2:
                lines.append(f"  {tag}: SAME ({len(data1)} bytes)\n")
            else:
                identical = False
                lines.append(f"* {tag}: DIFF ({len(data1)} vs {len(data2)} bytes)\n")

        if identical:
            lines.append("\nResult: SAME\n")
        else:
            lines.append("\nResult: DIFFERENT\n")

        return identical, "".join(lines)

