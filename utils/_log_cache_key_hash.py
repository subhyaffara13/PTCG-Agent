
def _log_cache_key_hash(hash_obj, last_serialized: str, hashfn):
  if logger.isEnabledFor(logging.DEBUG):
    # Log the hash of just this entry
    fresh_hash_obj = hashlib.sha256()
    hashfn(fresh_hash_obj)
    logger.debug(
        "get_cache_key hash of serialized %s: %s",
        last_serialized,
        fresh_hash_obj.digest().hex(),
    )
    # Log the cumulative hash
    logger.debug(
        "get_cache_key hash after serializing %s: %s",
        last_serialized,
        hash_obj.digest().hex(),
    )

