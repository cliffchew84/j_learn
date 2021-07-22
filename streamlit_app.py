import os
import tempfile
import pygsheets
import numpy as np
import pandas as pd
import streamlit as st
from sys import platform
import plotly.express as px
import plotly.graph_objects as go

############ Connect to Google Sheets to get data ############
if platform == "darwin":
    json_encode = os.environ['g_cred'].replace("\\\\", "\\").encode('utf-8')

else:
    json_encode = st.secrets['g_cred'].replace("\\\\", "\\").encode('utf-8')

def _google_creds_as_file():
    temp = tempfile.NamedTemporaryFile()
    temp.write(json_encode)
    temp.flush()
    return temp

def pull_data(worksheet_name):

    creds_file = _google_creds_as_file()
    gc = pygsheets.authorize(service_account_file=creds_file.name)
    return gc.open(worksheet_name)

sh = pull_data('Eng-Jpn Anki')

list_of_worksheets = [str(i).split(" ")[1].replace("'", "") for i in sh.worksheets()]

st.set_page_config(layout="wide")

############ Filter to get the necessary ############

option = st.selectbox(
     'Please select the word list',
     tuple(list_of_worksheets))

wks = sh.worksheet_by_title(option)
df = wks.get_as_df(has_header=False)
final = df.copy()

st.write("No of records : {}".format(final.shape[0]))

# ############ Creating table views ############
t_views = list()
for cols in final.columns:
    t_views.append(final[cols])

ltable = go.Figure(data=[go.Table(
    header=dict(values=['Eng', 'Jpn'],
                font=dict(color='white'),
                line_color='#009688',
                fill_color='#039BE5',
                align='left'),
    cells=dict(values=t_views,
               line_color='darkslategray',
               fill_color='#E0F0F7',
               align='left'))
])

# ltable.update_traces(columnwidth=[1,1])
ltable.update_layout(
    height=500,
    margin=dict(
        l=10, #left margin
        r=5, #right margin
        b=10, #bottom margin
        t=10  #top margin
    )
)

st.plotly_chart(ltable, use_container_width=True)