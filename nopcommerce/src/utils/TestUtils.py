import re

def convert_price_to_float(price_string):
    """
    Converts a string like "Item total: $105.96000000000001" to a float.

    Args:
        price_string: The string containing the price.

    Returns:
        The price as a float.
    """

    # Remove non-numeric characters and the currency symbol.
    price_string = re.sub(r"[^\d\-.]", "", price_string)
    return float(price_string)
def convert_currency_to_int(currency_str):
    # Remove the dollar sign and convert to float
    return float(currency_str.replace('$', ''))


def calculate_sum(values):
    return sum(values)
