
def _create_operator_type_usage_processors():
    """
    Create a set of processors that determine the required types for all enabled operators.
    :return: Dictionary of operator key to processor. Key is 'domain:operator (e.g. ai.onnx:Cast)'.
    """
    operator_processors = {}

    def add(processor):
        if processor.name in operator_processors:
            raise RuntimeError("Duplicate processor for " + processor.name)

        operator_processors[processor.name] = processor

    # Starting with ops from:
    #   - Priority 1P models
    #   - Mobilenet + SSD Mobilenet + MobileBert
    #   - some known large kernels
    #
    # Ops we are ignoring currently so as not to produce meaningless/unused output:
    # - Implementation is type agnostic:
    #    ai.onnx: If, Loop, Reshape, Scan, Shape, Squeeze, Tile, Unsqueeze
    #    com.microsoft: DynamicQuantizeMatMul, MatMulIntegerToFloat
    # - Only one type supported in the ORT implementation:
    #    ai.onnx: NonMaxSuppression
    #    com.microsoft: FusedConv, FusedGemm, FusedMatMul
    # - Implementation does not have any significant type specific code:
    #    ai.onnx: Concat, Flatten, Not, Reshape, Shape, Squeeze, Unsqueeze
    #
    default_processor_onnx_ops = [
        "Abs",
        "ArgMax",
        "ArgMin",
        "AveragePool",
        "BatchNormalization",
        "BitShift",
        "Ceil",
        "Clip",
        "Conv",
        "CumSum",
        "Exp",
        "Expand",
        "Floor",
        "Gemm",
        "IsNaN",
        "Log",
        "LogSoftmax",
        "LpNormalization",
        "MatMul",
        "Max",
        "MaxPool",
        "Mean",
        "Min",
        "NonZero",
        "Pad",
        "QLinearConv",
        "QLinearMatMul",
        "Range",
        "Reciprocal",
        "ReduceL1",
        "ReduceL2",
        "ReduceLogSum",
        "ReduceLogSumExp",
        "ReduceMax",
        "ReduceMean",
        "ReduceMin",
        "ReduceProd",
        "ReduceSum",
        "ReduceSumSquare",
        "Relu",
        "Resize",
        "ReverseSequence",
        "RoiAlign",
        "Round",
        "Scatter",
        "ScatterElements",
        "ScatterND",
        "Shrink",
        "Sigmoid",
        "Sign",
        "Sin",
        "Softmax",
        "Split",
        "SplitToSequence",
        "Sqrt",
        "Sum",
        "Tanh",
        "TopK",
        "Transpose",
        "Unique",
    ]

    # ops that are used to manipulate shapes or indices so require int32_t and int64_t to be available
    default_processor_onnx_ops_requiring_ints_for_input_0 = [
        "Add",
        "Concat",
        "Div",
        "Equal",
        "Greater",
        "Less",
        "Mul",
        "Neg",  # used in tflite TransposeConv conversion
        "Sub",
    ]

    # NOTE: QLinearConv has ONNX and internal implementations
    internal_ops = ["QLinearAdd", "QLinearMul", "QLinearConv"]

    # TODO - review and add ML ops as needed
    # ML Op notes.
    #  CastMap: Switch on value type of input map type, and output type
    #  DictVectorizer: Templatized on key+value of input so need to handle like OneHot with custom processor
    #  LabelEncoder: Implementation switches on input and output types (only supports string and int64 in T1 and T2)
    #  LinearClassifier: Internal switch on input type and also switch on output type
    #  SVMClassifier: ditto
    #  TreeEnsembleClassifier: Templatized on input type and also switch on output type
    #  ZipMap: Switch on output type (derived from attributes)
    default_processor_onnxml_ops = []

    [add(DefaultTypeUsageProcessor("ai.onnx", op)) for op in default_processor_onnx_ops]
    [
        add(DefaultTypeUsageProcessor("ai.onnx", op, required_input_types={0: {"int32_t", "int64_t"}}))
        for op in default_processor_onnx_ops_requiring_ints_for_input_0
    ]
    [add(DefaultTypeUsageProcessor("ai.onnx.ml", op)) for op in default_processor_onnxml_ops]
    [add(DefaultTypeUsageProcessor("com.microsoft", op)) for op in internal_ops]

    #
    # Operators that require custom handling
    #

    # Cast switches on types of input 0 and output 0
    add(DefaultTypeUsageProcessor("ai.onnx", "Cast", inputs=[0], outputs=[0]))

    # Operators that switch on the type of input 0 and 1
    add(DefaultTypeUsageProcessor("ai.onnx", "Gather", inputs=[0, 1]))
    add(DefaultTypeUsageProcessor("ai.onnx", "GatherElements", inputs=[0, 1]))
    add(DefaultTypeUsageProcessor("ai.onnx", "Pow", inputs=[0, 1]))
    add(DefaultTypeUsageProcessor("ai.onnx", "Slice", inputs=[0, 1]))

    # Operators that switch on output type
    add(DefaultTypeUsageProcessor("ai.onnx", "ConstantOfShape", inputs=[], outputs=[0]))

    # Random generator ops produce new data so we track the output type
    onnx_random_ops = ["RandomNormal", "RandomNormalLike", "RandomUniform", "RandomUniformLike", "Multinomial"]
    [add(DefaultTypeUsageProcessor("ai.onnx", op, inputs=[], outputs=[0])) for op in onnx_random_ops]

    # Where always has a boolean first input so track the second input type for typed registration
    add(Input1TypedRegistrationProcessor("ai.onnx", "Where"))

    # we only support 'float' as input for [Dynamic]QuantizeLinear so just track the output type
    # as that's what is used in the typed registration
    add(Output0TypedRegistrationProcessor("ai.onnx", "QuantizeLinear"))
    add(Output0TypedRegistrationProcessor("ai.onnx", "DynamicQuantizeLinear"))

    # make sure all the dequantize types are enabled. we use int32_t for parts of GEMM and Conv so just
    # enabling int8 and uint8 is not enough.
    # TODO: Only apply required types to the global type list and ignore if it's model based per-op type reduction
    add(
        DefaultTypeUsageProcessor(
            "ai.onnx", "DequantizeLinear", inputs=[0], required_input_types={0: {"int8_t", "uint8_t", "int32_t"}}
        )
    )

    # OneHot concatenates type strings into a triple in the typed registration
    #   e.g. float_int64_t_int64_t
    add(OneHotProcessor())

    return operator_processors

