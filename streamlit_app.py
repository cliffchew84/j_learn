import os
import tempfile
import pygsheets
import numpy as np
import pandas as pd
import streamlit as st
from sys import platform
import plotly.express as px
import plotly.graph_objects as go

pd.set_option('display.max_colwidth',None)

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

sh = pull_data('NLB Project')

wk_list = [str(i).split(" ")[1].replace("'", "") for i in sh.worksheets()]

############ Filter to get the necessary ############
st.set_page_config(layout="wide")

wks = sh.worksheet_by_title("All")
df = wks.get_as_df(has_header=True)
final = df[df.availability == "Available"][
    ['library', 'title', 'number', 'url']]

lib_select = st.selectbox(
     'Select Library',
     tuple(df.library.drop_duplicates().tolist()) + ["All", ])

search_text = st.text_input(label="Title Search").lower()

if lib_select != 'All':
    final = final[
        final['library'] == lib_select].drop_duplicates().sort_values('title')

if len(search_text) > 0:
    final['title_lower'] = final['title'].str.lower()
    final = final[final.title_lower.str.contains(search_text)]
    del final['title_lower']

def make_clickable(text, link):
    # target _blank to open new window
    # extract clickable text to display for your link
    return f'<a target="_blank" href="{link}">{text}</a>'

# link is the column with hyperlinks
final['title'] = [make_clickable(text, url) for text, url in zip(final['title'], final['url'])]

del final['url']
del final['library']
final = final.reset_index(drop=True)

final_table = final.to_html(escape=False)

st.write("Book : {}".format(final.shape[0]))
st.write(final_table, unsafe_allow_html=True)