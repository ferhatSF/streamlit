import streamlit as st
import numpy as np
import pandas as pd

from functionforDownloadButtons import download_button

def _max_width_():
    max_width_str = f"max-width: 1800px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )
    
st.set_page_config(page_icon="💲", page_title="PULSE REPORT: OPPS")

st.title("CVS Timeline Data Analytics")

sample_file="https://raw.githubusercontent.com/ferhatSF/sample-data/5e641880a6767affc2798aa9be7cd99c5739d247/sample_timeline.csv"
sample = pd.read_csv(sample_file)
st.write(sample)

c29, c30, c31 = st.columns([1, 6, 1])

with c30:
    
    uploaded_file = st.file_uploader(
        "",
        key="1",
        help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
    )
    st.info("👆 Upload a .csv file here. Sample to try: Sample-Timeline-Analytics.csv " + sample_file )
    st.download_button('Download Sample Data', sample, "sample.csv",""')   
    if uploaded_file is not None:
        file_container = st.expander("Check your Timeline data .csv")
        shows = pd.read_csv(uploaded_file)
        uploaded_file.seek(0)
        file_container.write(shows)

    else:
        st.stop()

dates = list(filter(lambda x: 'date' in x.lower(), shows.columns))
no_dates = list(filter(lambda x: 'date' not in x.lower(), shows.columns))

DATE_COLUMN = st.selectbox(
     'Pick the date column in your data?',
     (dates))

PIVOT_COL = st.selectbox(
     'Pick the PIVOT column in your data?',
     (shows.columns))

DATE_PLOT = st.selectbox(
     'Pick the TIME for PLOTS in your data?',
     ('YEAR','YEAR-MONTH'))
    
FILTER_COL = st.selectbox(
     'Pick the filter column in your data?',
     (no_dates))

picks=shows[FILTER_COL].unique()

filters = ['Closed Won']

filters = st.multiselect(
     'Chose the values to include?',
     picks)

shows = shows[shows[FILTER_COL].isin(filters)]

#shows=shows[shows['Stage'].str.contains("Won")]

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
