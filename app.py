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
    # Data Cleaning
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')  # Ensure 'Age' is numeric, coerce errors to NaN
    df = df.dropna(subset=['Age'])  # Drop rows where 'Age' is NaN
    return df

df = get_data_from_csv()
print(df.columns)
st.dataframe(df)

#-------SIDEBAR-------
def create_multiselect_filter(title, column, df): # Multiselect for multiple selections, default to no selections
    options = df[column].dropna().unique()
    if column in ["NOC", "Sport", "Event"]:
        options = sorted(options, key=lambda x: str(x))
    return st.sidebar.multiselect(
        title,
        options=options,
        default=[]  # All options deselected by default
    )

NOC = create_multiselect_filter("Select NOC:", "NOC", df)
Age = st.sidebar.slider("Select Age Range:", int(df['Age'].min()), int(df['Age'].max()), (int(df['Age'].min()), int(df['Age'].max())))
Sport = create_multiselect_filter("Select Sport:", "Sport", df)
Event = create_multiselect_filter("Select Event:", "Event", df)
Medal = create_multiselect_filter("Select Medal:", "Medal", df)

# Filtering dataframe based on selections
df_selection = df[
    (df['NOC'].isin(NOC) if NOC else True) &
    (df['Age'] >= Age[0]) & (df['Age'] <= Age[1]) &
    (df['Sport'].isin(Sport) if Sport else True) &
    (df['Event'].isin(Event) if Event else True) &
    (df['Medal'].isin(Medal) if Medal else True)
]

st.dataframe(df_selection)