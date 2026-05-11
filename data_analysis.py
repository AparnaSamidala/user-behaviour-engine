import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load clean data
users_df   = pd.read_csv('data/raw/users_clean.csv')
content_df = pd.read_csv('data/raw/content_clean.csv')
history_df = pd.read_csv('data/raw/history_clean.csv')

# Merge history with content
merged_df = history_df.merge(content_df, on='content_id', how='left')

# Chart 1 - Most watched genres
plt.figure(figsize=(10, 5))
genre_counts = merged_df['genre'].value_counts()
sns.barplot(x=genre_counts.index, y=genre_counts.values, palette='viridis')
plt.title('Most Watched Genres')
plt.xlabel('Genre')
plt.ylabel('Watch Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('assets/genre_chart.png')
plt.show()
print("✅ Genre chart saved!")

# Chart 2 - Watch time by device
plt.figure(figsize=(8, 5))
device_watch = history_df.groupby('device')['watch_duration_mins'].mean()
sns.barplot(x=device_watch.index, y=device_watch.values, palette='coolwarm')
plt.title('Average Watch Time by Device')
plt.xlabel('Device')
plt.ylabel('Avg Watch Duration (mins)')
plt.tight_layout()
plt.savefig('assets/device_chart.png')
plt.show()
print("✅ Device chart saved!")

# Chart 3 - Subscription breakdown
plt.figure(figsize=(6, 6))
subscription_counts = users_df['subscription'].value_counts()
plt.pie(subscription_counts.values,
        labels=subscription_counts.index,
        autopct='%1.1f%%',
        colors=['#ff9999','#66b3ff','#99ff99'])
plt.title('User Subscription Breakdown')
plt.tight_layout()
plt.savefig('assets/subscription_chart.png')
plt.show()
print("✅ Subscription chart saved!")

# Chart 4 - Rating distribution
plt.figure(figsize=(8, 5))
rated_df = history_df[history_df['rating'] > 0]
sns.histplot(rated_df['rating'], bins=5, kde=False, color='purple')
plt.title('Rating Distribution')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('assets/rating_chart.png')
plt.show()
print("✅ Rating chart saved!")

print("\n🎉 All 4 charts created and saved in assets/ folder!")