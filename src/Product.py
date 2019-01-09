import constants
import math
from time import sleep
from selenium.webdriver.common.keys import Keys


class Product:
    def __init__(self, browser, url):
        self.browser = browser
        self.url = url
        self.retail_price = 0
        self.bid_value = 0
        self.size_idx = 0

    def fetch_retail_price(self):
        details = self.browser.find_elements_by_class_name(
            constants.PRODUCT_DETAIL_CLASS_NAME)
        for detail in details:
            is_price, price = self.is_detail_price(detail)
            if is_price:
                self.retail_price = price
                break

    def calculate_bid_value(self):
        self.bid_value = round(self.retail_price - constants.SHIPPING_PRICE)
        return self.bid_value

    def select_size_all(self):
        try:
            print('Selecting size to all')
            size_dropdown = self.browser.find_element_by_xpath(
                constants.SIZE_DROPDOWN_CSS_SELECTOR)
            all_btn = self.browser.find_element_by_xpath(
                constants.ALL_SIZES_BUTTON_CSS_SELECTOR)

            size_dropdown.click()
            all_btn.click()
        except:
            pass

    def is_detail_price(self, detail):
        price_text = detail.find_element_by_xpath(
            constants.PRICE_TEXT_IN_PRODUCT_DETAIL_XPATH).text
        is_price = price_text[0] == '$' and price_text[1:].isdigit()
        if is_price:
            return True, int(price_text[1:])

        return False, 0

    def fetch_product_page(self):
        self.browser.get(self.url)

    def is_bid_present(self):
        try:
            self.browser.find_element_by_class_name(
                constants.BID_EXISTS_BANNER_CLASS_NAME)
            return True
        except:
            return False

    def bypass_understand_page(self):
        try:
            print('Understanding')
            self.browser.find_element_by_class_name(
                constants.I_UNDERSTAND_CONTAINER_CLASS_NAME)
            sleep(1)
            self.click_understand()
        except:
            print('Skipped understanding')
            pass

    def click_understand(self):
        print('Called click understand')
        understand_btn = self.browser.find_element_by_class_name(
            'button-green')
        understand_btn.click()
        print('Clicked understand')

    def manage_sizes(self):
        try:
            grid = self.browser.find_element_by_class_name('size-select-grid')
            size_btns = grid.find_elements_by_css_selector(
                '.grid-tile.buy-tile')
            size_btns[self.size_idx].click()
            self.create_bid()
            self.size_idx += 1

            if self.size_idx >= len(size_btns):
                return

            if self.browser.current_url != self.url:
                self.fetch_product_page()
            self.goto_bid_page()
        except:
            self.create_bid()

    def goto_bid_page(self):
        self.select_size_all()
        bid_btn = self.browser.find_element_by_id('bid-buy-button')
        bid_btn.click()
        self.bypass_understand_page()
        self.manage_sizes()

    def create_bid(self):
        print('Creating bid')
        bid_input = self.browser.find_element_by_xpath(
            '//input[@name="ask-amount"]')
        bid_input.send_keys(self.bid_value)

        try:
            warning_text = self.browser.find_element_by_class_name(
                'warning-text')
            warning_text = warning_text.text
            min_bid = warning_text[-3:]
            if min_bid[0] == '$':
                min_bid = min_bid[1:]

            self.bid_value = int(min_bid)
            bid_input.send_keys(
                Keys.chord(Keys.CONTROL, "a"), str(self.bid_value))
        except:
            pass

        review_btn = self.browser.find_element_by_class_name('button-green')
        review_btn.click()

        confirm_btn = self.browser.find_element_by_css_selector(
            constants.BID_CONFIRM_BUTTON_CSS_SELECTOR)
        confirm_btn.click()
