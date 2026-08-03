from typing import Any

def create_node_mapping_kernel_to_post_grad(
    triton_kernel_to_post_grad_json: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Create bidirectional mappings between triton kernel name and post_grad
    graph code nodes, and vice versa.
    """

    # return a dummy dict if there's any error
    empty_return: dict[str, dict[str, Any]] = {
        "cppCodeToPost": {},
        "postToCppCode": {},
    }

    if not isinstance(triton_kernel_to_post_grad_json, dict):
        log.error(
            "Provenance tacking error: triton_kernel_to_post_grad_json is not a dict"
        )
        return empty_return

    post_to_cpp_code: dict[str, Any] = collections.defaultdict(OrderedSet)

    try:
        for outer_key, node_array in triton_kernel_to_post_grad_json.items():
            if not isinstance(node_array, list):
                log.error(
                    "Provenance tacking error: triton_kernel_to_post_grad_json value is not a list"
                )
                return empty_return
            for curr_node in node_array:
                post_to_cpp_code[curr_node].add(outer_key)

        def convert_sets_to_lists(d: dict[str, Any]) -> None:
            for key in d:
                d[key] = list(d[key])
            d = dict(d)

        # convert to list because set is not JSON serializable
        convert_sets_to_lists(post_to_cpp_code)
        return {
            "cppCodeToPost": triton_kernel_to_post_grad_json,
            "postToCppCode": post_to_cpp_code,
        }
    except Exception as e:
        # Since this is just logging code, it should never interfere with regular
        # program execution, so we use this try-except to guard against any error
        signpost_event(
            "inductor",
            "provenance_tracking_error",
            {
                "function": "create_mapping_kernel_to_post_grad",
                "error_msg": str(e),
                "stack_trace": traceback.format_exc(),
            },
        )
        log.error(
            "triton_kernel_to_post_grad_json:  %s", triton_kernel_to_post_grad_json
        )
        return empty_return

