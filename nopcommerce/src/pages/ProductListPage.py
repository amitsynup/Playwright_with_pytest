from nopcommerce.src.pages.CartPage import CartPage


class ProductListPage:
    def __init__(self,page):
        self.page=page

        self._products_header= page.locator("//span[@class='title']")
        self._burger_menu = page.locator("//button[@id='react-burger-menu-btn']")
        self._logoutbutton = page.locator("//a[@id='logout_sidebar_link']")
        self._cart_icon=page.locator("//a[@class='shopping_cart_link']")



    @property
    def product_header(self):
        #it return selector of product header text
        return self._products_header

    def clickburger_menu_btn(self):
        self._burger_menu.click()

    def click_logout(self):
        self._logoutbutton.click()

    def do_logout(self):
        self.clickburger_menu_btn()
        self.click_logout()

    def get_add_remove_cart_locator(self,prodouct):
        return self.page.locator(f"//div[text()='{prodouct}']/ancestor::div[@class='inventory_item_label']/following-sibling::div//button")
    def click_add_to_cart_or_remove_from_cart(self,prodouct):
        self.get_add_remove_cart_locator(prodouct).click()
        return self
    def click_card_icon(self):
        self._cart_icon.click()
        return CartPage(self.page)