#Simple script to extract a large quantity of tickers from global stock exchanges.
#This script exploits the fact that Yahoo lets us search for individual letters in all stocks and can display up to 7000 results at once on a html page.
#Last tested on 27/01/2022
#Made by Harry Ecran

#Basic functionality
import re
import string

#Webscraping
from bs4 import BeautifulSoup
import requests

#File management
import csv
from pathlib import Path

Alphabet = list(string.ascii_lowercase)

#Get directory.
Directory = str(Path(__file__).resolve().parent)

#Required as Yahoo blocks scrape requests when using requests.get() with the default headers.
RequestsHeaders = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

#When requesting more than 7000 rows of tickers at once, Yahoo seems to stop sending the data.
RowsPerPage = str(7000)

print("Starting to request data from https://finance.yahoo.com/.")

OutputLocation = Directory + "\\YahooTickers\\Raw\\"

#Create folder structure if it does not yet exist.
Path(OutputLocation).mkdir(parents=True, exist_ok=True)

#Going over every letter to get as many different tickers as possible. Seeing as at least with one letter will result in the stock being found.
for letter in Alphabet:
    print("Currently doing: " + letter)

    URLToScrape = "https://finance.yahoo.com/lookup/equity?s=" + letter + "&c=" + RowsPerPage

    #Dowloading html and extracting ticker data.
    HtmlText = requests.get(URLToScrape, headers=RequestsHeaders).text 
    Soup = BeautifulSoup(HtmlText, "lxml")
    Stocks = Soup.find_all("tr", class_ = re.compile("data-row.+")) 

    Header = ["Symbol", "Name", "Last Price", "Industry/Category", "Type", "Exchange"]

    #Cleaning the data and writing it to a csv file to be available later.
    with open(OutputLocation + "Output_tickers_" + letter, "w", encoding='UTF8') as fh_Tickers:

        Writer = csv.writer(fh_Tickers)
        Writer.writerow(Header)

        for ticker in Stocks:
            DataRow = []
            DataStock = ticker.find_all("td")
            
            for data in DataStock:
                DataRow.append(data.text)

            Writer.writerow(DataRow)
        
    fh_Tickers.close()

print("Done with webscraping.")

#Here duplicates are deleted and all tickers are combined into a single file.
print("Started deletion of duplicates and combination into single file.")

InputLocation = Directory + "\\YahooTickers\\Raw\\"
OutputLocation = Directory + "\\YahooTickers\\Combined\\"

Path(InputLocation).mkdir(parents=True, exist_ok=True)
Path(OutputLocation).mkdir(parents=True, exist_ok=True)

OutputData = []
FoundTickers = []

#Going over all previously created files and getting rid of duplicates.
for letter in Alphabet:
    print("Currently doing: " + letter)
    with open(InputLocation + "Output_tickers_" + letter, "r", encoding='UTF8') as fh_Tickers:

        Reader = csv.reader(fh_Tickers)
        Header = next(Reader)

        for row in Reader:
            if row == []: #Required because of possible empty lines in the csv files.
                continue

            if not (row[0] in FoundTickers):
                OutputData.append(row)
                FoundTickers.append(row[0])

    fh_Tickers.close()

Header = ["Symbol", "Name", "Last Price", "Industry/Category", "Type", "Exchange"]

#Writing all tickers to a single file.
with open(OutputLocation + "Output_tickers_combined", "w", encoding='UTF8') as fh_Tickers:

        Writer = csv.writer(fh_Tickers)
        Writer.writerow(Header)

        for ticker in OutputData:
            Writer.writerow(ticker)
    
fh_Tickers.close()

print("Completed deletion of duplicates and combination into single file.")

#Splitting all tickers to their respective markets.
print("Start stock seperation based on their market.")

InputLocation = Directory + "\\YahooTickers\\Combined\\"
OutputLocation = Directory + "\\YahooTickers\\SplitPerMarket\\"

Path(InputLocation).mkdir(parents=True, exist_ok=True)
Path(OutputLocation).mkdir(parents=True, exist_ok=True)

ExchangesDic = {}
AllExchanges = []

#Ordening the stocks by market.
with open(InputLocation + "Output_tickers_combined", "r", encoding='UTF8') as fh_Tickers:

        Reader = csv.reader(fh_Tickers)
        Header = next(Reader)

        for row in Reader:
            if row == []:
                continue
            
            if not (row[5] in AllExchanges):
                AllExchanges.append(row[5])
                ExchangesDic[row[5]] = []
            
            ExchangesDic[row[5]].append(row)
    
fh_Tickers.close()

Header = ["Symbol", "Name", "Last Price", "Industry/Category", "Type", "Exchange"]

#Writing each market to a seperate file.
for key in ExchangesDic:
    with open(OutputLocation + "Output_tickers_" + key, "w", encoding='UTF8') as fh_Tickers:

            Writer = csv.writer(fh_Tickers)
            Writer.writerow(Header)

            for ticker in ExchangesDic[key]:
                Writer.writerow(ticker)
        
    fh_Tickers.close()

print("Completed stock seperation based on their market.")