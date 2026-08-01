
def get_item_date(item: ListingItem) -> datetime | None:
    """Extract date from an item, supporting both repo items (last_commit.date) and bucket items (mtime/uploaded_at)."""
    match item:
        case BucketFile(mtime=mtime) if mtime is not None:
            return mtime
        case BucketFile(uploaded_at=uploaded_at) | BucketFolder(uploaded_at=uploaded_at) if uploaded_at is not None:
            return uploaded_at
        case RepoFile(last_commit=last_commit) | RepoFolder(last_commit=last_commit) if last_commit is not None:
            return last_commit.date
        case _:
            return None

