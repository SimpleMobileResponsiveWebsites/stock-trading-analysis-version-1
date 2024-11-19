import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import StringIO

# Function to load default datasets or uploaded files
def load_data(csv_file=None, xlsx_file=None):
    try:
        # Handle CSV
        if csv_file:
            csv_data = pd.read_csv(csv_file)
        else:
            csv_data = pd.read_csv("yahoo_stock_data_extraction (5).csv")  # Default file
            
        # Handle XLSX
        if xlsx_file:
            xlsx_data = pd.read_excel(xlsx_file, sheet_name=None)  # Load all sheets
        else:
            xlsx_data = pd.read_excel("yahoo_stock_data_extraction (5).xlsx", sheet_name=None)  # Default file
        
        return csv_data, xlsx_data
    except FileNotFoundError as e:
        st.error(f"File not found: {e}")
    except Exception as e:
        st.error(f"Error loading data: {e}")
    return None, None

# Sidebar for dataset and file upload
def sidebar():
    st.sidebar.header("Options")
    dataset = st.sidebar.selectbox(
        "Select Dataset",
        ("1d", "5d", "1m", "6m", "1y", "5y", "All")
    )
    st.sidebar.write("Upload your files (optional):")
    uploaded_csv = st.sidebar.file_uploader("Upload CSV File", type="csv")
    uploaded_xlsx = st.sidebar.file_uploader("Upload XLSX File", type="xlsx")
    return dataset, uploaded_csv, uploaded_xlsx

# Column selection widget
def select_columns(df):
    st.sidebar.subheader("Filter Columns")
    available_columns = df.columns.tolist()
    selected_columns = st.sidebar.multiselect(
        "Select columns to display:", available_columns, default=available_columns
    )
    return df[selected_columns]

# Visualization functions
def plot_visualizations(df):
    st.subheader("Visualizations")

    # Line Chart
    if st.checkbox("Show Line Chart"):
        y_axis = st.selectbox("Select Y-axis for Line Chart:", df.columns)
        line_chart = px.line(df, x=df.index, y=y_axis, title=f"{y_axis} over Time")
        st.plotly_chart(line_chart, use_container_width=True)

    # Bar Chart
    if st.checkbox("Show Bar Chart"):
        y_axis = st.selectbox("Select Y-axis for Bar Chart:", df.columns)
        bar_chart = px.bar(df, x=df.index, y=y_axis, title=f"{y_axis} Distribution")
        st.plotly_chart(bar_chart, use_container_width=True)

    # Heatmap
    if st.checkbox("Show Heatmap"):
        numeric_data = df.select_dtypes(include=["float", "int"])
        if not numeric_data.empty:
            st.write("Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Heatmap requires numeric data.")

# Main app logic
def main():
    st.title("Stock Data Visualization")
    st.markdown("Visualize Yahoo Stock Datasets: 1d, 5d, 1m, 6m, 1y, 5y, and All.")

    # Sidebar interaction
    dataset_choice, uploaded_csv, uploaded_xlsx = sidebar()

    # Load data
    csv_data, xlsx_data = load_data(uploaded_csv, uploaded_xlsx)

    if csv_data is None or xlsx_data is None:
        st.warning("No data to display. Please upload valid files or ensure default files are available.")
        return

    # Select dataset
    if dataset_choice in xlsx_data:
        df = xlsx_data[dataset_choice]
    else:
        df = csv_data

    # Data validation
    if df.empty:
        st.warning(f"Selected dataset '{dataset_choice}' is empty.")
        return

    # Column selection
    filtered_df = select_columns(df)

    # Display filtered data
    st.write("Filtered Data", filtered_df)

    # Plot visualizations
    plot_visualizations(filtered_df)

# Run the app
if __name__ == "__main__":
    main()
