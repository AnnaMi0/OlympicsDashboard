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

    )
    return df

df = get_data_from_csv()
print(df.columns)
st.dataframe(df)

#-------SIDEBAR-------
def create_multiselect_filter(title, column, df):
    options = df[column].dropna().unique()
    if column == "Team" or column == "Sport" or column == "Event":
        options = sorted(options, key=lambda x: str(x))
    return st.sidebar.multiselect(
        title,
        options=options,
        default=list(options)
    )

Team = create_multiselect_filter("Select Team:", "Team", df)
Age = create_multiselect_filter("Select Age:", "Age", df)
Sport = create_multiselect_filter("Select Sport:", "Sport", df)
Event = create_multiselect_filter("Select Event:", "Event", df)
Medal = create_multiselect_filter("Select Medal:", "Medal", df)

# Filtering dataframe based on selections
df_selection = df.query(
    "Team == @Team & Age == @Age & Sport == @Sport & Event == @Event & Medal == @Medal"
)

st.dataframe(df_selection)