
def _looks_like_boto3_service_request(node: ClassDef) -> bool:
    return node.qname() == BOTO_SERVICE_FACTORY_QUALIFIED_NAME

