import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ── PAGE CONFIG ───────────────────────────────────
st.set_page_config(
    page_title = "User Behavior Intelligence Engine",
    page_icon  = "🎬",
    layout     = "wide"
)

# ── LOAD DATA ─────────────────────────────────────
@st.cache_data
def load_data():
    users_df   = pd.read_csv('data/raw/users_clean.csv')
    content_df = pd.read_csv('data/raw/content_clean.csv')
    history_df = pd.read_csv('data/raw/history_clean.csv')
    merged_df  = pd.merge(history_df, content_df, on='content_id', how='left')
    merged_df  = pd.merge(merged_df,  users_df,   on='user_id',    how='left')
    return users_df, content_df, history_df, merged_df

users_df, content_df, history_df, merged_df = load_data()

# ── TITLE ─────────────────────────────────────────
st.title("🎬 User Behavior Intelligence Engine")
st.markdown("### Netflix/Spotify Style Analytics Dashboard")
st.markdown("---")

# ── SIDEBAR FILTERS ───────────────────────────────
st.sidebar.title("🔍 Filters")

countries = ['All'] + list(users_df['country'].unique())
selected_country = st.sidebar.selectbox("Select Country", countries)

subscriptions = ['All'] + list(users_df['subscription'].unique())
selected_subscription = st.sidebar.selectbox("Select Subscription", subscriptions)

# Apply filters
filtered_df = merged_df.copy()
if selected_country != 'All':
    filtered_df = filtered_df[filtered_df['country'] == selected_country]
if selected_subscription != 'All':
    filtered_df = filtered_df[filtered_df['subscription'] == selected_subscription]

# ── KPI METRICS ───────────────────────────────────
st.markdown("## 📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Total Users",    len(filtered_df['user_id'].unique()))
col2.metric("🎬 Total Views",    len(filtered_df))
col3.metric("⏱️ Avg Watch Time", f"{filtered_df['watch_duration_mins'].mean():.1f} mins")
col4.metric("⭐ Avg Rating",     f"{filtered_df[filtered_df['rating']>0]['rating'].mean():.1f}")

st.markdown("---")

# ── CHARTS ROW 1 ──────────────────────────────────
st.markdown("## 📈 Content Analytics")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎭 Most Watched Genres")
    genre_counts = filtered_df['genre'].value_counts()
    fig = px.bar(x=genre_counts.index,
                 y=genre_counts.values,
                 color=genre_counts.index,
                 title='Most Watched Genres')
    fig.update_layout(xaxis_title='Genre', yaxis_title='Watch Count')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📱 Watch Time by Device")
    device_watch = filtered_df.groupby('device')['watch_duration_mins'].mean()
    fig = px.bar(x=device_watch.index,
                 y=device_watch.values,
                 color=device_watch.index,
                 title='Average Watch Time by Device')
    fig.update_layout(xaxis_title='Device', yaxis_title='Avg Mins')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── CHARTS ROW 2 ──────────────────────────────────
st.markdown("## 👥 User Analytics")
col1, col2 = st.columns(2)

with col1:
    st.subheader("💳 Subscription Breakdown")
    sub_counts = filtered_df['subscription'].value_counts()
    fig = px.pie(values=sub_counts.values,
                 names=sub_counts.index,
                 title='Subscription Breakdown')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("⭐ Rating Distribution")
    rated_df = filtered_df[filtered_df['rating'] > 0]
    fig = px.histogram(rated_df, x='rating',
                       nbins=5,
                       title='Rating Distribution',
                       color_discrete_sequence=['purple'])
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── CHURN RISK ────────────────────────────────────
st.markdown("## 🔴 Churn Risk Analysis")
try:
    churn_df = pd.read_csv('data/raw/churn_analysis.csv')
    churn_counts = churn_df['churn_risk'].value_counts()
    fig = px.bar(x=churn_counts.index,
                 y=churn_counts.values,
                 color=churn_counts.index,
                 color_discrete_map={
                     'Low Risk':    'green',
                     'Medium Risk': 'orange',
                     'High Risk':   'red'
                 },
                 title='Churn Risk Distribution')
    st.plotly_chart(fig, use_container_width=True)
except:
    st.warning("⚠️ Run advanced_analytics.py first!")

# ── TOP CONTENT TABLE ─────────────────────────────
st.markdown("## 🏆 Top 10 Most Watched Content")
top_content = filtered_df.groupby('title')['user_id'].count().sort_values(ascending=False).head(10).reset_index()
top_content.columns = ['Title', 'Total Views']
st.dataframe(top_content, use_container_width=True)

st.markdown("---")
st.markdown("Built with ❤️ using Python & Streamlit")
