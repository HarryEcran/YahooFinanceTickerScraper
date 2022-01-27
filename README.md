# YahooFinanceTickerScraper
A small python scrypt to scrape most international stock tickers from Yahoo Finance using minimal amounts of html requests.
This is done by exploiting the fact that Yahoo Finance allows for single letter searches.
The low amount of html requests is archieved by asking for up to 7000 stock tickers at once, 
this seems to be the maximum amount of stocks Yahoo Finance is able to return before starting to return html code containing everything except the stock tickers.

Last tested on 27/01/2022, the regular expressions or URL could change at any time breaking the script.
Made by Harry Ecran
