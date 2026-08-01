
def s3_bucket_public_with_data(
    s3_bucket_public, tips_file, jsonl_file, feather_file, xml_file
):
    """
    The following datasets
    are loaded.

    - tips.csv
    - tips.csv.gz
    - tips.csv.bz2
    - items.jsonl
    """
    test_s3_files = [
        ("tips#1.csv", tips_file),
        ("tips.csv", tips_file),
        ("tips.csv.gz", tips_file + ".gz"),
        ("tips.csv.bz2", tips_file + ".bz2"),
        ("items.jsonl", jsonl_file),
        ("simple_dataset.feather", feather_file),
        ("books.xml", xml_file),
    ]
    for s3_key, file_name in test_s3_files:
        with open(file_name, "rb") as f:
            s3_bucket_public.put_object(Key=s3_key, Body=f)
    return s3_bucket_public

