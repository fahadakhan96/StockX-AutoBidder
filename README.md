# StockX-AutoBidder
This is an auto-bidder that I built using Python &amp; Selenium for the website [StockX](https://stockx.com).

## Usage instructions
1.	Enter your StockX account email address. Make sure it’s correct.
2.	Enter your StockX account password. Make sure it’s correct.
3.	Open your preferred browser and go to https://stockx.com and select the category, brand and sub-category you want to bid on. Selecting the sub-category is optional.
4.	Copy the address bar in the URL and paste it into the URL text box.
5.	Make sure the URL is in the following format: https://stockx.com/<brand>/<sub-category>. 
    •	Examples of valid URLs:
        •	https://stockx.com/supreme
        •	https://stockx.com/supreme/headwear
    •	Examples of invalid URLs:
        •	https://stockx.com
        •	stockx.com/supreme
        •	https://www.stockx.com/supreme
6.	Keep the `Headless` checkbox unchecked. Headless mode means that the bot will run in the background and you will not be able to view what it’s doing. Moreover, headless mode is currently buggy with Google Chrome.
7.	If you want to restrict the bot to bid on a fixed number of products, check the `Restrict` checkbox and enter the number in the textbox below it. Otherwise, the bot will bid on all products available.
8.	Click the `Start` button to start the bot.
9.	In order to manually close the program and quit the bot, click on the `Close` button on the top-right only once. It will finish all pending processes, properly cleanup any locked resources and then quit itself.
10.	The bot keeps a record of the items it has bid on in the file `stockx_bids.csv`. This file can be opened with MS Excel. Please don’t delete or modify this file. This file is important for the program to function correctly. The program will automatically create this file if it is not present.
11.	The program also requires `chromedriver.exe` to be in the same folder as the `main.py` and the `stockx_bids.csv`. This file is also important for the program to function correctly. Please don’t delete this file or try to open it manually.
  
## Making it work with Firefox
1. The Selenium webdriver in `StockX.py` needs to be changed from `Chrome` to `Firefox`.
2. You'll need to include the `geckodriver.exe` file in the same directory as `main.py` and other files.
3. The GUI can give an option to open with either _Firefox_ or _Chrome_ (or other browsers). PRs are welcome.
