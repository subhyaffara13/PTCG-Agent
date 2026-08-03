from typing import Optional

def get_hf_task_embedding_for_model(
    model: str, task_type: Optional[str], api_base: str
) -> Optional[str]:
    if task_type is not None:
        if task_type in get_args(hf_tasks_embeddings):
            return task_type
        else:
            raise Exception(
                "Invalid task_type={}. Expected one of={}".format(
                    task_type, hf_tasks_embeddings
                )
            )
    http_client = HTTPHandler(concurrent_limit=1)

    model_info = http_client.get(url=f"{api_base}/api/models/{model}")

    model_info_dict = model_info.json()

    pipeline_tag: Optional[str] = model_info_dict.get("pipeline_tag", None)

    return pipeline_tag

