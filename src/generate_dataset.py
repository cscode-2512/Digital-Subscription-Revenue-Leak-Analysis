import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()

rows = 250000

plans = {
    "Mobile":149,
    "Basic":299,
    "Standard":499,
    "Premium":699
}

plan_weights = [0.35, 0.30, 0.20, 0.15]

devices = ["Mobile","Smart TV","Laptop","Tablet"]

payment_methods = ["UPI","Credit Card","Debit Card","Net Banking","Wallet"]

payment_status = ["Success","Failed"]

channels = ["Ads","Organic","Referral","App Store"]

countries = ["India","UAE","UK","USA","Canada"]

content_types = ["Movies","TV Series","Sports","Kids","Documentary"]

age_groups = ["18-24","25-34","35-44","45-54","55+"]

data = []

for i in range(rows):

    # plan (non-uniform)
    plan = random.choices(list(plans.keys()), weights=plan_weights)[0]
    price = plans[plan]

    signup = fake.date_between(start_date='-3y', end_date='today')

    # churn logic
    churn_prob = {
        "Mobile": 0.35,
        "Basic": 0.30,
        "Standard": 0.20,
        "Premium": 0.15
    }

    cancel = None
    if random.random() < churn_prob[plan]:
        cancel = fake.date_between(start_date=signup, end_date='today')

    # age bias
    age = random.choices(age_groups, weights=[0.25,0.30,0.20,0.15,0.10])[0]

    # watch hours
    if plan == "Premium":
        watch = np.random.normal(60,15)
    elif plan == "Standard":
        watch = np.random.normal(45,12)
    elif plan == "Basic":
        watch = np.random.normal(30,10)
    else:
        watch = np.random.normal(20,8)

    watch = max(0, round(watch,2))

    # device bias
    if age in ["18-24","25-34"]:
        device = random.choices(devices, weights=[0.5,0.2,0.2,0.1])[0]
    else:
        device = random.choices(devices, weights=[0.2,0.4,0.2,0.2])[0]

    # content bias
    if age == "18-24":
        content = random.choice(["Movies","Sports","Kids"])
    elif age in ["25-34","35-44"]:
        content = random.choice(["Movies","TV Series","Documentary"])
    else:
        content = random.choice(["TV Series","Documentary","Kids"])

    # payment method bias
    payment = random.choices(
        payment_methods,
        weights=[0.35,0.25,0.15,0.15,0.10]
    )[0]

    # payment status bias
    failure_prob = {
        "UPI": 0.10,
        "Credit Card": 0.15,
        "Debit Card": 0.20,
        "Net Banking": 0.18,
        "Wallet": 0.12
    }

    status = "Failed" if random.random() < failure_prob[payment] else "Success"

    # country bias
    country = random.choices(
        countries,
        weights=[0.40,0.15,0.15,0.20,0.10]
    )[0]

    row = {
        "user_id": i+1,
        "subscription_plan": plan if random.random() > 0.02 else " " + plan + " ",
        "monthly_price": price,
        "signup_date": signup,
        "cancel_date": cancel,
        "watch_hours": watch,
        "content_preference": content,
        "device_type": device,
        "payment_method": payment,
        "payment_status": status,
        "acquisition_channel": random.choice(channels),
        "trial_user": random.choice(["Yes","No"]),
        "country": country,
        "age_group": age
    }

    data.append(row)

df = pd.DataFrame(data)

# ------------------------------
# Introduce Missing Values
# ------------------------------
cols_with_missing = [
    "subscription_plan",
    "payment_method",
    "device_type",
    "country"
]

for col in cols_with_missing:
    df.loc[df.sample(frac=0.02).index, col] = np.nan


# ------------------------------
# Introduce Invalid Prices
# ------------------------------
df.loc[df.sample(frac=0.005).index, "monthly_price"] = -100


# ------------------------------
# Introduce Duplicate Rows
# ------------------------------
duplicates = df.sample(frac=0.01)
df = pd.concat([df, duplicates], ignore_index=True)


