import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()
np.random.seed(42)
random.seed(42)

print("🔄 Generating dataset... Please wait.")

NUM_USERS    = 500
NUM_CONTENT  = 50
NUM_RECORDS  = 10000

genres = ['Drama', 'Comedy', 'Action', 'Documentary',
          'Thriller', 'Romance', 'Sci-Fi', 'Horror']

content = []
for i in range(1, NUM_CONTENT + 1):
    content.append({
        'content_id':    f'C{str(i).zfill(3)}',
        'title':         fake.catch_phrase(),
        'genre':         random.choice(genres),
        'release_year':  random.randint(2015, 2024),
        'duration_mins': random.randint(20, 150)
    })
content_df = pd.DataFrame(content)

users = []
for i in range(1, NUM_USERS + 1):
    users.append({
        'user_id':      f'U{str(i).zfill(4)}',
        'age':          random.randint(18, 65),
        'country':      random.choice(['US', 'UK', 'India',
                                       'Canada', 'Germany', 'Australia']),
        'subscription': random.choice(['Free', 'Basic', 'Premium']),
        'join_date':    fake.date_between(start_date='-3y', end_date='-30d')
    })
users_df = pd.DataFrame(users)

records = []
for _ in range(NUM_RECORDS):
    user         = random.choice(users)
    content_item = random.choice(content)
    duration     = content_item['duration_mins']
    watch_pct    = round(random.betavariate(2, 1.5) * 100, 1)

    records.append({
        'user_id':             user['user_id'],
        'content_id':          content_item['content_id'],
        'watch_date':          fake.date_between(start_date='-1y', end_date='today'),
        'watch_duration_mins': round(duration * watch_pct / 100, 1),
        'completion_pct':      watch_pct,
        'device':              random.choice(['Mobile', 'Desktop', 'TV', 'Tablet']),
        'rating':              random.choice([None, None, 1, 2, 3, 4, 5])
    })
history_df = pd.DataFrame(records)

content_df.to_csv('data/raw/content.csv',      index=False)
users_df.to_csv('data/raw/users.csv',           index=False)
history_df.to_csv('data/raw/watch_history.csv', index=False)

print("\n✅ Dataset created successfully!")
print(f"   📁 Users:         {len(users_df)} rows")
print(f"   📁 Content items: {len(content_df)} rows")
print(f"   📁 Watch records: {len(history_df)} rows")
print("\n📂 Check your data/raw/ folder now!")