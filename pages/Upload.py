import streamlit as st
import pandas as pd
import os
from utils.styles import load_css

st.set_page_config(page_title="Dataset Upload", layout="wide")
# load_css()

st.title("Dataset Upload")
st.caption("Upload datasets for validation and quality analysis.")

UPLOAD_FOLDER = "data/uploaded"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file:

    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    st.success("Dataset uploaded successfully.")

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", f"{df.shape[0]:,}")
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing Values", int(df.isna().sum().sum()))
    c4.metric("Duplicate Rows", int(df.duplicated().sum()))

    st.divider()

    left, right = st.columns([2, 1])

    with left:
        st.subheader("Dataset Preview")
        st.dataframe(
            df.head(20),
            use_container_width=True,
            hide_index=True
        )

    with right:
        st.subheader("Column Information")

        info = pd.DataFrame({
            "Column": df.columns,
            "Type": df.dtypes.astype(str),
            "Missing": df.isna().sum().values
        })

        st.dataframe(
            info,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    st.subheader("Basic Statistics")

    numeric = df.select_dtypes(include="number")

    if not numeric.empty:
        st.dataframe(
            numeric.describe().T,
            use_container_width=True
        )
    else:
        st.info("No numeric columns available.")

else:
    st.info("Upload a dataset to begin validation.")