import os
import random
import sqlite3
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

fake = Faker("en_IN")

DB_PATH = os.path.join("data", "enterprise_data.db")
CSV_PATH = os.path.join("data", "sample_transactions.csv")

os.makedirs("data", exist_ok=True)

CARD_TYPES = ["Silver", "Gold", "Platinum"]
CURRENCIES = ["INR", "USD", "EUR"]
MERCHANT_CATEGORIES = [
    "Travel",
    "Dining",
    "Shopping",
    "Fuel",
    "Healthcare",
    "Entertainment",
    "Grocery",
    "Electronics"
]
COUNTRIES = [
    "India",
    "USA",
    "Singapore",
    "UAE",
    "UK"
]
STATUS = ["Approved", "Declined", "Pending"]
RISK = ["Low", "Medium", "High"]
PAYMENT = ["Credit", "Debit"]
DEVICE = ["Mobile", "Desktop", "POS"]
CHANNEL = ["Online", "Offline"]


def random_datetime():
    start = datetime.now() - timedelta(days=180)
    end = datetime.now()

    delta = end - start

    return start + timedelta(
        seconds=random.randint(0, int(delta.total_seconds()))
    )


rows = []

for i in range(1, 501):

    rows.append({

        "Transaction_ID": f"TXN{i:06d}",

        "Customer_ID": f"CUST{random.randint(1,150):05d}",

        "Card_Type": random.choice(CARD_TYPES),

        "Transaction_Amount": round(random.uniform(100, 150000), 2),

        "Currency": random.choice(CURRENCIES),

        "Merchant_Category": random.choice(MERCHANT_CATEGORIES),

        "Merchant_Country": random.choice(COUNTRIES),

        "Transaction_Time": random_datetime().strftime("%Y-%m-%d %H:%M:%S"),

        "Transaction_Status": random.choice(STATUS),

        "Risk_Level": random.choice(RISK),

        "Payment_Method": random.choice(PAYMENT),

        "Device_Type": random.choice(DEVICE),

        "Channel": random.choice(CHANNEL)

    })

df = pd.DataFrame(rows)

# ----------------------------------------------------
# Inject Data Quality Issues
# ----------------------------------------------------

# Duplicate Transaction IDs
df.loc[25, "Transaction_ID"] = df.loc[10, "Transaction_ID"]
df.loc[70, "Transaction_ID"] = df.loc[45, "Transaction_ID"]

# Missing Values
df.loc[15, "Currency"] = None
df.loc[120, "Merchant_Country"] = None
df.loc[260, "Transaction_Amount"] = None

# Invalid Currency
df.loc[85, "Currency"] = "XYZ"

# Negative Amount
df.loc[170, "Transaction_Amount"] = -5500

# Future Timestamp
future = datetime.now() + timedelta(days=5)
df.loc[230, "Transaction_Time"] = future.strftime("%Y-%m-%d %H:%M:%S")

# Invalid Card Type
df.loc[320, "Card_Type"] = "Diamond"

# Invalid Risk Level
df.loc[360, "Risk_Level"] = "Very High"

# Invalid Status
df.loc[410, "Transaction_Status"] = "Completed"

# Save CSV
df.to_csv(CSV_PATH, index=False)

print("Sample dataset created.")

# -------------------------------------------
# Register dataset in SQLite
# -------------------------------------------

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
INSERT INTO datasets(
filename,
upload_timestamp,
uploaded_by,
total_rows,
quality_score,
status,
validation_time
)
VALUES(?,?,?,?,?,?,?)
""",
(
"sample_transactions.csv",
datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
"System",
len(df),
0,
"Uploaded",
None
)
)

conn.commit()
conn.close()

print("Dataset metadata stored.")
print(f"CSV saved at: {CSV_PATH}")