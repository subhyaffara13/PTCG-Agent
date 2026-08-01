
def get_file_contents_from_s3(bucket_name, object_key):
    try:
        # v0 rely on boto3 for authentication - allowing boto3 to handle IAM credentials etc
        import boto3
        from botocore.credentials import Credentials

        from litellm.main import bedrock_converse_chat_completion

        credentials: Credentials = bedrock_converse_chat_completion.get_credentials()
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=credentials.access_key,
            aws_secret_access_key=credentials.secret_key,
            aws_session_token=credentials.token,  # Optional, if using temporary credentials
        )
        verbose_proxy_logger.debug(
            f"Retrieving {object_key} from S3 bucket: {bucket_name}"
        )
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        verbose_proxy_logger.debug(f"Response: {response}")

        # Read the file contents and directly parse YAML
        file_contents = response["Body"].read().decode("utf-8")
        verbose_proxy_logger.debug("File contents retrieved from S3")

        # Parse YAML directly from string
        config = yaml.safe_load(file_contents)
        return config

    except ImportError as e:
        # this is most likely if a user is not using the litellm docker container
        verbose_proxy_logger.error(f"ImportError: {str(e)}")
        pass
    except Exception as e:
        verbose_proxy_logger.error(f"Error retrieving file contents: {str(e)}")
        return None

