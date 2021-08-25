import datetime

import item
import options
import utils


def purge_old_price_data(text_box=None):
    """Removes price data from items with more than x price points, or removes price points older than y days"""
    count = 0
    count += purge_list(item.product_list)
    count += purge_list(item.material_list)
    utils.send_warning('{} price points purged successfully.'.format(str(count)), text_box)


def purge_list(item_list):
    count = 0
    for x in item_list:
        if len(x.price_data) > 0:
            while len(x.price_data) > options.price_purge_amount:
                x.price_data.pop(0)
                count += 1
            # delta = datetime.datetime.now() - x.price_data[0].time
            while len(x.price_data) > 0 and (
                    datetime.datetime.now() - x.price_data[0].time).days > options.price_purge_time:
                x.price_data.pop(0)
                count += 1
    return count


def find_old_prices(text_box=None):
    """Finds items without recent price data"""
    pass
