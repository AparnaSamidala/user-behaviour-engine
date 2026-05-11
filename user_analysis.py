import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load clean data
users_df   = pd.read_csv('data/raw/users_clean.csv')
content_df = pd.read_csv('data/raw/content_clean.csv')
history_df = pd.read_csv('data/raw/history_clean.csv')

# Merge tables
merged_df = pd.merge(history_df, content_df, on='content_id', how='left')
merged_df = pd.merge(merged_df, users_df, on='user_id', how='left')

# Analysis 1 - Top 10 most popular content
top_content = merged_df.groupby('title')['user_id'].count().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
sns.barplot(x=top_content.values, y=top_content.index, palette='magma')
plt.title('Top 10 Most Popular Content')
plt.xlabel('Total Views')
plt.ylabel('Content Title')
plt.tight_layout()
plt.savefig('assets/top_content.png')
plt.show()
print("✅ Top content chart saved!")

# Analysis 2 - User engagement score
user_engagement = merged_df.groupby('user_id').agg(
    total_watch_time = ('watch_duration_mins', 'sum'),
    avg_completion   = ('completion_pct', 'mean'),
    total_views      = ('content_id', 'count')
).reset_index()
user_engagement['engagement_score'] = (
    user_engagement['total_watch_time'] * 0.5 +
    user_engagement['avg_completion']   * 0.3 +
    user_engagement['total_views']      * 0.2
)
print("\n✅ User Engagement Scores:")
print(user_engagement.sort_values('engagement_score', ascending=False).head(10))

# Analysis 3 - Watch trends over time
merged_df['watch_date'] = pd.to_datetime(merged_df['watch_date'])
merged_df['month'] = merged_df['watch_date'].dt.to_period('M')
monthly_views = merged_df.groupby('month')['user_id'].count()
plt.figure(figsize=(12, 5))
monthly_views.plot(kind='line', color='blue', marker='o')
plt.title('Monthly Watch Trends')
plt.xlabel('Month')
plt.ylabel('Total Views')
plt.tight_layout()
plt.savefig('assets/trends_chart.png')
plt.show()
print("✅ Trends chart saved!")

# Analysis 4 - Top 10 users by watch time
top_users = merged_df.groupby('user_id')['watch_duration_mins'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=top_users.index, y=top_users.values, palette='rocket')
plt.title('Top 10 Users by Watch Time')
plt.xlabel('User ID')
plt.ylabel('Total Watch Time (mins)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('assets/top_users.png')
plt.show()
print("✅ Top users chart saved!")

# Save engagement scores
user_engagement.to_csv('data/raw/user_engagement.csv', index=False)
print("\n✅ Engagement scores saved!")
