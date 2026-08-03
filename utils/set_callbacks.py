import os
import subprocess
import sys

def set_callbacks(callback_list, function_id=None):
    """
    Globally sets the callback client
    """
    global sentry_sdk_instance, capture_exception, add_breadcrumb, slack_app, alerts_channel, traceloopLogger, athinaLogger, heliconeLogger, supabaseClient, lunaryLogger, promptLayerLogger, langFuseLogger, customLogger, weightsBiasesLogger, logfireLogger, dynamoLogger, s3Logger, dataDogLogger, prometheusLogger, greenscaleLogger, openMeterLogger, deepevalLogger

    try:
        for callback in callback_list:
            if callback == "sentry":
                try:
                    import sentry_sdk
                except ImportError:
                    print_verbose("Package 'sentry_sdk' is missing. Installing it...")
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", "sentry_sdk"]
                    )
                    import sentry_sdk
                from sentry_sdk.scrubber import EventScrubber

                sentry_sdk_instance = sentry_sdk
                sentry_trace_rate = (
                    os.environ.get("SENTRY_API_TRACE_RATE")
                    if "SENTRY_API_TRACE_RATE" in os.environ
                    else "1.0"
                )
                sentry_sample_rate = (
                    os.environ.get("SENTRY_API_SAMPLE_RATE")
                    if "SENTRY_API_SAMPLE_RATE" in os.environ
                    else "1.0"
                )
                sentry_sdk_instance.init(
                    dsn=os.environ.get("SENTRY_DSN"),
                    traces_sample_rate=float(sentry_trace_rate),  # type: ignore
                    sample_rate=float(
                        sentry_sample_rate if sentry_sample_rate else 1.0
                    ),
                    send_default_pii=False,  # Prevent sending Personal Identifiable Information
                    event_scrubber=EventScrubber(
                        denylist=SENTRY_DENYLIST, pii_denylist=SENTRY_PII_DENYLIST
                    ),
                    environment=os.environ.get("SENTRY_ENVIRONMENT", "production"),
                )
                capture_exception = sentry_sdk_instance.capture_exception
                add_breadcrumb = sentry_sdk_instance.add_breadcrumb
            elif callback == "slack":
                try:
                    from slack_bolt import App
                except ImportError:
                    print_verbose("Package 'slack_bolt' is missing. Installing it...")
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", "slack_bolt"]
                    )
                    from slack_bolt import App
                slack_app = App(
                    token=os.environ.get("SLACK_API_TOKEN"),
                    signing_secret=os.environ.get("SLACK_API_SECRET"),
                )
                alerts_channel = os.environ["SLACK_API_CHANNEL"]
                print_verbose(f"Initialized Slack App: {slack_app}")
            elif callback == "traceloop":
                traceloopLogger = TraceloopLogger()
            elif callback == "athina":
                athinaLogger = AthinaLogger()
                print_verbose("Initialized Athina Logger")
            elif callback == "helicone":
                heliconeLogger = HeliconeLogger()
            elif callback == "lunary":
                lunaryLogger = LunaryLogger()
            elif callback == "promptlayer":
                promptLayerLogger = PromptLayerLogger()
            elif callback == "langfuse":
                langFuseLogger = LangFuseLogger(
                    langfuse_public_key=None, langfuse_secret=None, langfuse_host=None
                )
            elif callback == "openmeter":
                openMeterLogger = OpenMeterLogger()
            elif callback == "datadog":
                dataDogLogger = DataDogLogger()
            elif callback == "dynamodb":
                dynamoLogger = DyanmoDBLogger()
            elif callback == "s3":
                s3Logger = S3Logger()
            elif callback == "wandb":
                from litellm.integrations.weights_biases import WeightsBiasesLogger

                weightsBiasesLogger = WeightsBiasesLogger()
            elif callback == "logfire":
                logfireLogger = LogfireLogger()
            elif callback == "supabase":
                print_verbose("instantiating supabase")
                supabaseClient = Supabase()
            elif callback == "greenscale":
                greenscaleLogger = GreenscaleLogger()
                print_verbose("Initialized Greenscale Logger")
            elif callable(callback):
                customLogger = CustomLogger()
    except Exception as e:
        raise e
    return None

