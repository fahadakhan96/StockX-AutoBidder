STOCKX_BASE_URL = 'https://stockx.com/'
LOGIN_URL = STOCKX_BASE_URL + 'login'

SHIPPING_PRICE = 13.95

CSV_NAME = 'stockx_bids.csv'

BROWSE_TABLE_ID = 'browse-table'

PRODUCT_DETAIL_CLASS_NAME = 'detail'
BID_EXISTS_BANNER_CLASS_NAME = 'singleBidAsk'
I_UNDERSTAND_CONTAINER_CLASS_NAME = 'works-buy-sell'

LOGIN_EMAIL_INPUT_XPATH = '//input[@name="email"]'
LOGIN_PASSWORD_INPUT_XPATH = '//input[@name="password"]'
PRODUCTS_IN_BROWSE_TABLE_XPATH = 'tbody/tr/td/a'
LIST_LAYOUT_BUTTON_XPATH = '//button[@name="list"]'
LOAD_MORE_XPATH = '//div[@class="browse-load-more"]/button'
PRICE_TEXT_IN_PRODUCT_DETAIL_XPATH = 'span'

BID_CONFIRM_BUTTON_CSS_SELECTOR = 'div.button-bar:nth-child(2) > div:nth-child(1) > button:nth-child(2)'
BID_FINISH_BUTTON_CSS_SELECTOR = 'button.right-button:nth-child(1)'
SIZE_DROPDOWN_CSS_SELECTOR = '/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div/div/div[1]/button'
ALL_SIZES_BUTTON_CSS_SELECTOR = '/html/body/div[1]/div[1]/div[2]/div[2]/span/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/ul/li[1]/div'