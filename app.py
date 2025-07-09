import streamlit as st
import argparse
from data_loader import load_data_from_root, load_data_results, load_data_samples
from views import (
    show_sidebar_instructions,
    comparative_analysis_tab,
    output_visualization_tab,
    sample_outputs_values,
)

st.set_page_config(
    page_title="LM-Eval Harness Multi-Model Visualizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    parser = argparse.ArgumentParser(description="LM-Eval-Harness Visualizer (root scan)")
    parser.add_argument(
        "--root", type=str, required=True,
        help="Root directory containing one subdirectory per model"
    )
    args = parser.parse_args()  

    st.title("LM-Evaluation-Harness Visualizer")
    show_sidebar_instructions()

    # df, all_samples = load_data_from_root(args.root)
    # if df.empty:
    #     st.error("No valid results loaded. Check your root directory and file patterns.")
    #     return


    df = load_data_results(args.root)
    comparative_analysis_tab(df)
    
    selected_model, selected_benchmark, selected_language = sample_outputs_values(df)
    samples = load_data_samples(args.root, selected_model, selected_benchmark, selected_language)
    if not samples:
        st.warning(f"No samples found for model '{selected_model}', benchmark '{selected_benchmark}', language '{selected_language}'.")
        return
    st.sidebar.info(f"Loaded {len(samples)} samples for model '{selected_model}', benchmark '{selected_benchmark}', language '{selected_language}'.")
    output_visualization_tab(samples)
    # output_visualization_tab(df, all_samples)

if __name__ == '__main__':
    main()
