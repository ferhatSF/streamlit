import streamlit as st
import numpy as np
import pandas as pd

from functionforDownloadButtons import download_button

st.set_page_config(page_icon="✂️", page_title="PULSE REPORT: OPPS")


c29, c30, c31 = st.columns([1, 6, 1])

with c30:

    uploaded_file = st.file_uploader(
        "",
        key="1",
        help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
    )

    if uploaded_file is not None:
        file_container = st.expander("Check your uploaded .csv")
        shows = pd.read_csv(uploaded_file)
        uploaded_file.seek(0)
        file_container.write(shows)

    else:
        st.info(
            f"""
                👆 Upload a .csv file first. Sample to try: [biostats.csv](https://people.sc.fsu.edu/~jburkardt/data/csv/biostats.csv)
                """
        )

        st.stop()

dates = list(filter(lambda x: 'date' in x.lower(), shows.columns))
no_dates = list(filter(lambda x: 'date' not in x.lower(), shows.columns))
        
    
FILTER_COL = st.selectbox(
     'Pick the filter column in your data?',
     (no_dates))

DATE_COLUMN = st.selectbox(
     'Pick the date column in your data?',
     (dates))

PIVOT_COL = st.selectbox(
     'Pick the PIVOT column in your data?',
     (shows.columns))

DATE_PLOT = st.selectbox(
     'Pick the TIME for PLOTS in your data?',
     ('YEAR','YEAR-MONTH'))

shows=shows[shows['Stage'].str.contains("Won")]

shows['YEAR'] = pd.to_datetime(shows[DATE_COLUMN]).dt.year
shows['YEAR-MONTH'] = pd.to_datetime(shows[DATE_COLUMN]).dt.to_period('M')

df=pd.pivot_table(shows, values='Amount', index=DATE_PLOT,
                    columns=PIVOT_COL, aggfunc=np.sum)

df.columns.name = None
df = df.reset_index()
df.set_index(DATE_PLOT, inplace=True)
df.index=df.index.to_series().astype(str)

s = df.sum()

start_date, end_date = st.select_slider(
     'Select a range of dates',
     options=df.index, value=(df.index[0], df.index[-1]))

st.write('You selected dates between', start_date, ' and ', end_date)

st.bar_chart(df[start_date:end_date])

st.write(df[start_date:end_date])

c29, c30, c31 = st.columns([1, 1, 2])

with c29:

    CSVButton = download_button(
        df,
        "File.csv",
        "Download to CSV",
    )

with c30:
    CSVButton = download_button(
        df,
        "File.csv",
        "Download to TXT",
    )
