import os
from typing import Any

def _report_to_json(report: BaseReport) -> dict[str, Any]:
    """Return the contents of this report as a dict of builtin entries,
    suitable for serialization.

    This was originally the serialize_report() function from xdist (ca03269).
    """

    def serialize_repr_entry(
        entry: ReprEntry | ReprEntryNative,
    ) -> dict[str, Any]:
        data = dataclasses.asdict(entry)
        for key, value in data.items():
            if hasattr(value, "__dict__"):
                data[key] = dataclasses.asdict(value)
        entry_data = {"type": type(entry).__name__, "data": data}
        return entry_data

    def serialize_repr_traceback(reprtraceback: ReprTraceback) -> dict[str, Any]:
        result = dataclasses.asdict(reprtraceback)
        result["reprentries"] = [
            serialize_repr_entry(x) for x in reprtraceback.reprentries
        ]
        return result

    def serialize_repr_crash(
        reprcrash: ReprFileLocation | None,
    ) -> dict[str, Any] | None:
        if reprcrash is not None:
            return dataclasses.asdict(reprcrash)
        else:
            return None

    def serialize_exception_longrepr(rep: BaseReport) -> dict[str, Any]:
        assert rep.longrepr is not None
        # TODO: Investigate whether the duck typing is really necessary here.
        longrepr = cast(ExceptionRepr, rep.longrepr)
        result: dict[str, Any] = {
            "reprcrash": serialize_repr_crash(longrepr.reprcrash),
            "reprtraceback": serialize_repr_traceback(longrepr.reprtraceback),
            "sections": longrepr.sections,
        }
        if isinstance(longrepr, ExceptionChainRepr):
            result["chain"] = []
            for repr_traceback, repr_crash, description in longrepr.chain:
                result["chain"].append(
                    (
                        serialize_repr_traceback(repr_traceback),
                        serialize_repr_crash(repr_crash),
                        description,
                    )
                )
        else:
            result["chain"] = None
        return result

    d = report.__dict__.copy()
    if hasattr(report.longrepr, "toterminal"):
        if hasattr(report.longrepr, "reprtraceback") and hasattr(
            report.longrepr, "reprcrash"
        ):
            d["longrepr"] = serialize_exception_longrepr(report)
        else:
            d["longrepr"] = str(report.longrepr)
    else:
        d["longrepr"] = report.longrepr
    for name in d:
        if isinstance(d[name], os.PathLike):
            d[name] = os.fspath(d[name])
        elif name == "result":
            d[name] = None  # for now
    return d

