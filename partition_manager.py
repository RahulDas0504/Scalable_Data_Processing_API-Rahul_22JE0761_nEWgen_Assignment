import csv
import logging

from pathlib import Path

from core.utils import (
    PARTITION_COUNT,
    compute_partition
)

logger = logging.getLogger(__name__)


class PartitionManager:

    def __init__(self, workspace):

        self.workspace = Path(workspace)

    def split_dataset(
        self,
        source_file,
        output_prefix,
        columns
    ):

        handles = {}
        writers = {}

        try:

            for index in range(
                PARTITION_COUNT
            ):

                file_path = (
                    self.workspace /
                    f"{output_prefix}_{index}.csv"
                )

                fh = open(
                    file_path,
                    "w",
                    newline="",
                    encoding="utf-8"
                )

                writer = csv.writer(fh)

                writer.writerow(columns)

                handles[index] = fh
                writers[index] = writer

            with open(
                source_file,
                "r",
                encoding="utf-8"
            ) as dataset:

                reader = csv.DictReader(
                    dataset
                )

                for row in reader:

                    uid = int(
                        row["user_id"]
                    )

                    partition_id = (
                        compute_partition(uid)
                    )

                    writers[
                        partition_id
                    ].writerow(row.values())

        finally:

            for fh in handles.values():
                fh.close()