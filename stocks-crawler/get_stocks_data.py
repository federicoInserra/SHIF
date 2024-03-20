import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import yfinance
from pymongo import MongoClient
import certifi
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# ==============================  DB CONNECTION SETUP  ==============================
DB = getenv("MDB_DB",default="shif")
COLLECTION = "stocks"
MONGODB_URI = getenv('MDBCONNSTR')

client = MongoClient(
    MONGODB_URI, tlsCAFile=certifi.where())

collection = client[DB][COLLECTION]

# ==================================================================================


# ==============================  GET STOCK DATA  =================================

def get_prices_history(from_day, to_day, symbol):

    print(f"Downloading data for {symbol} .....")
    yfinance.pdr_override()
    df = pdr.get_data_yahoo([symbol], from_day, to_day)

    prices = []
    # Manipulate the data to create a document representing the stock price
    for day in df.index:

        stock = {
            "symbol": symbol,
            "day": day,
            "price": round(df["Open"][day], 2)
        }

        prices.append(stock)

    return prices


# ==============================  MAIN  =================================
DAYS_OF_DATA = 3653  # These is to get the last 10 years of stock data

# Define dates interval
to_day = dt.datetime.now()
from_day = to_day - dt.timedelta(days=DAYS_OF_DATA)

# Lists of stocks to retrieve
# TOP 20 COMPANIES SYMBOL, UPDATED AT 4TH MARCH 2024, https://stockanalysis.com/list/biggest-companies/
top20_stocks_list_symbol = ["MSFT", "AAPL", "NVDA", "GOOGL", "META", "LLY", "TSM", "AVGO", "TSLA", "V", "NVO", "JPM", "WMT", "UNH",
                            "MA", "XOM", "ASML", "JNJ", "HD", "PG"]

# other_stocks = ["COST", "TM", "AMD", "MRK", "ABBV", "ORCL", "CRM", "CVX", "BAC", "NFLX", "ADBE", "KO", "ACN", "PEP", "SAP", "FMX", "TMO", "LIN", "MCD", "NVS", "ABT", "DIS", "SHEL", "AZN", "CSCO", "WFC", "TMUS", "INTC", "DHR", "INTU", "QCOM", "BABA", "AMAT", "GE", "IBM", "CAT", "VZ", "PDD", "CMCSA", "AXP", "TXN",
#                 "UNP", "NKE", "NOW", "BX", "TTE", "AMGN", "HSBC", "MS", "BHP", "PFE", "ISRG", "LOW", "PM", "HDB", "RY", "SYK", "COP", "SPGI", "HON", "UPS", "LRCX", "GS", "PLD", "BLK", "MUFG", "UL", "BA", "T", "SCHW", "BUD", "BKNG", "RTX", "ETN", "SNY", "ELV", "MDT", "TJX", "NEE", "PGR", "VRTX", "PBR", "C", "TD", "SONY"]

other_stocks = ["SE","PEP","HSY","FUN","FXI","MBLY","XRP","XLU","CEVA","MET","DOC","NTR","BNTX","X","CSCO","MCD","HEFA","AGI","FIS","BGY","BIDU","LIN","SPX","PTEN","CNM","EPR","UAL","ADSK","SNDX","BTBT","LULU","CRD.B","MNDY","AVAV","M","DRV","EOSE","VERI","TMUS","GIL","USPH","HPE","PSTG","NYCB","BRK.B","NIO","WRN","PFE","WHR","SQM","NTAP","AXGN","PTON","BSX","MUR","AVDL","PARA","CVGI","RIOT","GDXJ","SEAT","CYC","VEEV","COWZ","CRWD","XHR","SQ","FICO","DRQ","ISRG","XLF","RL","CUBE","EBAY","T","TFX","TSVT","RSP","TOST","EQIX","AMD","HQY","TSHA","EHC","JD","PYPL","QDTE","ACXP","DKNG","CALF","FTEC","SATS","EVRG","PX","GEF.B","MDT","AIR","STNE","BBBL","THO","SIRI","MSOX","LEGH","KOS","BTC","TDUP","GXO","VIAV","O","ROKU","YANG","FUBO","DLR","KSS","URA","FMC","IJH","COPJ","AGG","FWRG","PPTA","RDDT","DEO","THC","SIG","LIT","ILMN","TJX","ESS","HMN","CLX","PNM","GECC","AY","CELH","CNTB","BBIO","SCOR","CHWY","LRCX","EXAS","AAVXF","SBUX","CIFR","OXY","CSL","GEHC","MANH","CSIQ","KNTK","CARA","CLMB","HIG","WKHS","MS","CVX","IYC","IRTC","DOGE","APAM","SBAC","NFE","ETH","ORLA","SETM","FSUGY","BRK.A","MCR","UPS","MU","HON","BBWI","GIS","SIEGY","XHYF","COO","BETE","JKS","SHOP","CAL","HUYA","DG","NKE","BROS","ARI","BKKT","TGT","CECO","EME","ORA","NKTR","XHYC","ALK","FM","INTT","SAVE","F","SVC","EYEN","MOS","SPR","ADBE","CSHI","YY","FSTR","KO","CFLT","ALEX","LITE","BANR","BATRA","DSP","TPR","CARR","SWN","RAIL","PLTR","BCS","WTIU","WSM","ZION","D","KLIC","BNY","STC","DASH","RDNT","PLUG","NTES","AVA","DSGN","ALPN","CRC","USD","IVW","BX","YORW","DELL","LUV","ZIM","SAIA","BMY","LYB","BHP","PNC","GDX","LTRX","EMXC","DSX","BBAI","SAIC","PDD","HII","FBRT","VUZI","MTZ","RJF","MD","AMZN","TD","XPO","BWLLF","GLD","QNBC","BDX","BBBS","HASI","JEPI","JILL","OLLI","RFIL","XP","KC","ORCL","BA","NXT","VSCO","CLF","AKYA","BAX","QGRO","ES","BPMC","OILU","GTLB","WDC","MOGO","ALB","PRS","CMTL","CTLT","DGS","CNQ","TRUP","AIG","TDW","AMT","PLD","WBD","TMF","BURL","HYSA","ALGN","XHYI","CROX","ALTI","IP","PLNT","KGC","ZS","CM","IYR","SOHU","SOL","RGLD","SNOW","HTHT","XHYT","SOUN","AMRX","BPOP","AEO","SFIX","ABT","SYK","LABD","ATOS","IBM","APP","MLM","AAL","BOX","BIL","PPA","WIX","CWEB","IXUS","GSL","EKSO","PCT","GEO","ESTC","BNDI","BBY","RLMD","AFRM","BLK","MO","UCBI","TXT","MRVL","KARS","FSLR","MASS","DYNF","CEG","FTAI","DLO","EPAM","LMT","DIN","HRL","S","GOOG","GGG","BE","DECK","ARM","XLM","EWC","GNK","AMKR","SMCI","AKRO","GS","CGEN","FIX","TDS","TFLO","EFA","HRB","TRV","TMV","MDY","LAND","WMT","EQT","NRGU","APO","BUFZ","TM","WRK","GQI","JWN","LTRN","FDX","KOLD","BUD","CI","MSFT","SPYI","SUI","BABA","SOFI","MRK","NEO","ROK","HRZN","FL","OIH","SIX","BOOM","AXP","JBLU","BDSX","ARGX","SOXS","NWPX","SPT","MARB","SOPH"]

stocks = []

# for symbol in top20_stocks_list_symbol:
for symbol in other_stocks:

    stocks += get_prices_history(from_day, to_day, symbol)

# Insert stocks in the database
collection.insert_many(stocks)
