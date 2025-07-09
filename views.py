import streamlit as st
import os

def show_sidebar_instructions():
    with st.sidebar:
        st.header("📂 Evaluation Root Directory")
        st.markdown("""
        Provide the root directory that contains one subdirectory per model.
        ```bash
        streamlit run main.py -- --root /path/to/eval_root
        ```
        """)


# def comparative_analysis_tab(df):
#     st.header("Model Performance Comparison")

#     col1, col2, col3 = st.columns(3)
#     models = ['All'] + sorted(df['model'].unique().tolist())
#     print(models)
#     benchmarks = ['All'] + sorted(df['benchmark'].unique().tolist())
#     print(benchmarks)
#     languages = ['All'] + sorted(df['language'].unique().tolist())
#     print(languages)

#     with col1:
#         selected_models = st.multiselect("Select Models", models, default=['All'])
#     with col2:
#         selected_bench = st.selectbox("Select Benchmark", benchmarks)
#     with col3:
#         selected_lang = st.selectbox("Select Language", languages)

#     filtered = df.copy()
#     if 'All' not in selected_models:
#         filtered = filtered[filtered['model'].isin(selected_models)]
#     if selected_bench != 'All':
#         filtered = filtered[filtered['benchmark'] == selected_bench]
#     if selected_lang != 'All':
#         filtered = filtered[filtered['language'] == selected_lang]

#     if filtered.empty:
#         st.warning("No data for selected filters.")
#         return

#     pivot = filtered.pivot_table(
#         index='benchmark',
#         columns=['language', 'model'],
#         values='value',
#         aggfunc='mean'
#     )
#     st.dataframe(
#         pivot.style.format("{:.4f}")
#                     .background_gradient(cmap='viridis', axis=None)
#                     .highlight_null('lightgrey'),
#         use_container_width=True
#     )
#     st.markdown("Higher values = better performance.")

def comparative_analysis_tab(df):
    st.header("Model Performance Comparison")

    # --- Filters ---
    col1, col2, col3 = st.columns(3)
    models = ['All'] + sorted(df['model'].unique().tolist())
    benchmarks = ['All'] + sorted(df['benchmark'].unique().tolist())
    languages = ['All'] + sorted(df['language'].unique().tolist())

    with col1:
        selected_models = st.multiselect("Select Models", models, default=['All'])
    with col2:
        selected_bench = st.multiselect("Select Benchmark", benchmarks, default=['All'])
    with col3:
        selected_lang = st.multiselect("Select Language", languages, default=['All'])

    # --- Apply filters ---
    filtered = df.copy()
    if 'All' not in selected_models:
        filtered = filtered[filtered['model'].isin(selected_models)]
    if 'All' not in selected_bench:
        filtered = filtered[filtered['benchmark'].isin(selected_bench)]
    if 'All' not in selected_lang:
        filtered = filtered[filtered['language'].isin(selected_lang)]

    if filtered.empty:
        st.warning("No data for selected filters.")
        return

    # --- Pivot table ---
    pivot = filtered.pivot_table(
        index='benchmark',
        columns=['language', 'model'],
        values='value',
        aggfunc='mean'
    )

    # --- Row-wise coloring ---
    styled = (
        pivot
        .style
        .format("{:.4f}")
        .background_gradient(cmap='viridis', axis=1)   # apply gradient per row
        .highlight_null('lightgrey')
    )

    st.dataframe(styled, use_container_width=True)
    st.markdown("Higher values = better performance.")

    
def sample_outputs_values(df):
    st.header("Sample Outputs")
    models = sorted(df['model'].unique().tolist())
    benchmarks = sorted(df['benchmark'].unique().tolist())
    languages = sorted(df['language'].unique().tolist())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_model = st.selectbox("Select Model", models)
    with col2:
        selected_benchmark = st.selectbox("Select Benchmark", benchmarks)
    with col3:
        selected_language = st.selectbox("Select Language", languages)
        
    return selected_model, selected_benchmark, selected_language
    

        
        
def output_visualization_tab(samples):
    st.header("Output Visualization")
    
    if not samples:
        st.warning("No samples available to visualize.")
        return
    
    idx = st.slider("Sample index", 0, len(samples) - 1, 0)
    sample = samples[idx]
    
    st.subheader(f"Sample {idx + 1} of {len(samples)}")
    
    #display all the fields in the sample dictionaty
    for key, value in sample.items():
        if isinstance(value, (list, dict)):
            st.markdown(f"**{key}**")
            st.markdown(value)
        else:
            st.markdown(f"**{key}**: {value}")