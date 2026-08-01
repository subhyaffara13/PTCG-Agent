
def extract_csv(input_dir: str, output_path: str, log_file_path: Optional[str] = None,
                max_workers: Optional[int] = None) -> pd.DataFrame:
    """Extracts game data to a CSV file in a memory-efficient way.
    
    Args:
        input_dir: Directory containing .json game files.
        output_path: Path to save the extracted CSV.
        log_file_path: Optional path to log errors.
        max_workers: Number of workers for parallel processing.
        
    Returns:
        pd.DataFrame: The extracted data.
    """
    game_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                game_files.append(os.path.join(root, file))

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(tqdm(executor.map(_extract_csv_row, game_files), total=len(game_files), desc="Extracting CSV"))

    # Filter results
    data_points = []
    errors = []
    for res, err in results:
        if err:
            errors.append(err)
        elif res:
            data_points.append(res)

    # Log errors if requested
    if log_file_path and errors:
        with open(log_file_path, 'w') as f:
            f.write("Extraction Errors:\n")
            for error in errors:
                f.write(f"{error}\n")

    df = pd.DataFrame(data_points)
    df.to_csv(output_path, index=False)

    return df

