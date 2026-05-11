import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


print("🔄 Loading datasets...")

users_df=pd.read_csv("data/raw/users.csv")
content_df=pd.read_csv("data/raw/content.csv")
history_df=pd.read_csv("data/raw/watch_history.csv")

print("\n👥 USERS DATASET:")
print(f"   Rows & Columns : {users_df.shape}")
print(f"   Column Names   : {list(users_df.columns)}")

print("\n🎬 CONTENT DATASET:")
print(f"   Rows & Columns : {content_df.shape}")
print(f"   Column Names   : {list(content_df.columns)}")

print("\n📺 WATCH HISTORY DATASET:")
print(f"   Rows & Columns : {history_df.shape}")
print(f"   Column Names   : {list(history_df.columns)}")

print("\n👀 FIRST 5 ROWS OF USERS:")
print(users_df.head())

print("\n👀 FIRST 5 ROWS OF CONTENT:")
print(content_df.head())

print("\n👀 FIRST 5 ROWS OF WATCH HISTORY:")
print(history_df.head())

print("\n📊 DATA TYPES OF USERS:")
print(users_df.dtypes)
print("\n❓ MISSING VALUES IN USERS:")
print(users_df.isnull().sum())

print("\n❓ MISSING VALUES IN CONTENT:")
print(content_df.isnull().sum())

print("\n❓ MISSING VALUES IN WATCH HISTORY:")
print(history_df.isnull().sum())

print("\n📊 TOTAL MISSING IN WATCH HISTORY:")
print(f"   Total missing: {history_df.isnull().sum().sum()}")

print("\n🔧 CLEANING DATA...")

users_df['join_date'] = pd.to_datetime(users_df['join_date'])
history_df['watch_date'] = pd.to_datetime(history_df['watch_date'])

history_df['rating'] = history_df['rating'].fillna(0)

users_df['age'] = users_df['age'].astype(int)
history_df['completion_pct'] = history_df['completion_pct'].astype(float)

print("✅ Data types fixed!")
print(f"   join_date  type : {users_df['join_date'].dtype}")
print(f"   watch_date type : {history_df['watch_date'].dtype}")
print("\n💾 SAVING CLEAN DATA...")

users_df.to_csv('data/raw/users_clean.csv', index=False)
history_df.to_csv('data/raw/history_clean.csv', index=False)
content_df.to_csv('data/raw/content_clean.csv', index=False)
