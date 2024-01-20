
class CheckoutPage:
    def __init__(self,page):
        self.page=page
        self._first_name=page.locator("//input[@id='first-name']")
        self._last_name=page.locator("//input[@id='last-name']")
        self._zipcode=page.locator("//input[@id='postal-code']")
        self._continue=page.locator("//input[@id='continue']")
        self._finish=page.locator("//button[@id='finish']")
        self._confirm_message=page.locator("//h2[@class='complete-header']")
        self._product_names = page.locator("//div[@class='inventory_item_name']")
        self._product_prices = page.locator("//div[@class='inventory_item_price']")
        self._item_total_label = page.locator("//div[@class='summary_subtotal_label']")
        self._tax_label = page.locator("//div[@class='summary_tax_label']")
        self._total_label = page.locator(".summary_total_label")


    def enter_first_name(self,F_name):
        self._first_name.fill(F_name)
        return self
    def enter_last_name(self,L_name):
        self._last_name.fill(L_name)
        return self

    def enter_zipCode(self,zip):
        self._zipcode.fill(zip)
        return self
    def enter_checkout_details(self,f_name,l_name,Zip_code):
        self.enter_first_name(f_name).enter_last_name(l_name).enter_zipCode(Zip_code)
        return self
    def click_continue(self):
        self._continue.click()
        return self

    def click_finish(self):
        self._finish.click()
        return
    def get_confirmation_message(self):
        return self._confirm_message.text_content()

    def get_product_names(self):
        # Use all() method to get a list of elements
        product_elements = self._product_names.all()
        return [element.text_content() for element in product_elements]

    def get_product_prices(self):
        # Use all() method to get a list of elements
        price_elements = self._product_prices.all()
        return [element.text_content() for element in price_elements]

    def get_item_total_label(self):
        return self._item_total_label.text_content()

    def get_tax_label(self):
        return self._tax_label.text_content()

    def get_total_label(self):
        return self._total_label.text_content()




