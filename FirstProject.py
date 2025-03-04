import streamlit as st
import pandas as pd
import os
from io import BytesIO


st.set_page_config(page_title="Data Sweeper" ,layout="wide")

st.title("Data Sweeper")
st.write("Transform your files between CSV and Exel formats with built-in data cleaning and visuslization")

uploaded_file=st.file_uploader("Upload your files(CSV or Excel)",type=['csv','xlsx'],accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
        file_ex=os.path.splitext(file.name)[-1].lower()

        if file_ex==".csv":
            df=pd.read_csv(file)
        elif file_ex==".xlsx":
            df=pd.read_excel(file)
        else: 
            st.error(f"Unsupported file type: {file_ex}")
            continue

        st.write(f"File name: {file.name}")
        st.write(f"File size: {file.size/1024}")


        st.write("Preview the head of the Data Frame")
        st.dataframe(df.head())

        st.subheader("Data Cleaning")
        if st.checkbox(f"Data Clean for {file.name}"):
            col1,col2=st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates for {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed!")
            
            with col2:
                if st.button(f"Fill Missing values: {file.name}"):
                    numeric_cols=df.select_dtypes(include=["number"]).columns
                    df[numeric_cols]=df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled!")
            
        st.subheader("Select Columns to Convert")
        columns=st.multiselect(f"Choose Columns for {file.name}", df.columns ,default=df.columns)
        df=df[columns]

        st.subheader("Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        st.subheader("Conversion Options")
        conversion_type= st.radio(f"Convert {file.name} to:",["CSV","Excel"], key=file.name)
        if st.button(f"Convert to {file.name}"):
            buffer = BytesIO()
            if conversion_type=="CSV":
                df.to_csv(buffer,index=False)
                file_name=file.name.replace(file_ex,".csv")
                mime_type="text/csv" 
            elif conversion_type=="Excel":
                df.to_excel(buffer,index=False)
                file_name=file.name.replace(file_ex,".xlsx")
                mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )  

st.write("All Files Processed!")