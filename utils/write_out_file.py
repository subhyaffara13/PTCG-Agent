
def write_out_file(df: pd.DataFrame, fname: str, any_remediations: bool, auto_accept: bool) -> None:
    """
    This function will write out a dataframe to a file, if the user would like to proceed, and also offer a fine-tuning command with the newly created file.
    For classification it will optionally ask the user if they would like to split the data into train/valid files, and modify the suggested command to include the valid set.
    """
    ft_format = infer_task_type(df)
    common_prompt_suffix = get_common_xfix(df.prompt, xfix="suffix")
    common_completion_suffix = get_common_xfix(df.completion, xfix="suffix")

    split = False
    input_text = "- [Recommended] Would you like to split into training and validation set? [Y/n]: "
    if ft_format == "classification":
        if accept_suggestion(input_text, auto_accept):
            split = True

    additional_params = ""
    common_prompt_suffix_new_line_handled = common_prompt_suffix.replace("\n", "\\n")
    common_completion_suffix_new_line_handled = common_completion_suffix.replace("\n", "\\n")
    optional_ending_string = (
        f' Make sure to include `stop=["{common_completion_suffix_new_line_handled}"]` so that the generated texts ends at the expected place.'
        if len(common_completion_suffix_new_line_handled) > 0
        else ""
    )

    input_text = "\n\nYour data will be written to a new JSONL file. Proceed [Y/n]: "

    if not any_remediations and not split:
        sys.stdout.write(
            f'\nYou can use your file for fine-tuning:\n> openai api fine_tunes.create -t "{fname}"{additional_params}\n\nAfter you’ve fine-tuned a model, remember that your prompt has to end with the indicator string `{common_prompt_suffix_new_line_handled}` for the model to start generating completions, rather than continuing with the prompt.{optional_ending_string}\n'
        )
        estimate_fine_tuning_time(df)

    elif accept_suggestion(input_text, auto_accept):
        fnames = get_outfnames(fname, split)
        if split:
            assert len(fnames) == 2 and "train" in fnames[0] and "valid" in fnames[1]
            MAX_VALID_EXAMPLES = 1000
            n_train = max(len(df) - MAX_VALID_EXAMPLES, int(len(df) * 0.8))
            df_train = df.sample(n=n_train, random_state=42)
            df_valid = df.drop(df_train.index)
            df_train[["prompt", "completion"]].to_json(  # type: ignore
                fnames[0], lines=True, orient="records", force_ascii=False, indent=None
            )
            df_valid[["prompt", "completion"]].to_json(
                fnames[1], lines=True, orient="records", force_ascii=False, indent=None
            )

            n_classes, pos_class = get_classification_hyperparams(df)
            additional_params += " --compute_classification_metrics"
            if n_classes == 2:
                additional_params += f' --classification_positive_class "{pos_class}"'
            else:
                additional_params += f" --classification_n_classes {n_classes}"
        else:
            assert len(fnames) == 1
            df[["prompt", "completion"]].to_json(
                fnames[0], lines=True, orient="records", force_ascii=False, indent=None
            )

        # Add -v VALID_FILE if we split the file into train / valid
        files_string = ("s" if split else "") + " to `" + ("` and `".join(fnames))
        valid_string = f' -v "{fnames[1]}"' if split else ""
        separator_reminder = (
            ""
            if len(common_prompt_suffix_new_line_handled) == 0
            else f"After you’ve fine-tuned a model, remember that your prompt has to end with the indicator string `{common_prompt_suffix_new_line_handled}` for the model to start generating completions, rather than continuing with the prompt."
        )
        sys.stdout.write(
            f'\nWrote modified file{files_string}`\nFeel free to take a look!\n\nNow use that file when fine-tuning:\n> openai api fine_tunes.create -t "{fnames[0]}"{valid_string}{additional_params}\n\n{separator_reminder}{optional_ending_string}\n'
        )
        estimate_fine_tuning_time(df)
    else:
        sys.stdout.write("Aborting... did not write the file\n")

