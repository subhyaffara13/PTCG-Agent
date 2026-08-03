from pathlib import Path


def migrate() -> bool:
    """Migrate IPython configuration to Jupyter"""
    env = {
        "jupyter_data": jupyter_data_dir(),
        "jupyter_config": jupyter_config_dir(),
        "ipython_dir": get_ipython_dir(),
        "profile": str(Path(get_ipython_dir(), "profile_default")),
    }
    migrated = False
    for src_t, dst_t in migrations.items():
        src = src_t.format(**env)
        dst = dst_t.format(**env)
        if Path(src).exists() and migrate_one(src, dst):
            migrated = True

    for name in config_migrations:
        if migrate_config(name, env):
            migrated = True

    custom_src = custom_src_t.format(**env)
    custom_dst = custom_dst_t.format(**env)

    if Path(custom_src).exists() and migrate_static_custom(custom_src, custom_dst):
        migrated = True

    # write a marker to avoid re-running migration checks
    ensure_dir_exists(env["jupyter_config"])
    with Path.open(Path(env["jupyter_config"], "migrated"), "w", encoding="utf-8") as f:
        f.write(datetime.now(tz=timezone.utc).isoformat())

    return migrated

