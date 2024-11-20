import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Function to load datasets
@st.cache_data
def load_data(uploaded_csv, uploaded_xlsx):
    try:
        # Load CSV data
        if uploaded_csv is not None:
            csv_data = pd.read_csv(uploaded_csv)
        else:
            csv_data = pd.read_csv("yahoo_stock_data_extraction (5).csv")  # Default CSV file

        # Load XLSX data
        if uploaded_xlsx is not None:
            xlsx_data = pd.read_excel(uploaded_xlsx, sheet_name=None)  # All sheets
        else:
            xlsx_data = pd.read_excel("yahoo_stock_data_extraction (5).xlsx", sheet_name=None)  # Default XLSX file

        return csv_data, xlsx_data

    except FileNotFoundError:
        st.error("Default files not found. Please upload CSV and XLSX files to proceed.")
        return None, None
    except Exception as e:
        st.error(f"Error loading files: {e}")
        return None, None

# Sidebar for dataset and file upload
def sidebar():
    st.sidebar.header("Options")
    dataset_choice = st.sidebar.selectbox(
        "Select Dataset",
        ("1d", "5d", "1m", "6m", "1y", "5y", "All")
    )
    uploaded_csv = st.sidebar.file_uploader("Upload CSV File (optional)", type="csv")
    uploaded_xlsx = st.sidebar.file_uploader("Upload XLSX File (optional)", type="xlsx")
    return dataset_choice, uploaded_csv, uploaded_xlsx

# Filter columns
def select_columns(df):
    st.sidebar.subheader("Filter Columns")
    columns = df.columns.tolist()
    selected_columns = st.sidebar.multiselect("Select columns to display", columns, default=columns)
    return df[selected_columns]

# Visualization functions
def plot_visualizations(df):
    st.subheader("Visualizations")

    # Line Chart
    if st.checkbox("Show Line Chart"):
        y_axis = st.selectbox("Select Y-axis for Line Chart:", df.columns, key="line_chart")
        line_chart = px.line(df, x=df.index, y=y_axis, title=f"{y_axis} over Time")
        st.plotly_chart(line_chart, use_container_width=True)

    # Bar Chart
    if st.checkbox("Show Bar Chart"):
        y_axis = st.selectbox("Select Y-axis for Bar Chart:", df.columns, key="bar_chart")
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

    # Properly check for loaded data
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

# Run the app
if __name__ == "__main__":
    main()
