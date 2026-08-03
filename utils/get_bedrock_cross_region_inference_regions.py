from typing import List

def get_bedrock_cross_region_inference_regions() -> List[str]:
    """Abbreviations of regions AWS Bedrock supports for cross region inference."""
    return ["global", "us", "eu", "apac", "jp", "au", "us-gov"]