# ------------------------------
# Category Inconsistency
# ------------------------------
df.loc[df.sample(frac=0.02).index, "payment_method"] = "credit card"
df.loc[df.sample(frac=0.02).index, "payment_method"] = "CREDIT_CARD"


# ------------------------------
# Date Issues
# ------------------------------
df.loc[df.sample(frac=0.005).index, "signup_date"] = "unknown"


# ------------------------------
# Save
# ------------------------------
df.to_csv("data/raw/streamwave_dataset_v2.csv", index=False)

print("Dataset Generated Successfully ✅")
print("Total Rows:", len(df))


# import pandas as pd
# import numpy as np
# import random
# from faker import Faker

# fake = Faker()

# rows = 250000

# plans = {
#     "Mobile":149,
#     "Basic":299,
#     "Standard":499,
#     "Premium":699
# }

# devices = ["Mobile","Smart TV","Laptop","Tablet"]

# payment_methods = [
#     "UPI",
#     "Credit Card",
#     "Debit Card",
#     "Net Banking",
#     "Wallet"
# ]

# payment_status = ["Success","Failed"]

# channels = [
#     "Ads",
#     "Organic",
#     "Referral",
#     "App Store"
# ]

# countries = [
#     "India",
#     "UAE",
#     "UK",
#     "USA",
#     "Canada"
# ]

# content_types = [
#     "Movies",
#     "TV Series",
#     "Sports",
#     "Kids",
#     "Documentary"
# ]

# age_groups = [
#     "18-24",
#     "25-34",
#     "35-44",
#     "45-54",
#     "55+"
# ]

# data = []

# for i in range(rows):

#     plan = random.choice(list(plans.keys()))
#     price = plans[plan]

#     signup = fake.date_between(start_date='-3y', end_date='today')

#     cancel = None
#     if random.random() < 0.25:
#         cancel = fake.date_between(start_date=signup, end_date='today')

#     row = {
#         "user_id": i+1,

#         # introduce whitespace problems
#         "subscription_plan": plan if random.random() > 0.02 else " " + plan + " ",

#         "monthly_price": price,

#         "signup_date": signup,
#         "cancel_date": cancel,

#         # outliers in watch hours
#         "watch_hours": round(np.random.uniform(0,80),2) if random.random() > 0.01 else round(np.random.uniform(200,500),2),

#         "content_preference": random.choice(content_types),

#         "device_type": random.choice(devices),

#         "payment_method": random.choice(payment_methods),

#         # introduce inconsistent payment status
#         "payment_status": random.choice(payment_status) if random.random() > 0.02 else "success",

#         "acquisition_channel": random.choice(channels),

#         "trial_user": random.choice(["Yes","No"]),

#         "country": random.choice(countries),

#         "age_group": random.choice(age_groups)
#     }

#     data.append(row)

# df = pd.DataFrame(data)

# # ------------------------------
# # Introduce Missing Values
# # ------------------------------

# cols_with_missing = [
#     "subscription_plan",
#     "payment_method",
#     "device_type",
#     "country"
# ]

# for col in cols_with_missing:
#     df.loc[df.sample(frac=0.02).index, col] = np.nan


# # ------------------------------
# # Introduce Invalid Prices
# # ------------------------------

# df.loc[df.sample(frac=0.005).index, "monthly_price"] = -100


# # ------------------------------
# # Introduce Duplicate Rows
# # ------------------------------

# duplicates = df.sample(frac=0.01)
# df = pd.concat([df, duplicates], ignore_index=True)


# # ------------------------------
# # Introduce Category Inconsistency
# # ------------------------------

# df.loc[df.sample(frac=0.02).index, "payment_method"] = "credit card"
# df.loc[df.sample(frac=0.02).index, "payment_method"] = "CREDIT_CARD"


# # ------------------------------
# # Convert some dates to string
# # ------------------------------

# df.loc[df.sample(frac=0.005).index, "signup_date"] = "unknown"


# # Save dataset
# df.to_csv("data/raw/streamwave_dataset.csv",index=False)

# print("Dataset Generated Successfully")
# print("Total Rows:",len(df))