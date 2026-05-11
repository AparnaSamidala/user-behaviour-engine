import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load clean data
users_df   = pd.read_csv('data/raw/users_clean.csv')
content_df = pd.read_csv('data/raw/content_clean.csv')
history_df = pd.read_csv('data/raw/history_clean.csv')

# Merge all tables
merged_df = pd.merge(history_df, content_df, on='content_id', how='left')
merged_df = pd.merge(merged_df, users_df, on='user_id', how='left')

# ── ANALYSIS 1 — CHURN PREDICTION ────────────────
merged_df['watch_date'] = pd.to_datetime(merged_df['watch_date'])
latest_date = merged_df['watch_date'].max()

last_watch = merged_df.groupby('user_id')['watch_date'].max().reset_index()
last_watch.columns = ['user_id', 'last_watch_date']
last_watch['days_inactive'] = (latest_date - last_watch['last_watch_date']).dt.days

last_watch['churn_risk'] = last_watch['days_inactive'].apply(
    lambda x: 'High Risk'   if x > 60 else
              'Medium Risk' if x > 30 else
              'Low Risk'
)

print("✅ Churn Risk Analysis:")
print(last_watch['churn_risk'].value_counts())

plt.figure(figsize=(8, 5))
churn_counts = last_watch['churn_risk'].value_counts()
sns.barplot(x=churn_counts.index, y=churn_counts.values,
            palette=['green', 'orange', 'red'])
plt.title('User Churn Risk Distribution')
plt.xlabel('Churn Risk')
plt.ylabel('Number of Users')
plt.tight_layout()
plt.savefig('assets/churn_chart.png')
plt.show()
print("✅ Churn chart saved!")

# ── ANALYSIS 2 — USER SEGMENTATION ───────────────
user_stats = merged_df.groupby('user_id').agg(
    total_views      = ('content_id', 'count'),
    avg_completion   = ('completion_pct', 'mean'),
    total_watch_time = ('watch_duration_mins', 'sum')
).reset_index()

user_stats['segment'] = user_stats.apply(
    lambda row: 'Super User'   if row['total_views'] > 30 and row['avg_completion'] > 70 else
                'Regular User' if row['total_views'] > 15 else
                'Casual User', axis=1
)

print("\n✅ User Segments:")
print(user_stats['segment'].value_counts())

plt.figure(figsize=(8, 5))
segment_counts = user_stats['segment'].value_counts()
plt.pie(segment_counts.values,
        labels=segment_counts.index,
        autopct='%1.1f%%',
        colors=['#66b3ff', '#99ff99', '#ff9999'])
plt.title('User Segmentation')
plt.tight_layout()
plt.savefig('assets/segments_chart.png')
plt.show()
print("✅ Segments chart saved!")

# ── ANALYSIS 3 — GENRE PREFERENCE BY AGE ─────────
merged_df['age_group'] = pd.cut(merged_df['age'],
    bins=[0, 25, 35, 50, 100],
    labels=['18-25', '26-35', '36-50', '50+'])

genre_age = merged_df.groupby(['age_group', 'genre'])['user_id'].count().reset_index()
genre_age.columns = ['age_group', 'genre', 'watch_count']

plt.figure(figsize=(12, 6))
sns.barplot(x='genre', y='watch_count', hue='age_group', data=genre_age)
plt.title('Genre Preference by Age Group')
plt.xlabel('Genre')
plt.ylabel('Watch Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('assets/genre_age_chart.png')
plt.show()
print("✅ Genre age chart saved!")

# ── SAVE RESULTS ──────────────────────────────────
last_watch.to_csv('data/raw/churn_analysis.csv', index=False)
user_stats.to_csv('data/raw/user_segments.csv', index=False)


