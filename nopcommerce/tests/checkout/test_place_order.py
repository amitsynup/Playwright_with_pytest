import os
import json
from decimal import Decimal

import pytest as pytest

from nopcommerce.src.pages.CheckoutPage import CheckoutPage
from nopcommerce.dbconnection.db_connect import connect_to_db
from nopcommerce.src.utils.TestUtils import convert_currency_to_int, convert_price_to_float, calculate_sum


class TestProductCheckout:

    def get_values_from_db(self, products, column_name):
        query = f"SELECT {column_name} FROM E_Commerce WHERE Products_name IN ({', '.join(['%s'] * len(products))})"

        connection, cursor = connect_to_db()

        try:
            cursor.execute(query, tuple(products))
            records = cursor.fetchall()
            return [record[0] for record in records]
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def get_prices_from_db(self, products):
        return self.get_values_from_db(products, "Price")

    def get_tax_from_db(self, products):
        return self.get_values_from_db(products, "Tax")

    def get_products_to_select(self):
        # Get the directory of the current script
        script_directory = os.path.dirname(os.path.realpath(__file__))

        # Construct the full path to the test data file
        relative_path = "../../src/Testdata/testdata.json"
        full_path = os.path.abspath(os.path.join(script_directory, relative_path))

        # Load products_to_select from the test data file
        with open(full_path, 'r') as file:
            data = json.load(file)

        return data.get("products_to_select", [])

    @pytest.mark.regression
    def test_product_checkout(self, set_up_tear_down, login_to_app, browser_type, browsers_config) -> None:
        page = set_up_tear_down  # Call the fixture to get the Page instance
        product_page = login_to_app

        # Access browser configuration from browsers_config
        print("Selected browser:", browser_type)
        print("Browser configuration:", browsers_config["browsers"][browser_type])

        # Retrieve the list of products to select from the test data
        products_to_select = self.get_products_to_select()

        # Click on each product to add it to the cart
        for product_name in products_to_select:
            product_page.click_add_to_cart_or_remove_from_cart(product_name)

        # Go to the cart and proceed to checkout
        product_page.click_card_icon().click_checkout_button() \
            .enter_checkout_details("fname", "Lname", "12345") \
            .click_continue()

        # Print all selected product names and prices
        selected_product_names = CheckoutPage(page).get_product_names()
        selected_product_prices = CheckoutPage(page).get_product_prices()
        # Convert currency strings to integers for easy comparison
        item_total_price = [convert_currency_to_int(price) for price in selected_product_prices]
        print("actual product price:", item_total_price)

        # Get prices from the database for the selected products
        prices_from_db = self.get_prices_from_db(selected_product_names)
        print("Prices from DB:", prices_from_db)
        # Assert that the prices match
        # Assert that the prices match after converting Decimal to string
        assert [str(price) for price in item_total_price] == [str(price) for price in
                                                              prices_from_db], "Prices do not match"

        total_from_page = CheckoutPage(page).get_item_total_label()
        print(total_from_page)
        total_price_in_float = convert_price_to_float(total_from_page)  # Use float for numerical value
        print(total_price_in_float)
        # Calculate the sum of item_total_price
        sum_of_prices = calculate_sum(item_total_price)

        print("Item total price:", +sum_of_prices)
        # Verify that the sum matches total_price_in_float
        assert sum_of_prices == total_price_in_float, f"Sum of prices does not match total: {sum_of_prices} != {total_price_in_float}"

        total_tax = CheckoutPage(page).get_tax_label()
        total_tax_price_in_float = convert_price_to_float(total_tax)
        # Convert total_tax_price_in_float to Decimal
        total_tax_price_d = Decimal(str(total_tax_price_in_float))
        print(total_tax_price_in_float)
        # Get the tax values from the database for the selected products
        tax_from_db = self.get_tax_from_db(selected_product_names)
        # Calculate the sum of tax_from_db
        sum_of_tax_from_db = calculate_sum(tax_from_db)
        print(sum_of_tax_from_db)
        # Verify that the sum matches total_tax_price_in_float
        assert sum_of_tax_from_db == total_tax_price_d, f"Sum of tax values does not match total tax: {sum_of_tax_from_db} != {total_tax_price_d}"

        total_price = CheckoutPage(page).get_total_label()
        total_price_f = convert_price_to_float(total_price)
        print(total_price_f)
        # assert round(total_price_in_float, 2) == round(total_tax_price_d + Decimal(str(sum_of_prices)), 2)

        # Click finish
        CheckoutPage(page).click_finish()

        # Confirm the order
        confirmation_message = CheckoutPage(page).get_confirmation_message()

        # Verify total in the confirmation message
        expected_message = "Thank you for your order!"
        page.wait_for_timeout(500)
        assert expected_message in confirmation_message, f"Expected: '{expected_message}', Actual: '{confirmation_message}'"

