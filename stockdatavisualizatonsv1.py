import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

@st.cache_data
def load_data(uploaded_csv, uploaded_xlsx):
    try:
        # Load CSV data
        if uploaded_csv is not None:
            csv_data = pd.read_csv(uploaded_csv)
        else:
            csv_data = pd.read_csv("yahoo_stock_data_extraction (5).csv")
        
        # Load XLSX data
        if uploaded_xlsx is not None:
            xlsx_data = pd.read_excel(uploaded_xlsx, sheet_name=None)
        else:
            xlsx_data = pd.read_excel("yahoo_stock_data_extraction (5).xlsx", sheet_name=None)
        return csv_data, xlsx_data
    except FileNotFoundError:
        st.error("Default files not found. Please upload CSV and XLSX files to proceed.")
        return None, None
    except Exception as e:
        st.error(f"Error loading files: {e}")
        return None, None

def sidebar():
    st.sidebar.header("Options")
    dataset_choice = st.sidebar.selectbox(
        "Select Dataset",
        ("1d", "5d", "1m", "6m", "1y", "5y", "All")
    )
    uploaded_csv = st.sidebar.file_uploader("Upload CSV File (optional)", type="csv")
    uploaded_xlsx = st.sidebar.file_uploader("Upload XLSX File (optional)", type="xlsx")
    return dataset_choice, uploaded_csv, uploaded_xlsx

def select_columns(df):
    st.sidebar.subheader("Filter Columns")
    columns = df.columns.tolist()
    selected_columns = st.sidebar.multiselect("Select columns to display", columns, default=columns[:5])  # Default to first 5 columns
    return df[selected_columns]

def plot_line_chart(df, x_col, y_col):
    line_chart = px.line(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
    st.plotly_chart(line_chart, use_container_width=True)

def plot_bar_chart(df, x_col, y_col):
    bar_chart = px.bar(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
    st.plotly_chart(bar_chart, use_container_width=True)

def plot_scatter_chart(df, x_col, y_col):
    scatter_chart = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
    st.plotly_chart(scatter_chart, use_container_width=True)

def plot_visualizations(df):
    st.subheader("Visualizations")
    
    # Get numeric columns for plotting
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    all_cols = df.columns.tolist()
    
    # Create columns for chart controls
    chart_types = ["Line Chart", "Bar Chart", "Scatter Plot", "Heatmap"]
    selected_charts = st.multiselect("Select charts to display:", chart_types)
    
    for chart_type in selected_charts:
        st.subheader(chart_type)
        
        if chart_type != "Heatmap":
            col1, col2 = st.columns(2)
            with col1:
                x_axis = st.selectbox(f"Select X-axis for {chart_type}:", all_cols, key=f"x_{chart_type}")
            with col2:
                y_axis = st.selectbox(f"Select Y-axis for {chart_type}:", numeric_cols, key=f"y_{chart_type}")
            
            if chart_type == "Line Chart":
                plot_line_chart(df, x_axis, y_axis)
            elif chart_type == "Bar Chart":
                plot_bar_chart(df, x_axis, y_axis)
            elif chart_type == "Scatter Plot":
                plot_scatter_chart(df, x_axis, y_axis)
        
        else:  # Heatmap
            numeric_data = df.select_dtypes(include=["float64", "int64"])
            if not numeric_data.empty:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm", ax=ax)
                st.pyplot(fig)
            else:
                st.warning("Heatmap requires numeric data.")

def main():
    st.title("Stock Data Visualization")
    st.markdown("Visualize Yahoo Stock Datasets: 1d, 5d, 1m, 6m, 1y, 5y, and All.")
    
    # Sidebar interaction
    dataset_choice, uploaded_csv, uploaded_xlsx = sidebar()
    
    # Load data
    csv_data, xlsx_data = load_data(uploaded_csv, uploaded_xlsx)
    
    if csv_data is None or xlsx_data is None:
        st.warning("No data available to display. Please upload valid files or ensure default files are present.")
        return
    
    # Select dataset
    if dataset_choice in xlsx_data:
        df = xlsx_data[dataset_choice]
    else:
        df = csv_data
    
    # Validate dataset
    if df.empty:
        st.warning(f"The dataset '{dataset_choice}' is empty.")
        return
    
    # Column selection
    filtered_df = select_columns(df)
    
    # Display filtered data
    st.write("Filtered Data", filtered_df)
    
    # Plot visualizations
    plot_visualizations(filtered_df)

if __name__ == "__main__":
    main()
