PARTITION_COUNT = 48


def compute_partition(
    user_identifier: int
) -> int:

    return user_identifier % PARTITION_COUNT