import os
import uuid
from pathlib import Path


def _cache_commit_hash_for_specific_revision(storage_folder: str, revision: str, commit_hash: str) -> None:
    """Cache reference between a revision (tag, branch or truncated commit hash) and the corresponding commit hash.

    Does nothing if `revision` is already a proper `commit_hash` or reference is already cached.
    """
    if revision != commit_hash:
        ref_path = Path(storage_folder) / "refs" / revision
        ref_path.parent.mkdir(parents=True, exist_ok=True)
        if not ref_path.exists() or commit_hash != ref_path.read_text():
            # Update ref only if has been updated. Could cause useless error in case
            # repo is already cached and user doesn't have write access to cache folder.
            # See https://github.com/huggingface/huggingface_hub/issues/1216.
            # Write atomically (tmp file + rename) so that concurrent readers never see
            # a partially written ref.
            tmp_path = ref_path.with_name(f"{ref_path.name}.{uuid.uuid4().hex[:8]}.tmp")
            tmp_path.write_text(commit_hash)
            os.replace(tmp_path, ref_path)

