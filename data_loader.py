import pandas as pd
import re
import os
from pathlib import Path
import streamlit as st
from parsers import parse_results_file, parse_samples_file


@st.cache_data
def load_data_from_root(root_path: str):
    """
    Scan root directory for model subdirectories and
    aggregate their results and sample files.
    Returns:
      - df: DataFrame with columns [model, benchmark, language, task, metric, value]
      - all_samples: dict mapping (model, task) -> list of sample dicts
    """
    all_results = []
    all_samples = {}

    root = Path(root_path)
    if not root.is_dir():
        st.error(f"Provided root '{root_path}' is not a valid directory.")
        return pd.DataFrame(), {}

    # Scan each subdirectory as a separate model
    for sub in sorted(root.iterdir()):
        if not sub.is_dir():
            continue
        model_name = sub.name
        st.sidebar.info(f"Loading model: **{model_name}**")

        # Gather result files
        result_files = list(sub.glob('results_*.json'))
        timestamps_to_consider = set()
        for rf in result_files:
            time_stamp = rf.name.split('results_')[-1].split('.')[0]
            all_results.extend(parse_results_file(str(rf), model_name))
            timestamps_to_consider.add(time_stamp)
        print(f"Found {len(result_files)} result files for model '{model_name}' with timestamps: {timestamps_to_consider}")

        # Gather sample files
        sample_files = list(sub.glob('samples_*.jsonl'))
        for sf in sample_files:
            timestamp = sf.name.split('_')[-1].split('.')[0]
            if timestamp not in timestamps_to_consider:
                print(f"Skipping sample file {sf.name} because its timestamp does not match any results file.")
                continue
            
            match = re.search(r'samples_(.*)_\d{4}-\d{2}-\d{2}T', sf.name)
            if match:
                task_key = match.group(1)
                key = (model_name, task_key)
                all_samples.setdefault(key, []).extend(parse_samples_file(str(sf)))
            else:
                st.warning(f"Skipping sample file with unrecognized name: {sf.name}")
        print(f"Found {len(sample_files)} sample files for model '{model_name}' with timestamps: {timestamps_to_consider}")

    df = pd.DataFrame(all_results)
    return df, all_samples


def load_data_results(root_path: str):
    """
    Load results from a root directory containing model subdirectories.
    Returns:
      - df: DataFrame with columns [model, benchmark, language, task, metric, value]
    """
    all_results = []

    root = Path(root_path)
    if not root.is_dir():
        st.error(f"Provided root '{root_path}' is not a valid directory.")
        return pd.DataFrame(), {}

    # Scan each subdirectory as a separate model
    for sub in sorted(root.iterdir()):
        if not sub.is_dir():
            continue
        model_name = sub.name
        st.sidebar.info(f"Loading model: **{model_name}**")

        # Gather result files
        result_files = list(sub.glob('results_*.json'))
        timestamps_to_consider = set()
        for rf in result_files:
            time_stamp = rf.name.split('results_')[-1].split('.')[0]
            all_results.extend(parse_results_file(str(rf), model_name))
            timestamps_to_consider.add(time_stamp)
        print(f"Found {len(result_files)} result files for model '{model_name}' with timestamps: {timestamps_to_consider}")

        
    df = pd.DataFrame(all_results)
    return df


def load_data_samples(
    root_path: str,
    model_name: str,
    benchmark: str,
    language: str
):
    """
    Load sample outputs for a specific model, benchmark, and language.
    Returns:
      - samples: List of sample dicts
    """
    model_results_base = Path(os.path.join(root_path, model_name))
    if not model_results_base.is_dir():
        st.error(f"Model directory '{model_name}' not found in root '{root_path}'.")
        return []
    sample_files = list(model_results_base.glob(f'samples_{benchmark}_{language}_*.jsonl'))
    if not sample_files:
        st.warning(f"No sample files found for model '{model_name}', benchmark '{benchmark}', language '{language}'.")
        return []
    
    #consider only the latest timestamp
    latest_file = sorted(sample_files)[-1]
    
    print(f"Loading samples from file: {latest_file.name}")
    samples = parse_samples_file(str(latest_file))
    if not samples:
        st.warning(f"No samples found in file: {latest_file.name}")
        return []
    
    return samples
    
    

