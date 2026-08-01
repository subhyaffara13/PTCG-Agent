
def add_skipped_file_notifications(skips, invocation):
    if skips is None or len(skips) == 0:
        return

    if invocation.tool_configuration_notifications is None:
        invocation.tool_configuration_notifications = []

    for skip in skips:
        (file_name, reason) = skip

        notification = om.Notification(
            level="error",
            message=om.Message(text=reason),
            locations=[
                om.Location(
                    physical_location=om.PhysicalLocation(
                        artifact_location=om.ArtifactLocation(
                            uri=to_uri(file_name)
                        )
                    )
                )
            ],
        )

        invocation.tool_configuration_notifications.append(notification)

