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

wk_list = [str(i).split(" ")[1].replace("'", "") for i in sh.worksheets()]
wk_list = [i for i in wk_list if "HIDE" not in i]

############ Filter to get the necessary ############
# st.set_page_config(layout="wide")
option = st.selectbox(
     'Select a word list',
     tuple(wk_list))

wks = sh.worksheet_by_title(option)
df = wks.get_as_df(has_header=False)
final = df.copy()

st.write("Words | Phrases : {}".format(final.shape[0]))

# ############ Creating table views ############
t_views = list()
for cols in final.columns:
    t_views.append(final[cols])

ltable = go.Figure(data=[go.Table(
    header=dict(values=['Eng', 'Jpn'],
                font=dict(color='white', size=14),
                line_color='#009688',
                fill_color='#039BE5',
                align='left'),
    cells=dict(values=t_views,
               font=dict(size=14),
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