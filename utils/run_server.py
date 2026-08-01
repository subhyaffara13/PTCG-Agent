
def run_server(
    cli_args,
    host,
    port,
    api_base,
    api_version,
    model,
    alias,
    add_key,
    headers,
    save,
    debug,
    detailed_debug,
    temperature,
    max_tokens,
    request_timeout,
    drop_params,
    add_function_to_prompt,
    config,
    max_budget,
    telemetry,
    test,
    local,
    num_workers,
    granian_threads,
    test_async,
    iam_token_db_auth,
    num_requests,
    use_queue,
    health,
    setup,
    version,
    run_gunicorn,
    run_hypercorn,
    run_granian,
    ssl_keyfile_path,
    ssl_certfile_path,
    ciphers,
    log_config,
    use_prisma_db_push: bool,
    skip_server_startup,
    keepalive_timeout,
    timeout_worker_healthcheck,
    max_requests_before_restart,
    max_requests_before_restart_jitter: Optional[int],
    enforce_prisma_migration_check: bool,
    use_v2_migration_resolver: bool,
    reload: bool,
):
    if cli_args:
        if cli_args == ("xai-oauth", "login"):
            from litellm.llms.xai.oauth import XAIOAuthAuthenticator

            authenticator = XAIOAuthAuthenticator()
            auth_data = authenticator.login()
            click.echo(
                f"xAI OAuth login successful. Credentials saved to {authenticator.auth_file}."
            )
            if auth_data.get("expires_at"):
                click.echo(f"Access token expires at {auth_data['expires_at']}.")
            return
        raise click.UsageError(f"Unknown command: {' '.join(cli_args)}")

    if setup:
        from litellm.setup_wizard import run_setup_wizard

        run_setup_wizard()
        return

    args = locals()
    if local:
        from proxy_server import (
            KeyManagementSettings,
            ProxyConfig,
            app,
            save_worker_config,
        )
    else:
        try:
            from .proxy_server import (
                KeyManagementSettings,
                ProxyConfig,
                app,
                save_worker_config,
            )
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(
                f"Missing dependency {e}. Run `pip install 'litellm[proxy]'`"
            )
        except ImportError as e:
            if "litellm[proxy]" in str(e):
                # user is missing a proxy dependency, ask them to pip install litellm[proxy]
                raise e
            else:
                # this is just a local/relative import error, user git cloned litellm
                from proxy_server import (
                    KeyManagementSettings,
                    ProxyConfig,
                    app,
                    save_worker_config,
                )
    if version is True:
        ProxyInitializationHelpers._echo_litellm_version()
        return
    if model and "ollama" in model and api_base is None:
        ProxyInitializationHelpers._run_ollama_serve()
    if health is True:
        ProxyInitializationHelpers._run_health_check(host, port)
        return
    if test is True:
        ProxyInitializationHelpers._run_test_chat_completion(host, port, model, test)
        return
    else:
        if headers:
            headers = json.loads(headers)
        save_worker_config(
            model=model,
            alias=alias,
            api_base=api_base,
            api_version=api_version,
            debug=debug,
            detailed_debug=detailed_debug,
            temperature=temperature,
            max_tokens=max_tokens,
            request_timeout=request_timeout,
            max_budget=max_budget,
            telemetry=telemetry,
            drop_params=drop_params,
            add_function_to_prompt=add_function_to_prompt,
            headers=headers,
            save=save,
            config=config,
            use_queue=use_queue,
        )
        if run_granian:
            try:
                import granian  # noqa: F401
            except ImportError as e:
                raise ImportError(
                    "granian must be installed to use --run_granian. "
                    "Run `pip install granian` or `pip install 'litellm[proxy]'` "
                    "(Granian requires Python 3.10+)."
                ) from e
        else:
            try:
                import uvicorn
            except Exception:
                raise ImportError(
                    "uvicorn, gunicorn needs to be imported. Run - `pip install 'litellm[proxy]'`"
                )

        db_connection_pool_limit = 100
        # Starts optional due to config fallback checks; guaranteed non-None before use.
        db_connection_timeout: Optional[Union[int, float]] = 60
        db_connect_timeout: Optional[Union[int, float]] = None
        db_socket_timeout: Optional[Union[int, float]] = None
        db_disable_prepared_statements: bool = False
        db_extra_connection_params: Optional[dict] = None
        general_settings = {}
        ### GET DB TOKEN FOR IAM AUTH ###

        if iam_token_db_auth or get_secret_bool("IAM_TOKEN_DB_AUTH"):
            from litellm.proxy.auth.rds_iam_token import generate_iam_auth_token

            db_host = os.getenv("DATABASE_HOST")
            # Default to the Postgres standard port. Without a default,
            # `db_port=None` flows into `boto.generate_db_auth_token(Port=None)`
            # and botocore stringifies it to `"None"` while building the
            # presigned URL, which then blows up with `ValueError: Port could
            # not be cast to integer value as 'None'` during signing.
            db_port = os.getenv("DATABASE_PORT", "5432")
            db_user = os.getenv("DATABASE_USER")
            db_name = os.getenv("DATABASE_NAME")
            db_schema = os.getenv("DATABASE_SCHEMA")

            token = generate_iam_auth_token(
                db_host=db_host, db_port=db_port, db_user=db_user
            )

            # print(f"token: {token}")
            _db_url = f"postgresql://{db_user}:{token}@{db_host}:{db_port}/{db_name}"
            if db_schema:
                _db_url += f"?schema={db_schema}"

            os.environ["DATABASE_URL"] = _db_url
            os.environ["IAM_TOKEN_DB_AUTH"] = "True"

        ### DECRYPT ENV VAR ###

        from litellm.secret_managers.aws_secret_manager import decrypt_env_var

        if (
            os.getenv("USE_AWS_KMS", None) is not None
            and os.getenv("USE_AWS_KMS") == "True"
        ):
            ## V2 IMPLEMENTATION OF AWS KMS - USER WANTS TO DECRYPT MULTIPLE KEYS IN THEIR ENV
            new_env_var = decrypt_env_var()

            for k, v in new_env_var.items():
                os.environ[k] = v

        litellm_settings = None
        if config is not None:
            """
            Allow user to pass in db url via config

            read from there and save it to os.env['DATABASE_URL']
            """
            try:
                import asyncio

            except Exception:
                raise ImportError(
                    "yaml needs to be imported. Run - `pip install 'litellm[proxy]'`"
                )

            proxy_config = ProxyConfig()
            _config = asyncio.run(proxy_config.get_config(config_file_path=config))

            ### LITELLM SETTINGS ###
            litellm_settings = _config.get("litellm_settings", None)
            if (
                litellm_settings is not None
                and "json_logs" in litellm_settings
                and litellm_settings["json_logs"] is True
            ):
                import litellm

                litellm.json_logs = True

                litellm._turn_on_json()
            ### GENERAL SETTINGS ###
            general_settings = _config.get("general_settings", {})
            if general_settings is None:
                general_settings = {}
            ### LOAD KEY MANAGEMENT SETTINGS FIRST (needed for custom secret manager) ###
            key_management_settings = general_settings.get(
                "key_management_settings", None
            )
            if key_management_settings is not None:
                import litellm

                litellm._key_management_settings = KeyManagementSettings(
                    **key_management_settings
                )

            if general_settings:
                ### LOAD SECRET MANAGER ###
                key_management_system = general_settings.get(
                    "key_management_system", None
                )
                proxy_config.initialize_secret_manager(
                    key_management_system=key_management_system, config_file_path=config
                )
            database_url = general_settings.get("database_url", None)
            if database_url is None and os.getenv("DATABASE_URL") is None:
                # Use helper function to construct DATABASE_URL from individual variables
                from litellm.proxy.utils import construct_database_url_from_env_vars

                database_url = construct_database_url_from_env_vars()
                if database_url:
                    os.environ["DATABASE_URL"] = database_url
            db_connection_pool_limit = general_settings.get(
                "database_connection_pool_limit",
                LiteLLMDatabaseConnectionPool.database_connection_pool_limit.value,
            )
            db_connection_timeout = general_settings.get("database_connection_timeout")
            if db_connection_timeout is None:
                db_connection_timeout = general_settings.get(
                    "database_connection_pool_timeout"
                )
            if db_connection_timeout is None:
                db_connection_timeout = (
                    LiteLLMDatabaseConnectionPool.database_connection_pool_timeout.value
                )
            db_connect_timeout = general_settings.get("database_connect_timeout")
            db_socket_timeout = general_settings.get("database_socket_timeout")
            _disable_prepared_statements = general_settings.get(
                "database_disable_prepared_statements", False
            )
            if isinstance(_disable_prepared_statements, str):
                from litellm.secret_managers.main import str_to_bool

                db_disable_prepared_statements = (
                    str_to_bool(_disable_prepared_statements) is True
                )
            else:
                db_disable_prepared_statements = bool(_disable_prepared_statements)
            db_extra_connection_params = general_settings.get(
                "database_extra_connection_params"
            )
            if database_url and database_url.startswith("os.environ/"):
                original_dir = os.getcwd()
                # set the working directory to where this script is
                sys.path.insert(
                    0, os.path.abspath("../..")
                )  # Adds the parent directory to the system path - for litellm local dev
                import litellm
                from litellm import get_secret_str

                database_url = get_secret_str(database_url, default_value=None)
                os.chdir(original_dir)
            if database_url is not None and isinstance(database_url, str):
                os.environ["DATABASE_URL"] = database_url

        # Handle database URL construction when no config file is used
        if config is None and os.getenv("DATABASE_URL") is None:
            # Use helper function to construct DATABASE_URL from individual variables
            from litellm.proxy.utils import construct_database_url_from_env_vars

            database_url = construct_database_url_from_env_vars()
            if database_url:
                os.environ["DATABASE_URL"] = database_url

        # Set default values for connection pool settings when no config is used
        if config is None:
            db_connection_pool_limit = (
                LiteLLMDatabaseConnectionPool.database_connection_pool_limit.value
            )
            db_connection_timeout = (
                LiteLLMDatabaseConnectionPool.database_connection_pool_timeout.value
            )

        if (
            os.getenv("DATABASE_URL", None) is not None
            or os.getenv("DIRECT_URL", None) is not None
        ):
            try:
                from litellm.secret_managers.main import get_secret

                connection_url_params = _build_db_connection_url_params(
                    connection_limit=db_connection_pool_limit,
                    pool_timeout=db_connection_timeout,
                    connect_timeout=db_connect_timeout,
                    socket_timeout=db_socket_timeout,
                    disable_prepared_statements=db_disable_prepared_statements,
                    extra_params=db_extra_connection_params,
                )
                if os.getenv("DATABASE_URL", None) is not None:
                    database_url = get_secret("DATABASE_URL", default_value=None)
                    modified_url = append_query_params(
                        str(database_url) if database_url else None,
                        connection_url_params,
                    )
                    os.environ["DATABASE_URL"] = modified_url
                if os.getenv("DIRECT_URL", None) is not None:
                    database_url = os.getenv("DIRECT_URL")
                    modified_url = append_query_params(
                        database_url, connection_url_params
                    )
                    os.environ["DIRECT_URL"] = modified_url
                subprocess.run(["prisma"], capture_output=True)
                is_prisma_runnable = True
            except FileNotFoundError:
                is_prisma_runnable = False

            if is_prisma_runnable:
                from litellm.proxy.db.check_migration import check_prisma_schema_diff
                from litellm.proxy.db.prisma_client import (
                    PrismaManager,
                    should_update_prisma_schema,
                )

                if (
                    should_update_prisma_schema(
                        general_settings.get("disable_prisma_schema_update")
                    )
                    is False
                ):
                    check_prisma_schema_diff(db_url=None)
                else:
                    if not use_v2_migration_resolver:
                        print(
                            "\033[1;33mLiteLLM Proxy: Using default (v1) migration resolver. "
                            "If your deployment has seen schema thrashing during rolling "
                            "deploys, try --use_v2_migration_resolver (safer: avoids the "
                            "diff-and-force recovery that caused the thrash).\033[0m"
                        )
                    try:
                        setup_ok = PrismaManager.setup_database(
                            use_migrate=not use_prisma_db_push,
                            use_v2_resolver=use_v2_migration_resolver,
                        )
                    except RuntimeError as e:
                        # v2 resolver raises on unrecoverable migration errors
                        # (e.g. non-idempotent failures, permission issues).
                        # v1 never raises here, so this only fires when the
                        # operator opted into v2.
                        print(
                            "\033[1;31mLiteLLM Proxy: Database migration cannot proceed. "
                            f"{e}\033[0m",
                            file=sys.stderr,
                            flush=True,
                        )
                        sys.exit(2)
                    if not setup_ok:
                        if enforce_prisma_migration_check:
                            print(
                                "\033[1;31mLiteLLM Proxy: Database setup failed after multiple retries. "
                                "The proxy cannot start safely. Please check your database connection and migration status.\033[0m"
                            )
                            sys.exit(1)
                        else:
                            print(
                                "\033[1;33mLiteLLM Proxy: Database migration failed but continuing startup. "
                                "Set --enforce_prisma_migration_check or ENFORCE_PRISMA_MIGRATION_CHECK=true to exit on failure.\033[0m"
                            )
            else:
                print(
                    f"Unable to connect to DB. DATABASE_URL found in environment, but prisma package not found."  # noqa: F541
                )
        if port == 4000 and ProxyInitializationHelpers._is_port_in_use(port):
            port = random.randint(1024, 49152)

        import litellm

        if detailed_debug is True:
            litellm._turn_on_debug()

        # DO NOT DELETE - enables global variables to work across files
        from litellm.proxy.proxy_server import app

        # Auto-create PROMETHEUS_MULTIPROC_DIR for multi-worker setups
        ProxyInitializationHelpers._maybe_setup_prometheus_multiproc_dir(
            num_workers=num_workers,
            litellm_settings=litellm_settings if config else None,  # type: ignore[possibly-unbound]
        )

        # Skip server startup if requested (after all setup is done)
        if skip_server_startup:
            print("LiteLLM: Setup complete. Skipping server startup as requested.")
            return

        running_uvicorn = run_gunicorn is False and run_hypercorn is False
        uvicorn_args = ProxyInitializationHelpers._get_default_unvicorn_init_args(
            host=host,
            port=port,
            log_config=log_config,
            keepalive_timeout=keepalive_timeout,
            timeout_worker_healthcheck=(
                timeout_worker_healthcheck if running_uvicorn else None
            ),
        )
        # Optional: recycle uvicorn workers after N requests
        if max_requests_before_restart is not None:
            uvicorn_args["limit_max_requests"] = max_requests_before_restart
        if run_gunicorn is False and run_hypercorn is False and run_granian is False:
            if max_requests_before_restart_jitter is not None:
                ProxyInitializationHelpers._apply_uvicorn_max_requests_jitter(
                    uvicorn_args=uvicorn_args,
                    max_requests_before_restart=max_requests_before_restart,
                    jitter=max_requests_before_restart_jitter,
                )
            if ssl_certfile_path is not None and ssl_keyfile_path is not None:
                print(
                    f"\033[1;32mLiteLLM Proxy: Using SSL with certfile: {ssl_certfile_path} and keyfile: {ssl_keyfile_path}\033[0m\n"
                )
                uvicorn_args["ssl_keyfile"] = ssl_keyfile_path
                uvicorn_args["ssl_certfile"] = ssl_certfile_path

            loop_type = ProxyInitializationHelpers._get_loop_type()
            if loop_type:
                uvicorn_args["loop"] = loop_type

            if reload:
                ProxyInitializationHelpers._configure_dev_reload(uvicorn_args, config)

            uvicorn.run(
                **uvicorn_args,
                workers=num_workers,
            )
        elif run_gunicorn is True:
            ProxyInitializationHelpers._run_gunicorn_server(
                host=host,
                port=port,
                app=app,
                num_workers=num_workers,
                ssl_certfile_path=ssl_certfile_path,
                ssl_keyfile_path=ssl_keyfile_path,
                max_requests_before_restart=max_requests_before_restart,
                max_requests_before_restart_jitter=max_requests_before_restart_jitter,
            )
        elif run_hypercorn is True:
            ProxyInitializationHelpers._init_hypercorn_server(
                app=app,
                host=host,
                port=port,
                ssl_certfile_path=ssl_certfile_path,
                ssl_keyfile_path=ssl_keyfile_path,
                ciphers=ciphers,
            )
        elif run_granian is True:
            ProxyInitializationHelpers._init_granian_server(
                host=host,
                port=port,
                num_workers=num_workers,
                ssl_certfile_path=ssl_certfile_path,
                ssl_keyfile_path=ssl_keyfile_path,
                max_requests_before_restart=max_requests_before_restart,
                ciphers=ciphers,
                granian_runtime_threads=granian_threads,
            )

