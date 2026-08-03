import re

def normalize_request_route(route: str) -> str:
    """
    Normalize request routes by replacing dynamic path parameters with placeholders.

    This prevents high cardinality in Prometheus metrics by collapsing routes like:
    - /v1/responses/1234567890 -> /v1/responses/{response_id}
    - /v1/threads/thread_123 -> /v1/threads/{thread_id}

    Args:
        route: The request route path

    Returns:
        Normalized route with dynamic parameters replaced by placeholders

    Examples:
        >>> normalize_request_route("/v1/responses/abc123")
        '/v1/responses/{response_id}'
        >>> normalize_request_route("/v1/responses/abc123/cancel")
        '/v1/responses/{response_id}/cancel'
        >>> normalize_request_route("/chat/completions")
        '/chat/completions'
    """
    # Define patterns for routes with dynamic IDs
    # Format: (regex_pattern, replacement_template)
    patterns = [
        # Responses API - must come before generic patterns
        (r"^(/(?:openai/)?v1/responses)/([^/]+)(/input_items)$", r"\1/{response_id}\3"),
        (r"^(/(?:openai/)?v1/responses)/([^/]+)(/cancel)$", r"\1/{response_id}\3"),
        (r"^(/(?:openai/)?v1/responses)/([^/]+)$", r"\1/{response_id}"),
        (r"^(/responses)/([^/]+)(/input_items)$", r"\1/{response_id}\3"),
        (r"^(/responses)/([^/]+)(/cancel)$", r"\1/{response_id}\3"),
        (r"^(/responses)/([^/]+)$", r"\1/{response_id}"),
        # Threads API
        (
            r"^(/(?:openai/)?v1/threads)/([^/]+)(/runs)/([^/]+)(/steps)/([^/]+)$",
            r"\1/{thread_id}\3/{run_id}\5/{step_id}",
        ),
        (
            r"^(/(?:openai/)?v1/threads)/([^/]+)(/runs)/([^/]+)(/steps)$",
            r"\1/{thread_id}\3/{run_id}\5",
        ),
        (
            r"^(/(?:openai/)?v1/threads)/([^/]+)(/runs)/([^/]+)(/cancel)$",
            r"\1/{thread_id}\3/{run_id}\5",
        ),
        (
            r"^(/(?:openai/)?v1/threads)/([^/]+)(/runs)/([^/]+)(/submit_tool_outputs)$",
            r"\1/{thread_id}\3/{run_id}\5",
        ),
        (
            r"^(/(?:openai/)?v1/threads)/([^/]+)(/runs)/([^/]+)$",
            r"\1/{thread_id}\3/{run_id}",
        ),
        (r"^(/(?:openai/)?v1/threads)/([^/]+)(/runs)$", r"\1/{thread_id}\3"),
        (
            r"^(/(?:openai/)?v1/threads)/([^/]+)(/messages)/([^/]+)$",
            r"\1/{thread_id}\3/{message_id}",
        ),
        (r"^(/(?:openai/)?v1/threads)/([^/]+)(/messages)$", r"\1/{thread_id}\3"),
        (r"^(/(?:openai/)?v1/threads)/([^/]+)$", r"\1/{thread_id}"),
        # Vector Stores API
        (
            r"^(/(?:openai/)?v1/vector_stores)/([^/]+)(/files)/([^/]+)$",
            r"\1/{vector_store_id}\3/{file_id}",
        ),
        (
            r"^(/(?:openai/)?v1/vector_stores)/([^/]+)(/files)$",
            r"\1/{vector_store_id}\3",
        ),
        (
            r"^(/(?:openai/)?v1/vector_stores)/([^/]+)(/file_batches)/([^/]+)$",
            r"\1/{vector_store_id}\3/{batch_id}",
        ),
        (
            r"^(/(?:openai/)?v1/vector_stores)/([^/]+)(/file_batches)$",
            r"\1/{vector_store_id}\3",
        ),
        (r"^(/(?:openai/)?v1/vector_stores)/([^/]+)$", r"\1/{vector_store_id}"),
        # Assistants API
        (r"^(/(?:openai/)?v1/assistants)/([^/]+)$", r"\1/{assistant_id}"),
        # Files API
        (r"^(/(?:openai/)?v1/files)/([^/]+)(/content)$", r"\1/{file_id}\3"),
        (r"^(/(?:openai/)?v1/files)/([^/]+)$", r"\1/{file_id}"),
        # Batches API
        (r"^(/(?:openai/)?v1/batches)/([^/]+)(/cancel)$", r"\1/{batch_id}\3"),
        (r"^(/(?:openai/)?v1/batches)/([^/]+)$", r"\1/{batch_id}"),
        # Fine-tuning API
        (
            r"^(/(?:openai/)?v1/fine_tuning/jobs)/([^/]+)(/events)$",
            r"\1/{fine_tuning_job_id}\3",
        ),
        (
            r"^(/(?:openai/)?v1/fine_tuning/jobs)/([^/]+)(/cancel)$",
            r"\1/{fine_tuning_job_id}\3",
        ),
        (
            r"^(/(?:openai/)?v1/fine_tuning/jobs)/([^/]+)(/checkpoints)$",
            r"\1/{fine_tuning_job_id}\3",
        ),
        (r"^(/(?:openai/)?v1/fine_tuning/jobs)/([^/]+)$", r"\1/{fine_tuning_job_id}"),
        # Models API
        (r"^(/(?:openai/)?v1/models)/([^/]+)$", r"\1/{model}"),
    ]

    # Apply patterns in order
    for pattern, replacement in patterns:
        normalized = re.sub(pattern, replacement, route)
        if normalized != route:
            return normalized

    # Return original route if no pattern matched
    return route

