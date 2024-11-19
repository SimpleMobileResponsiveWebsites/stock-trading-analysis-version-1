import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime

# Load Data Function
@st.cache_data
def load_data_from_files(csv_path, xlsx_path):
    csv_data = pd.read_csv(csv_path)
    xlsx_data = pd.read_excel(xlsx_path, sheet_name=None)  # Load all sheets
    return csv_data, xlsx_data

# Sidebar for Dataset Selection
def sidebar():
    st.sidebar.header("Options")
    dataset = st.sidebar.selectbox(
        "Select Dataset",
        ("1d", "5d", "1m", "6m", "1y", "5y", "All")
    )
    return dataset

# Sidebar Column Selection
def select_columns(df):
    st.sidebar.subheader("Filter Columns")
    available_columns = df.columns.tolist()
    selected_columns = st.sidebar.multiselect("Select columns to display:", available_columns, default=available_columns)
    return selected_columns

# Date Filtering
def filter_by_date(df):
    st.sidebar.subheader("Filter by Date")
    if "Date" in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        min_date = df['Date'].min()
        max_date = df['Date'].max()
        date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
        return df[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])]
    return df

# Visualization Options
def plot_visualizations(df):
    st.subheader("Visualizations")

    # Line Chart
    if st.checkbox("Show Line Chart"):
        y_axis = st.selectbox("Select Y-axis for Line Chart:", df.columns, index=1)
        line_chart = px.line(df, x="Date", y=y_axis, title=f"{y_axis} over Time")
        st.plotly_chart(line_chart, use_container_width=True)

    # Bar Chart
    if st.checkbox("Show Bar Chart"):
        y_axis = st.selectbox("Select Y-axis for Bar Chart:", df.columns, index=2)
        bar_chart = px.bar(df, x="Date", y=y_axis, title=f"{y_axis} Distribution")
        st.plotly_chart(bar_chart, use_container_width=True)

    # Candlestick Chart
    if st.checkbox("Show Candlestick Chart"):
        if all(col in df.columns for col in ["Date", "Open", "High", "Low", "Close"]):
            fig = px.line(df, x="Date", y=["Open", "High", "Low", "Close"], title="Candlestick Chart")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Candlestick Chart requires Open, High, Low, and Close columns.")

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

# Main App
def main():
    st.title("Stock Data Visualization")
    st.markdown("Visualize Yahoo Stock Datasets: 1d, 5d, 1m, 6m, 1y, 5y, and All.")

    # Default File Paths (for deployment with preloaded files)
    default_csv = "yahoo_stock_data_extraction (5).csv"
    default_xlsx = "yahoo_stock_data_extraction (5).xlsx"

    # File Upload Option
    st.sidebar.subheader("Upload Files")
    uploaded_csv = st.sidebar.file_uploader("Upload CSV File", type="csv")
    uploaded_xlsx = st.sidebar.file_uploader("Upload XLSX File", type="xlsx")

    # Load Data
    if uploaded_csv and uploaded_xlsx:
        st.sidebar.write("Using uploaded files.")
        csv_data = pd.read_csv(uploaded_csv)
        xlsx_data = pd.read_excel(uploaded_xlsx, sheet_name=None)
    else:
        st.sidebar.write("Using default files.")
        csv_data, xlsx_data = load_data_from_files(default_csv, default_xlsx)

    # Dataset Selection
    dataset_choice = sidebar()
    st.sidebar.write(f"Selected Dataset: {dataset_choice}")

    # Load the selected dataset
    if dataset_choice in xlsx_data:
        df = xlsx_data[dataset_choice]
    else:
        df = csv_data

    # Column Filtering
    selected_columns = select_columns(df)
    filtered_df = df[selected_columns]

    # Date Filtering
    filtered_df = filter_by_date(filtered_df)

    # Show Filtered Dataframe
    st.write("Filtered Data", filtered_df)

    # Plot Visualizations
    plot_visualizations(filtered_df)

# Run the App
if __name__ == "__main__":
    main()
