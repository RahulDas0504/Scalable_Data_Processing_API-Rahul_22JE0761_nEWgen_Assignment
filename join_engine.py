import csv
import shutil
import tempfile
import logging

from time import perf_counter

from core.partition_manager import (
    PartitionManager
)

from core.merge_executor import (
    MergeExecutor
)

from core.utils import PARTITION_COUNT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def execute_large_scale_join(
    users_dataset="users.csv",
    transactions_dataset="transactions.csv",
    final_output="result.csv"
):

    start = perf_counter()

    workspace = tempfile.mkdtemp(
        prefix="join_workspace_"
    )

    logger.info(
        "Starting scalable join process"
    )

    try:

        partition_service = (
            PartitionManager(workspace)
        )

        partition_service.split_dataset(
            users_dataset,
            "users",
            [
                "user_id",
                "name",
                "signup_date"
            ]
        )

        partition_service.split_dataset(
            transactions_dataset,
            "transactions",
            [
                "transaction_id",
                "user_id",
                "amount"
            ]
        )

        merge_service = MergeExecutor(
            workspace
        )

        total_matches = 0

        with open(
            final_output,
            "w",
            newline="",
            encoding="utf-8"
        ) as output:

            writer = csv.writer(output)

            writer.writerow([
                "transaction_id",
                "user_id",
                "amount",
                "name",
                "signup_date"
            ])

            for partition_id in range(
                PARTITION_COUNT
            ):

                logger.info(
                    f"Merging partition "
                    f"{partition_id + 1}/"
                    f"{PARTITION_COUNT}"
                )

                cache = (
                    merge_service.load_partition(
                        partition_id
                    )
                )

                matches = (
                    merge_service.process_partition(
                        partition_id,
                        writer,
                        cache
                    )
                )

                total_matches += matches

        elapsed = perf_counter() - start

        logger.info(
            f"Join completed successfully | "
            f"Matches: {total_matches:,}"
        )

        logger.info(
            f"Execution time: "
            f"{elapsed:.2f} seconds"
        )

    finally:

        shutil.rmtree(
            workspace,
            ignore_errors=True
        )

        logger.info(
            "Temporary files removed"
        )