
def parse_nvprof_trace(path):
    import sqlite3

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row

    # Parse strings table
    strings = {}
    for r in conn.execute("SELECT _id_ as id, value FROM StringTable"):
        strings[r["id"]] = torch._C._demangle(r["value"])

    # First, find all functions and create FunctionEvents for them
    marker_query = """
    SELECT
        start.id AS marker_id, start.name, start.timestamp AS start_time, end.timestamp AS end_time
    FROM
        CUPTI_ACTIVITY_KIND_MARKER AS start INNER JOIN CUPTI_ACTIVITY_KIND_MARKER AS end
        ON start.id = end.id
    WHERE
        start.name != 0 AND end.name = 0
    """
    functions = []
    functions_map = {}
    unique = EnforceUnique()
    for row in conn.execute(marker_query):
        unique.see(row["marker_id"])
        evt = FunctionEvent(
            id=row["marker_id"],
            node_id=0,  # missing a node_id when calling FunctionEvent. This is just to ensure
            # that pytorch doesn't crash when creating a FunctionEvent() object
            name=strings[row["name"]],
            start_us=row["start_time"],
            end_us=row["end_time"],
            thread=0,
        )  # TODO: find in sqlite database
        functions.append(evt)
        functions_map[evt.id] = evt

    # Now, correlate all kernels with FunctionEvents
    kernel_query = """
    SELECT
        start.id AS marker_id, start.name, start.timestamp, end.timestamp,
        runtime._id_ AS runtime_id, runtime.cbid, runtime.start AS runtime_start, runtime.end AS runtime_end,
        kernel.start AS kernel_start, kernel.end AS kernel_end, kernel.name AS kernel_name
    FROM
        CUPTI_ACTIVITY_KIND_MARKER AS start
        INNER JOIN CUPTI_ACTIVITY_KIND_MARKER AS end
            ON start.id = end.id
        INNER JOIN CUPTI_ACTIVITY_KIND_RUNTIME as runtime
            ON (start.timestamp < runtime.start AND runtime.end < end.timestamp)
        INNER JOIN CUPTI_ACTIVITY_KIND_CONCURRENT_KERNEL AS kernel
            ON kernel.correlationId = runtime.correlationId
    """
    unique = EnforceUnique()
    for row in conn.execute(kernel_query):
        unique.see(row["marker_id"], row["runtime_id"])
        # 211 is cudaKernelLaunch for cuda >= 9.2
        if row["cbid"] != 211:
            raise AssertionError(f"Expected cbid to be 211, but got {row['cbid']}")
        evt = functions_map[row["marker_id"]]
        evt.append_kernel(
            row["kernel_name"], 0, row["kernel_end"] - row["kernel_start"]
        )

    functions.sort(key=lambda evt: evt.time_range.start)
    return functions

