crafting_queue_length = 5
"""the length of time (in days) for matching a stock and a sale (if the gap is longer than this, match_stock not count 
it as a match) """
time_gap = 7
"""the number of days over which price data will be purged"""
price_purge_time = 14
"""the amount of price points over which old data will be purged"""
price_purge_amount = 10


def reset_to_defaults():
    crafting_queue_length = 5
    time_gap = 7
    price_purge_time = 14
    price_purge_amount = 10
