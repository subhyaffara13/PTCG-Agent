import os

def download_python_file_from_s3(
    bucket_name: str,
    object_key: str,
    local_file_path: str,
) -> bool:
    """
    Download a Python file from S3 and save it to local filesystem.

    Args:
        bucket_name (str): S3 bucket name
        object_key (str): S3 object key (file path in bucket)
        local_file_path (str): Local path where file should be saved

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import boto3
        from botocore.credentials import Credentials

        from litellm.llms.bedrock.base_aws_llm import BaseAWSLLM

        base_aws_llm = BaseAWSLLM()

        credentials: Credentials = base_aws_llm.get_credentials()
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=credentials.access_key,
            aws_secret_access_key=credentials.secret_key,
            aws_session_token=credentials.token,
        )

        verbose_proxy_logger.debug(
            f"Downloading Python file {object_key} from S3 bucket: {bucket_name}"
        )
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)

        # Read the file contents
        file_contents = response["Body"].read().decode("utf-8")
        verbose_proxy_logger.debug(f"File contents: {file_contents}")

        # Ensure directory exists
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

        # Write to local file
        with open(local_file_path, "w") as f:
            f.write(file_contents)

        verbose_proxy_logger.debug(
            f"Python file downloaded successfully to {local_file_path}"
        )
        return True

    except ImportError as e:
        verbose_proxy_logger.error(f"ImportError: {str(e)}")
        return False
    except Exception as e:
        verbose_proxy_logger.exception(f"Error downloading Python file: {str(e)}")
        return False

