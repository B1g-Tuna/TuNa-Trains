import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Define the Excel file and sheet name
EXCEL_FILE = 'TuNa_Trains.xlsx'
SHEET_NAME = 'WODs'

def append_data_to_excel(data):
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    else:
        df = pd.DataFrame(columns=["Date", "Exercise", "Repetitions", "Sets", "Intensity", "Intensity Unit", "Additional Notes"])

    new_data = pd.DataFrame(data, columns=["Date", "Exercise", "Repetitions", "Sets", "Intensity", "Intensity Unit", "Additional Notes"])
    df = pd.concat([df, new_data], ignore_index=True)
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='a' if os.path.exists(EXCEL_FILE) else 'w') as writer:
        df.to_excel(writer, sheet_name=SHEET_NAME, index=False)

def main():
    st.title("TuNa")

    columns = ["Exercise", "Repetitions", "Sets", "Intensity", "Intensity Unit", "Additional Notes"]
    data = {col: [] for col in columns}

    for i in range(5):
        cols = st.columns(len(columns))
        for idx, col in enumerate(columns):
            data[col].append(cols[idx].text_input(f"{col} {i+1}"))

    if st.button("Done"):
        if st.confirm("Are you sure you want to submit?"):
            current_date = datetime.now().strftime("%Y-%m-%d")
            rows = [[current_date] + [data[col][i] for col in columns] for i in range(5)]
            append_data_to_excel(rows)
            st.success("Data submitted successfully!")
            st.rerun()

# python -m streamlit run app.py
