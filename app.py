import streamlit as st

import pandas as pd
import os 
from io import BytesIO             

#setup our app
st.set_page_config(page_title="💿Data Sweeper", page_icon=":bar_chart:", layout="wide")
st.title("Upload and Display Excel File💿")
st.write("Transform Your Files between Excel and CSV format with built-in data cleaning and transformation features!")

#upload the excel file
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "csv"], accept_multiple_files=True )


if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower() 


        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: {file_ext} ❌")
            continue

        #display the dataframe
        file_name = file.name
        file_type = file.type
        file_size = file.size
        st.write(f"**File Name:** {file_name}")
        st.write(f"**File Type:** {file_type}")
        st.write(f"**File Size:** {file_size/1024}")
        st.write(df)

        #add a download button
        st.download_button(label="Download CSV", data=df.to_csv(index=False), file_name=f"{file_name}.csv")
        

        st.write("📈Preview the Head of the DataFrame:")
        st.dataframe(df.head())
        
        #option for data cleaning
        st.subheader("🔎Data Cleaning Options")
        if st.checkbox(f"clean the data {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Removed Duplicates!")
            with col2:
                if st.button(f"Remove Null Values from {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] =df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values have been Filled!")

                      #choose specific columns to keeps or converts
        st.subheader("🎯Choose Columns to Keep or Convert")            
        columns = st.multiselect(f"Select Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]


    #create Some Visualizations
    st.subheader("📊 Data Visualizations")
    if st.checkbox(f"Show Data Visualizations for {file.name}"):
        st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

        #Convert the file -> CSV to Excel 
        st.subheader("🔄Conversation Options")
        conversation_type = st.radio(f"Choose the Conversation Type for {file.name} to:", ["Excel", "CSV"], key=file.name) 
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversation_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
                if conversation_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0) 


                #Download The File
                st.download_button(label=f"⬇ Download {file.name} as {conversation_type}", data=buffer, file_name=file_name, mime=mime_type)
                st.success(f"Successfully Converted 🎉 {file.name} to {conversation_type}!✅")

                