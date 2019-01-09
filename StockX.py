import threading
import pandas as pd
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

import constants
from Product import Product


class StockX(threading.Thread):
    def __init__(self,
                 master,
                 username,
                 password,
                 url,
                 restrict_bid_num=False,
                 allowed_num=0,
                 headless=True):
        super().__init__()
        self.master = master
        self.username = username
        self.password = password
        self.url = url
        self.restrict_bid_num = restrict_bid_num
        self.initial_success = self.master.success_bids.get()
        self.allowed_num = allowed_num
        self.force_quit = False

        self.df_successful_bids = pd.read_csv(constants.CSV_NAME, index_col=0)

        self.brand = ''
        self.sub_category = ''

        splitted_url = self.url[len(constants.STOCKX_BASE_URL):].split('/')
        if len(splitted_url) == 2:
            self.brand, self.sub_category = splitted_url
        elif len(splitted_url) == 1:
            self.brand = splitted_url[0]

        self.no_of_successful_bids = 0
        self.product_urls = []
        self.start_pointer = 0
        self.options = Options()
        self.options.headless = headless

    def cleanup(self):
        print('StockX destructor')
        self.browser.close()
        print(self.df_successful_bids.head())
        self.df_successful_bids.to_csv(constants.CSV_NAME)
        self.master.can_quit_now()
        print('After writing')

    def run(self):
        self.master.status.set('Starting browser...')
        self.browser = Chrome(options=self.options)
        self.login()
        self.browser.get(self.url)
        self.change_to_list_layout()
        self.fetch_and_loop_urls()

    def fetch_and_loop_urls(self):
        self.fetch_product_urls()
        self.loop_product_urls()

    def fetch_product_urls(self):
        if self.force_quit:
            self.master.cleanup()
            return

        self.master.status.set('Fetching product urls...')
        table = self.browser.find_element_by_id(constants.BROWSE_TABLE_ID)
        products = table.find_elements_by_xpath(
            constants.PRODUCTS_IN_BROWSE_TABLE_XPATH)[self.start_pointer:]
        urls = [product.get_attribute('href') for product in products]
        self.start_pointer += len(urls)
        self.product_urls = urls

    def loop_product_urls(self):
        for url in self.product_urls:
            self.bid_on_product(url)
            if self.force_quit or (
                    self.restrict_bid_num
                    and self.no_of_successful_bids >= self.allowed_num):
                self.master.status.set('Quitting...')
                self.master.cleanup()
                return

        self.fetch_more()
        self.master.status.set('Quitting...')
        self.master.cleanup()

    def bid_on_product(self, url):
        self.master.status.set('Bidding on product...')
        if url in self.df_successful_bids.index:
            print('Skipping cos in csv')
            return False

        product = Product(self.browser, url)
        product.fetch_product_page()
        if product.is_bid_present():
            print('Skipping otherwise')
            self.write_bid_to_df(url, -1)
            return False

        product.fetch_retail_price()
        bid_value = product.calculate_bid_value()
        product.goto_bid_page()
        # sleep(1)
        # product.create_bid()
        self.no_of_successful_bids += 1
        self.master.status.set('Bid successful!')
        self.master.success_bids.set(self.initial_success +
                                     self.no_of_successful_bids)
        self.write_bid_to_df(url, bid_value)
        return True

    def fetch_more(self):
        print('Fetching more...')
        try:
            load_more_btn = self.browser.find_element_by_xpath(
                constants.LOAD_MORE_XPATH)
            load_more_btn.click()
            sleep(2)
            self.fetch_and_loop_urls()
        except:
            return

    def login(self):
        if self.force_quit:
            return

        self.master.status.set('Logging in...')
        self.browser.get(constants.LOGIN_URL)
        email_input = self.browser.find_element_by_xpath(
            constants.LOGIN_EMAIL_INPUT_XPATH)
        email_input.send_keys(self.username)
        pwd_input = self.browser.find_element_by_xpath(
            constants.LOGIN_PASSWORD_INPUT_XPATH)
        pwd_input.send_keys(self.password)
        pwd_input.submit()
        sleep(1)

    def change_to_list_layout(self):
        print('Changing to list layout...')
        list_btn = self.browser.find_element_by_xpath(
            constants.LIST_LAYOUT_BUTTON_XPATH)
        list_btn.click()

    def write_bid_to_df(self, url, bid_value):
        if self.force_quit:
            return

        print('Writing to DataFrame')
        self.df_successful_bids.loc[url] = [
            self.brand, self.sub_category, bid_value
        ]

        with open(constants.CSV_NAME, 'a') as f:
            f.write('{},{},{},{}\n'.format(url, self.brand, self.sub_category,
                                           bid_value))
