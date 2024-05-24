import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Olympics Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
                   )


@st.cache_data

def get_data_from_csv():
    df = pd.read_csv(
        "athlete_events.csv",
        header=0,
        usecols=lambda column: column != "A",
        nrows=1000
    )
    return df

df = get_data_from_csv()
print(df.columns)
st.dataframe(df)

#-------SIDEBAR-------
st.sidebar.header("Filter Here:")

Team = st.sidebar.multiselect(
    "Select Team:",
    options=df["Team"].unique(),
    default=list(df["Team"].unique())
)

Age = st.sidebar.multiselect(
    "Select Age:",
    options=df["Age"].unique(),
    default=list(df["Age"].dropna().unique()) # dropna to handle missing values in 'Medal'
)

Sport = st.sidebar.multiselect(
    "Select Sport:",
    options=df["Sport"].unique(),
    default=list(df["Sport"].unique())
)

Event = st.sidebar.multiselect(
    "Select Event:",
    options=df["Event"].unique(),
    default=list(df["Event"].unique())
)

Medal = st.sidebar.multiselect(
    "Select Medal:",
    options=df["Medal"].dropna().unique(),  
    default=list(df["Medal"].dropna().unique())
)

# Filtering dataframe based on selections
df_selection = df.query(
    "Team == @Team & Age == @Age & Sport == @Sport & Event == @Event & Medal == @Medal"
)

st.dataframe(df_selection)