
def start():
    r"""Starts cuda profiler data collection.

    .. warning::
        Raises CudaError in case of it is unable to start the profiler.
    """
    check_error(cudart().cudaProfilerStart())


def start(mode: ProfilerMode = "interval", wait_until_completed: bool = False) -> None:
    r"""Start OS Signpost tracing from MPS backend.

    The generated OS Signposts could be recorded and viewed in
    XCode Instruments Logging tool.

    Args:
        mode(str): OS Signpost tracing mode could be "interval", "event",
            or both "interval,event".
            The interval mode traces the duration of execution of the operations,
            whereas event mode marks the completion of executions.
            See document `Recording Performance Data`_ for more info.
        wait_until_completed(bool): Waits until the MPS Stream complete
            executing each encoded GPU operation. This helps generating single
            dispatches on the trace's timeline.
            Note that enabling this option would affect the performance negatively.

    .. _Recording Performance Data:
       https://developer.apple.com/documentation/os/logging/recording_performance_data
    """
    mode_normalized = mode.lower().replace(" ", "")
    torch._C._mps_profilerStartTrace(  # type: ignore[attr-defined]
        mode_normalized, wait_until_completed
    )


def Start(builder):
    ArgTypeAndIndexStart(builder)


def Start(builder):
    AttributeStart(builder)


def Start(builder):
    CheckpointStart(builder)


def Start(builder):
    DeprecatedKernelCreateInfosStart(builder)


def Start(builder):
    DeprecatedNodeIndexAndKernelDefHashStart(builder)


def Start(builder):
    DeprecatedSessionStateStart(builder)


def Start(builder):
    DeprecatedSubGraphSessionStateStart(builder)


def Start(builder):
    DimensionStart(builder)


def Start(builder):
    DimensionValueStart(builder)


def Start(builder):
    FloatPropertyStart(builder)


def Start(builder):
    GraphStart(builder)


def Start(builder):
    InferenceSessionStart(builder)


def Start(builder):
    IntPropertyStart(builder)


def Start(builder):
    KernelTypeStrArgsEntryStart(builder)


def Start(builder):
    KernelTypeStrResolverStart(builder)


def Start(builder):
    MapTypeStart(builder)


def Start(builder):
    ModelStart(builder)


def Start(builder):
    ModuleStateStart(builder)


def Start(builder):
    NodeStart(builder)


def Start(builder):
    NodeEdgeStart(builder)


def Start(builder):
    NodesToOptimizeIndicesStart(builder)


def Start(builder):
    OperatorSetIdStart(builder)


def Start(builder):
    OpIdKernelTypeStrArgsEntryStart(builder)


def Start(builder):
    OptimizerGroupStart(builder)


def Start(builder):
    ParameterOptimizerStateStart(builder)


def Start(builder):
    PropertyBagStart(builder)


def Start(builder):
    RuntimeOptimizationRecordStart(builder)


def Start(builder):
    RuntimeOptimizationRecordContainerEntryStart(builder)


def Start(builder):
    RuntimeOptimizationsStart(builder)


def Start(builder):
    SequenceTypeStart(builder)


def Start(builder):
    ShapeStart(builder)


def Start(builder):
    SparseTensorStart(builder)


def Start(builder):
    StringPropertyStart(builder)


def Start(builder):
    StringStringEntryStart(builder)


def Start(builder):
    TensorStart(builder)


def Start(builder):
    TensorTypeAndShapeStart(builder)


def Start(builder):
    TypeInfoStart(builder)


def Start(builder):
    ValueInfoStart(builder)


def Start(builder):  # noqa: N802
    builder.StartObject(2)


def Start(builder):  # noqa: N802
    builder.StartObject(1)

