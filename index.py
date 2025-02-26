import streamlit as st
import pandas as pd
import os
from io import BytesIO
import openpyxl

st.title('🚀 Data Sweeper - Clean & Transform Your Data!')

st.write("""
Welcome to **Data Sweeper!** 📊✨
This tool helps you **clean, transform, and convert** your data effortlessly.  
🔹 Upload **CSV** or **Excel** files  
🔹 **Remove duplicates** & **fill missing values**  
🔹 **Select specific columns** for analysis  
🔹 **Convert files** between CSV & Excel formats  
🔹 **Download** your cleaned data instantly!  
""")

file = st.file_uploader("📥 Upload your CSV or Excel file", type=['csv', 'xlsx'], accept_multiple_files=False)

if file:
    file_extension = os.path.splitext(file.name)[-1].lower()

    if file_extension == '.csv':
        df = pd.read_csv(file)
    elif file_extension == '.xlsx':
        df = pd.read_excel(file)
    else:
        st.error(f'❌ Invalid file type: {file_extension}')
        st.stop()

    st.write(f"**📂 File Name:** {file.name}")
    st.write(f"**📄 File Type:** {file_extension}")
    st.write(f"**📏 File Size:** {file.size} bytes")
    
    st.subheader('Data Preview')
    st.dataframe(df.head())

    st.subheader('🛠 Data Cleaning Options')

    if st.button('🧹 Remove Duplicates'):
        df = df.drop_duplicates()
        st.success('✅ Duplicates removed successfully!')
        st.dataframe(df.head())

    if st.button('📊 Fill Missing Values'):
        numeric_cols = df.select_dtypes(include=['number']).columns
        if not numeric_cols.empty:
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            st.success('✅ Missing values filled with column mean!')
            st.dataframe(df.head())
        else:
            st.warning("⚠ No numeric columns found to fill missing values.")

    st.subheader('Select Columns')
    selected_columns = st.multiselect("Choose columns to keep and remove extra one", df.columns, default=df.columns)
    df = df[selected_columns]

    if st.button('View Changes'):
        st.subheader('Data Preview')
        st.dataframe(df.head())

    st.subheader('🔄 Convert File Format')
    conversion_type = st.radio("Convert file to:", ('CSV', 'Excel'))

    buffer = BytesIO()
    if conversion_type == 'CSV':
        df.to_csv(buffer, index=False)
        file_name = file.name.replace(file_extension, '.csv')
        mime_type = 'text/csv'
    else:
        df.to_excel(buffer, index=False, engine='openpyxl')
        file_name = file.name.replace(file_extension, '.xlsx')
        mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    st.download_button(label='📥 Download Processed File', data=buffer.getvalue(), file_name=file_name, mime=mime_type)

else:
    st.warning("⚠ Please upload a file to get started.")

