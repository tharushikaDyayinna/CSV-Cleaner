import streamlit as st
import pandas as pd
import zipfile
import io

st.set_page_config(page_title="CSV Cleaner & Zipper", layout="centered")

st.title("🧼 CSV Cleaner")

uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)

if uploaded_files:
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for uploaded_file in uploaded_files:
            st.write(f"Processing: {uploaded_file.name}")

            try:
                df = pd.read_csv(uploaded_file)

                # Clean Quantity
                if 'Quantity' in df.columns:
                    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)

                # Clean text columns
                text_cols = df.select_dtypes(include="object").columns
                df[text_cols] = df[text_cols].apply(lambda s: s.str.strip())

                # Save to in-memory buffer
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                cleaned_name = f"{uploaded_file.name.replace('.csv', '')}_cleaned.csv"

                # Add to ZIP
                zip_file.writestr(cleaned_name, csv_buffer.getvalue())

            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")

    st.success("✅ All files cleaned and zipped!")

    st.download_button(
        label="📦 Download All Cleaned CSVs as ZIP",
        data=zip_buffer.getvalue(),
        file_name="cleaned_csv_files.zip",
        mime="application/zip"
    )
