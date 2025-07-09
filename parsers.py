import json
import re
import streamlit as st


def parse_results_file(file_path, model_name):
    """
    Parse a single results_*.json file, extract per-task metrics.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        results = []
        for task_name, task_data in data.get('results', {}).items():
            parts = task_name.split('_')
            language = parts[-1] if len(parts) > 1 else 'unknown'
            benchmark = '_'.join(parts[:-1]) if len(parts) > 1 else task_name

            # Determine primary metric
            metric_key = next(
                (k for k in ['acc,none', 'exact_match,none', 'bleu,none'] if k in task_data),
                next((k for k, v in task_data.items() if isinstance(v, float)), None)
            )

            if metric_key and task_data.get(metric_key) is not None:
                results.append({
                    'model': model_name,
                    'benchmark': benchmark,
                    'language': language,
                    'task': task_name,
                    'metric': metric_key.split(',')[0],
                    'value': task_data[metric_key]
                })
        return results
    except Exception as e:
        st.warning(f"Could not parse results file: {file_path}. Error: {e}")
        return []


def parse_samples_file(file_path):
    """
    Parse a samples_*.json or .jsonl file into a list of sample dicts.
    """
    try:
        samples = []
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.endswith('.jsonl'):
                for line in f:
                    json_line = json.loads(line.strip())
                    #remove key "doc" from the above
                    json_line.pop('doc', None)
                    json_line.pop('"doc_hash', None)
                    json_line.pop('prompt_hash', None)
                    json_line.pop('target_hash', None)
                    json_line.pop('doc_hash', None)
                    samples.append(json_line)
            else:
                content = json.load(f)
                if isinstance(content, list):
                    samples.extend(content)
                else:
                    samples.append(content)
        return samples
    except Exception as e:
        st.error(f"Error parsing samples file {file_path}: {e}")
        return []