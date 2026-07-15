import streamlit as st
import pandas as pd
import os
from database.models import insert_dataset, get_dataset_by_name


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

    # Save to disk
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Read dataset
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # Register in SQLite
    dataset_id = insert_dataset(uploaded_file.name, df.shape[0])

    st.success(f"Dataset uploaded and registered in database successfully. (Run ID: {dataset_id})")

    # Workflow Actions (Bento Box style buttons)
    st.markdown("### Next Steps")
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("Configure Business Rules", key="nav_rules", width="stretch"):
            st.switch_page("app_pages/Rule_Manager.py")
    with c_btn2:
        if st.button("Run Validation Pipeline", key="nav_pipeline", width="stretch", type="primary"):
            st.switch_page("app_pages/Pipeline_Monitor.py")

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
            width="stretch",
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
            width="stretch",
            hide_index=True
        )

    st.divider()

    st.subheader("Basic Statistics")
    numeric = df.select_dtypes(include="number")

    if not numeric.empty:
        st.dataframe(
            numeric.describe().T,
            width="stretch"
        )
    else:
        st.info("No numeric columns available.")

else:
    st.info("Upload a dataset to begin validation.")