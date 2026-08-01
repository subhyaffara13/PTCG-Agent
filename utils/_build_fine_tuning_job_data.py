
def _build_fine_tuning_job_data(
    model, training_file, hyperparameters, suffix, validation_file, integrations, seed
):
    return FineTuningJobCreate(
        model=model,
        training_file=training_file,
        hyperparameters=hyperparameters,
        suffix=suffix,
        validation_file=validation_file,
        integrations=integrations,
        seed=seed,
    )

