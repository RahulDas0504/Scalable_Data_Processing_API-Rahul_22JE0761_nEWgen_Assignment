import pandas as pd
import numpy as np


def generate_data():

    print("Generating datasets...")

    total_users = 5_000_000

    users = pd.DataFrame({
        "user_id": np.arange(1, total_users + 1),
        "name": [
            f"User_{i}"
            for i in range(total_users)
        ],
        "signup_date": pd.date_range(
            start="2020-01-01",
            periods=total_users,
            freq="min"
        )
    })

    users.to_csv(
        "users.csv",
        index=False
    )

    total_transactions = 10_000_000

    transactions = pd.DataFrame({
        "transaction_id": np.arange(
            1,
            total_transactions + 1
        ),
        "user_id": np.random.randint(
            1,
            total_users + 1,
            size=total_transactions
        ),
        "amount": np.random.uniform(
            5.0,
            500.0,
            size=total_transactions
        ).round(2)
    })

    transactions.to_csv(
        "transactions.csv",
        index=False
    )

    print("Datasets created successfully")


if __name__ == "__main__":
    generate_data()