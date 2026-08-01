
def _handle_async_invoke_status(
    batch_id: str, aws_region_name: str, logging_obj=None, **kwargs
) -> "LiteLLMBatch":
    """
    Handle async invoke status check for AWS Bedrock.

    Args:
        batch_id: The async invoke ARN
        aws_region_name: AWS region name
        **kwargs: Additional parameters

    Returns:
        dict: Status information including status, output_file_id (S3 URL), etc.
    """
    import asyncio

    from litellm.llms.bedrock.embed.embedding import BedrockEmbedding

    async def _async_get_status():
        # Create embedding handler instance
        embedding_handler = BedrockEmbedding()

        # Get the status of the async invoke job
        status_response = await embedding_handler._get_async_invoke_status(
            invocation_arn=batch_id,
            aws_region_name=aws_region_name,
            logging_obj=logging_obj,
            **kwargs,
        )

        # Transform response to a LiteLLMBatch object
        from litellm.types.llms.openai import BatchJobStatus
        from litellm.types.utils import LiteLLMBatch

        # Normalize status to lowercase (AWS returns 'Completed', 'Failed', etc.)
        aws_status_raw = status_response.get("status", "")
        aws_status_lower = aws_status_raw.lower()
        # Map AWS status values to LiteLLM expected values
        status_mapping: dict[str, BatchJobStatus] = {
            "completed": "completed",
            "failed": "failed",
            "inprogress": "in_progress",
            "in_progress": "in_progress",
        }
        normalized_status: BatchJobStatus = status_mapping.get(
            aws_status_lower, "failed"
        )  # Default to "failed" if unknown status

        # Get output S3 URI safely
        output_s3_uri = ""
        try:
            output_s3_uri = status_response["outputDataConfig"]["s3OutputDataConfig"][
                "s3Uri"
            ]
        except (KeyError, TypeError):
            pass

        # Use BedrockBatchesConfig's timestamp parsing method (expects raw AWS status string)
        import time

        from litellm.llms.bedrock.batches.transformation import BedrockBatchesConfig

        (
            created_at,
            in_progress_at,
            completed_at,
            failed_at,
            _,
            _,
        ) = BedrockBatchesConfig()._parse_timestamps_and_status(
            status_response, aws_status_raw
        )
        result = LiteLLMBatch(
            id=status_response["invocationArn"],
            object="batch",
            status=normalized_status,
            created_at=created_at
            or int(time.time()),  # Provide default timestamp if None
            in_progress_at=in_progress_at,
            completed_at=completed_at,
            failed_at=failed_at,
            request_counts=BatchRequestCounts(
                total=1,
                completed=1 if normalized_status == "completed" else 0,
                failed=1 if normalized_status == "failed" else 0,
            ),
            metadata=dict(
                **{
                    "output_file_id": output_s3_uri,
                    "failure_message": status_response.get("failureMessage") or "",
                    "model_arn": status_response["modelArn"],
                }
            ),
            completion_window="24h",
            endpoint="/v1/embeddings",
            input_file_id="",
        )

        return result

    # Since this function is called from within an async context via run_in_executor,
    # we need to create a new event loop in a thread to avoid conflicts
    import concurrent.futures

    def run_in_thread():
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        try:
            return new_loop.run_until_complete(_async_get_status())
        finally:
            new_loop.close()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(run_in_thread)
        return future.result()

