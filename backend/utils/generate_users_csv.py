import pandas as pd
from faker import Faker

# Initialize Faker
fake = Faker()

# Load ratings.csv and get unique userIds
ratings_df = pd.read_csv('ml-latest-small/ratings.csv')
unique_user_ids = ratings_df['userId'].unique()

# Prepare user data
users_data = []
for user_id in unique_user_ids:
    if user_id == 1:
        full_name = "Melos Simeneh"
        username = "melos"
    else:
        full_name = fake.name()
        first_name = full_name.split()[0]
        username = first_name.lower()
    
    password = "1234"

    users_data.append({
        'userId': user_id,
        'username': username,
        'full_name': full_name,
        'password': password
    })

# Save to CSV
users_df = pd.DataFrame(users_data)
users_df.to_csv('users.csv', index=False)

print("✅ 'users.csv' created with userId 1 as Melos Simeneh and others randomly generated.")
