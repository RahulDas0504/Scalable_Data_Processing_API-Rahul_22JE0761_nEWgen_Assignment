import csv

from pathlib import Path


class MergeExecutor:

    def __init__(self, workspace):

        self.workspace = Path(workspace)

    def load_partition(
        self,
        partition_id
    ):

        cache = {}

        users_file = (
            self.workspace /
            f"users_{partition_id}.csv"
        )

        with open(
            users_file,
            "r",
            encoding="utf-8"
        ) as fp:

            reader = csv.DictReader(fp)

            for row in reader:

                cache[
                    int(row["user_id"])
                ] = (
                    row["name"],
                    row["signup_date"]
                )

        return cache

    def process_partition(
        self,
        partition_id,
        writer,
        user_cache
    ):

        matched = 0

        txn_file = (
            self.workspace /
            f"transactions_{partition_id}.csv"
        )

        with open(
            txn_file,
            "r",
            encoding="utf-8"
        ) as fp:

            reader = csv.DictReader(fp)

            for row in reader:

                uid = int(
                    row["user_id"]
                )

                if uid in user_cache:

                    name, signup = (
                        user_cache[uid]
                    )

                    writer.writerow([
                        row["transaction_id"],
                        uid,
                        row["amount"],
                        name,
                        signup
                    ])

                    matched += 1

        return matched