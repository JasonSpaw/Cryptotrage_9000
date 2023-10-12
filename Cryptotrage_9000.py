Coinbase_Key = '<Your Key>'
Coinbase_Secret = '<Your Key>'
Gemini_Key = '<Your Key>'
Gemini_Secret = '<Your Key>'
Kraken_Key = '<Your Key>'
Kraken_Secret = '<Your Key>'
Kucoin_Key = '<Your Key>'
Kucoin_Secret = '<Your Key>'
Kucoin_passphrase = "<Your Passphrase>"

import http.client, json, hmac, hashlib, time, base64, requests, datetime, uuid, multiprocessing
import pandas as pd
import numpy as np
from multiprocessing import Pool
import concurrent.futures
import tkinter as tk                    
from tkinter import ttk
from tkinter import filedialog, messagebox, ttk
import sys
import io
from io import StringIO
import os
import webbrowser
import pickle
from PIL import ImageTk, Image


global ku_tickers
global quote_ticker
global CB_Products
global CB_Prod_List
global Kucoin_Prod_List
global Kucoin_Products
global Kraken_Prod_List
global Kraken_Products
global Kraken_Prod_List2
global Kraken_Products2
global Gemini_Prod_List
global Gemini_Products
global Gemini_Prod_List2
global Gemini_Products2
global tri_on_Ccheck
global tri_on_CB
global tri_on_Gemini
global tri_on_Kraken
global tri_on_Kucoin
global tri_results_CB
global filter_list_CB
global comparison_list_CB
global sort_check_CB
global sort_by_CB
global acend_CB
global sorted_subset_CB
global tri_results_Gemini
global filter_list_Gemini
global comparison_list_Gemini
global sort_check_Gemini
global sort_by_Gemini
global acend_Gemini
global sorted_subset_Gemini
global tri_results_Kraken
global filter_list_Kraken
global comparison_list_Kraken
global sort_check_Kraken
global sort_by_Kraken
global acend_Kraken
global sorted_subset_Kraken
global tri_results_Kucoin
global filter_list_Kucoin
global comparison_list_Kucoin
global sort_check_Kucoin
global sort_by_Kucoin
global acend_Kucoin
global sorted_subset_Kucoin
global Cross_results

filtered_subset = pd.DataFrame(columns=["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", "cc3", "v1", "vp1", "v2", 
                "vp2", "v3", "vp3"])

sorted_subset_CB = pd.DataFrame(columns=["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", "cc3", "v1", "vp1", "v2", 
                "vp2", "v3", "vp3"])

filtered_subset_Gemini = pd.DataFrame(columns=["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", "cc3", "v1", "vp1", "v2", 
                "vp2", "v3", "vp3"])

sorted_subset_Gemini = pd.DataFrame(columns=["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", "cc3", "v1", "vp1", "v2", 
                "vp2", "v3", "vp3"])

filtered_subset_Kraken = pd.DataFrame(columns=["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", "cc3", "v1", "vp1", "v2", 
                "vp2", "v3", "vp3"])

sorted_subset_Kraken = pd.DataFrame(columns=["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", "cc3", "v1", "vp1", "v2", 
                "vp2", "v3", "vp3"])

filtered_subset_Ccheck = pd.DataFrame(columns=["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", "cc3", "v1", "vp1", "v2", 
                "vp2", "v3", "vp3"])

sorted_subset_Ccheck  = pd.DataFrame(columns=["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", "cc3", "v1", "vp1", "v2", 
                "vp2", "v3", "vp3"])

tri_on_CB = False
tri_on_Gemini = False
tri_on_Kraken = False
tri_on_Kucoin = False
tri_on_Ccheck = False
sort_check_CB = False

tri_results_CB = pd.DataFrame()

def check_all_CB():
    global CB_Products
    global CB_Prod_List
    timestamp = str(int(time.time())) 
    method = 'GET'
    requestPath = '/api/v3/brokerage/products'
    body = ''

    message = timestamp + method + requestPath + body
    signature = hmac.new(Coinbase_Secret.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()

    conn = http.client.HTTPSConnection("api.coinbase.com")
    payload = ''
    headers = {
    'Content-Type': 'application/json',
    'CB-ACCESS-KEY': Coinbase_Key,
    'CB-ACCESS-SIGN': signature.hex(),
    'CB-ACCESS-TIMESTAMP': timestamp

    }


    conn.request("GET", "/api/v3/brokerage/products", payload, headers)
    res = conn.getresponse()
    data = res.read()
    CB_String = data.decode("utf-8")
    CB_Json = json.loads(str(CB_String))

    CB_Products = {}
    CB_Prod_List = []

    for prod in CB_Json['products']:
        pair_name = prod['product_id']
        CB_Prod_List.append(pair_name)
        CB_Products[f"{pair_name}"] = {}
        CB_Products[f"{pair_name}"]['price'] = prod['price']
        CB_Products[f"{pair_name}"]['price_percentage_change_24h'] = prod['price_percentage_change_24h']
        CB_Products[f"{pair_name}"]['volume_24h'] = prod['volume_24h']
        CB_Products[f"{pair_name}"]['volume_percentage_change_24h'] = prod['volume_percentage_change_24h']
        CB_Products[f"{pair_name}"]['base_increment'] = prod['base_increment']
        CB_Products[f"{pair_name}"]['quote_increment'] = prod['quote_increment']
        CB_Products[f"{pair_name}"]['quote_min_size'] = prod['quote_min_size']
        CB_Products[f"{pair_name}"]['quote_max_size'] = prod['quote_max_size']
        CB_Products[f"{pair_name}"]['base_min_size'] = prod['base_min_size']
        CB_Products[f"{pair_name}"]['base_max_size'] = prod['base_max_size']
        CB_Products[f"{pair_name}"]['base_name'] = prod['base_name']
        CB_Products[f"{pair_name}"]['quote_name'] = prod['quote_name']
        CB_Products[f"{pair_name}"]['quote_currency_id'] = prod['quote_currency_id']
        CB_Products[f"{pair_name}"]['base_currency_id'] = prod['base_currency_id']

    return CB_Products, CB_Prod_List
    
def check_all_Gemini():
    ### Price feed for all ticker symbols

    base_url = "https://api.gemini.com/v1"
    response = requests.get(base_url + "/pricefeed")
    price_feed = response.json()

    Gemini_Products = {}
    Gemini_Prod_List = []

    for prod in price_feed:
        pair_name = prod['pair']
        Gemini_Prod_List.append(pair_name)
        Gemini_Products[f"{pair_name}"] = {}
        Gemini_Products[f"{pair_name}"]['price'] = prod['price']
        Gemini_Products[f"{pair_name}"]['percentChange24h'] = prod['percentChange24h']

    return Gemini_Products, Gemini_Prod_List

def check_all_Kraken():
    Kraken_Json = requests.get('https://api.kraken.com/0/public/Ticker').json()

    All_In_The_Kraken = requests.get('https://api.kraken.com/0/public/Assets').json()

    In_The_Kraken = All_In_The_Kraken['result']
    Kraken_Products = Kraken_Json['result']

    Kraken_Prod_List = []
    for i in Kraken_Json['result'].keys():
        Kraken_Prod_List.append(str(i))

    return Kraken_Products, Kraken_Prod_List, In_The_Kraken

def check_all_Kucoin():
    # Get info for allticker symbols
    url = 'https://api.kucoin.com/api/v1/market/allTickers'
    now = int(time.time() * 1000)
    #data = {}
    #data_json = json.dumps(data)
    str_to_sign = str(now) + 'GET' + '/api/v1/market/allTickers'
    signature = base64.b64encode(
        hmac.new(Kucoin_Secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(
        hmac.new(Kucoin_Secret.encode('utf-8'), Kucoin_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": Kucoin_Key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
        "Content-Type": "application/json" # specifying content type or using json=data in request
    }
    response = requests.request('get', url, headers=headers)
    products = response.json()

    Kucoin_Products = {}
    Kucoin_Prod_List = []
    
    for prod in products['data']['ticker']:
        pair_name = prod['symbol']
        Kucoin_Prod_List.append(pair_name)
        Kucoin_Products[f"{pair_name}"] = {}
        Kucoin_Products[f"{pair_name}"]['symbolName'] = prod['symbolName']
        Kucoin_Products[f"{pair_name}"]['buy'] = prod['buy']
        Kucoin_Products[f"{pair_name}"]['sell'] = prod['sell']
        Kucoin_Products[f"{pair_name}"]['changeRate'] = prod['changeRate']
        Kucoin_Products[f"{pair_name}"]['changePrice'] = prod['changePrice']
        Kucoin_Products[f"{pair_name}"]['high'] = prod['high']
        Kucoin_Products[f"{pair_name}"]['low'] = prod['low']
        Kucoin_Products[f"{pair_name}"]['vol'] = prod['vol']
        Kucoin_Products[f"{pair_name}"]['volValue'] = prod['volValue']
        Kucoin_Products[f"{pair_name}"]['last'] = prod['last']
        Kucoin_Products[f"{pair_name}"]['price'] = prod['last']
        Kucoin_Products[f"{pair_name}"]['averagePrice'] = prod['averagePrice']
        Kucoin_Products[f"{pair_name}"]['takerFeeRate'] = prod['takerFeeRate']
        Kucoin_Products[f"{pair_name}"]['makerFeeRate'] = prod['makerFeeRate']
        Kucoin_Products[f"{pair_name}"]['takerCoefficient'] = prod['takerCoefficient']
        Kucoin_Products[f"{pair_name}"]['makerCoefficient'] = prod['makerCoefficient']
        
    return Kucoin_Products, Kucoin_Prod_List

def formator_Gemini(Gemini_dict, symbol_list):
    new_dict = {}
    new_list = []
    for i in symbol_list:
        base_url = "https://api.gemini.com/v1"
        response = requests.get(base_url + f"/symbols/details/{i}")
        symbols = response.json()
        print(symbols)
        try:
            s1 = symbols['base_currency']
            s2 = symbols['quote_currency']
            gd1 = Gemini_dict[i]["price"]
            gd2 = Gemini_dict[i]["percentChange24h"]
            new_dict[f"{s1}-{s2}"] = {"symbol": i, "price": f"{gd1}", "percentChange24h": f"{gd2}"}
            new_list.append(f"{s1}-{s2}")
        except KeyError:
            print('KeyError')
            continue
    return new_dict, new_list

def formator_Kraken(Kraken_dict, symbol_list):
    new_dict = {}
    new_list = []

    symbol_string = ""
    k = 0

    for i in symbol_list:
        k += 1
        if k < len(symbol_list):
            symbol_string = symbol_string + i + ','
        else:
            symbol_string = symbol_string + i

    print(symbol_string)
    
    corrections = {'XXBT': 'BTC', 'XBT': 'BTC', 'XBT.M': 'BTC.M', 'XETH': 'ETH', 'XETC': 'ETC', 'XLTC': 'LTC',
                   'XDG': 'DOGE', 'XXDG': 'DOGE', 'XXTZ': 'XTZ', 'XXRP': 'XRP', 'XXMR': 'XMR', 'XXLM': 'XLM',
                   'XMLN': 'MLN', 'REPV2': 'REP', 'XREPV2': 'REP', 'REP': 'REPV1', 'XREP': 'REPV1', 'ZUSD': 'USD',
                   'ZEUR': 'EUR', 'ZGBP': 'GBP', 'ZJPY': 'JPY', 'ZCAD': 'CAD'
                  }


    for i in symbol_list:
        print(i)
        try:
            resp = requests.get(f"https://api.kraken.com/0/public/AssetPairs?pair={i}").json()

            s1 = resp["result"][i]["base"]
            s2 = resp["result"][i]["quote"]
            
            if s1 in corrections.keys():
                c1 = corrections[s1]
            else:
                c1 = s1
                
            if s2 in corrections.keys():
                c2 = corrections[s2]
            else:
                c2 = s2
                
            price = Kraken_dict[i]["c"][0]
            lot_volume = Kraken_dict[i]["c"][1]
            vol_t = Kraken_dict[i]["v"][0]
            vol_24h = Kraken_dict[i]["v"][1]

            new_dict[f"{c1}-{c2}"] = {"symbol": i, "altname": resp["result"][i]["altname"], "wsname": resp["result"][i]["wsname"], 
                                      "base": s1, "quote": s2, "price": price, "lot_volume": lot_volume, 
                                      "vol_today": vol_t, "vol_24h": vol_24h}
            new_list.append(f"{c1}-{c2}")
        except KeyError:
            print('KeyError')
            continue
        
    return new_dict, new_list

### Coinbase Basic Functions  ----------------------------------------------------------------------

# not tested
def create_order_Coinbase(product_id, client_order_id, side, quote_size = "", base_size = "", base = "", limit_price = "", post_only = None, order_type = "market"):
    timestamp = str(int(time.time())) 
    method = 'POST'
    requestPath = '/api/v3/brokerage/orders'
    body = ''

    message = timestamp + method + requestPath + body
    signature = hmac.new(Coinbase_Secret.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()

    conn = http.client.HTTPSConnection("api.coinbase.com")

    if order_type == "market" and side == "BUY":
        payload = json.dumps({
        "client_order_id": f"{client_order_id}",
        "product_id": f"{product_id}",
        "side": f"{side}",
        "order_configuration": {
            "market_market_ioc": {
            "quote_size": f"{quote_size}"
            }
        }
        })

    if order_type == "market" and side == "SELL":
        payload = json.dumps({
        "client_order_id": f"{client_order_id}",
        "product_id": f"{product_id}",
        "side": f"{side}",
        "order_configuration": {
            "market_market_ioc": {
            "base_size": f"{base_size}"
            }
        }
        })

    if order_type == "limit":
        payload = json.dumps({
        "client_order_id": f"{client_order_id}",
        "product_id": f"{product_id}",
        "side": f"{side}",
        "order_configuration": {
            "limit_limit_gtc": {
            "base_size": f"{base}",
            "limit_price": f"{limit_price}",
            "post_only": post_only
            }
        }
        })
        
    headers = {
    'Content-Type': 'application/json',
    'CB-ACCESS-KEY': Coinbase_Key,
    'CB-ACCESS-SIGN': signature.hex(),
    'CB-ACCESS-TIMESTAMP': timestamp

    }
    conn.request("POST", "/api/v3/brokerage/orders", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return print(data.decode("utf-8"))

def list_accounts_CB(Coinbase_Key = Coinbase_Key, Coinbase_Secret = Coinbase_Secret):
    timestamp = str(int(time.time())) 
    method = 'GET'
    requestPath = '/api/v3/brokerage/accounts'
    body = ''

    message = timestamp + method + requestPath + body
    signature = hmac.new(Coinbase_Secret.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()

    conn = http.client.HTTPSConnection("api.coinbase.com")
    payload = ''
    headers = {
    'Content-Type': 'application/json',
    'CB-ACCESS-KEY': Coinbase_Key,
    'CB-ACCESS-SIGN': signature.hex(),
    'CB-ACCESS-TIMESTAMP': timestamp
    }
    conn.request("GET", "/api/v3/brokerage/accounts", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return print(data.decode("utf-8"))

def check_account_CB(account_uuid, Coinbase_Key, Coinbase_Secret):
    timestamp = str(int(time.time())) 
    method = 'GET'
    requestPath = f'/api/v3/brokerage/accounts/{account_uuid}'
    body = ''

    message = timestamp + method + requestPath + body
    signature = hmac.new(Coinbase_Secret.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()

    conn = http.client.HTTPSConnection("api.coinbase.com")
    payload = ''
    headers = {
    'Content-Type': 'application/json',
    'CB-ACCESS-KEY': Coinbase_Key,
    'CB-ACCESS-SIGN': signature.hex(),
    'CB-ACCESS-TIMESTAMP': timestamp
    }
    conn.request("GET", f"/api/v3/brokerage/accounts/{account_uuid}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return print(data.decode("utf-8"))

def check_selected_CB(pairs):
    results = []

    if pairs.__class__ == list:
        for pair in pairs:
            print(pair)
            timestamp = str(int(time.time())) 
            method = 'GET'
            requestPath = f"/api/v3/brokerage/products/{pair}"
            body = ''

            message = timestamp + method + requestPath + body
            signature = hmac.new(Coinbase_Secret.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()

            payload = ''
            headers = {
            'Content-Type': 'application/json',
            'CB-ACCESS-KEY': Coinbase_Key,
            'CB-ACCESS-SIGN': signature.hex(),
            'CB-ACCESS-TIMESTAMP': timestamp
            }

            conn = http.client.HTTPSConnection("api.coinbase.com")
            conn.request("GET", f"/api/v3/brokerage/products/{pair}", payload, headers)
            res = conn.getresponse()
            data = res.read()
            results.append(data.decode("utf-8"))
    else:
        timestamp = str(int(time.time())) 
        method = 'GET'
        requestPath = f"/api/v3/brokerage/products/{pairs}"
        body = ''

        message = timestamp + method + requestPath + body
        signature = hmac.new(Coinbase_Secret.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()

        payload = ''
        headers = {
        'Content-Type': 'application/json',
        'CB-ACCESS-KEY': Coinbase_Key,
        'CB-ACCESS-SIGN': signature.hex(),
        'CB-ACCESS-TIMESTAMP': timestamp
        }

        conn = http.client.HTTPSConnection("api.coinbase.com")
        conn.request("GET", f"/api/v3/brokerage/products/{pairs}", payload, headers)
        res = conn.getresponse()
        data = res.read()
        results.append(data.decode("utf-8"))
    return results

def available_tickers_paths(product_list):
    tickers = []
    bi_paths = []
    tri_paths = []
    for i in product_list:
        tick1, tick2 = i.split('-')
        if tick1 not in tickers:
            tickers.append(tick1)
        if tick2 not in tickers:
            tickers.append(tick2)

    for i in tickers:
        for j in tickers:
            if i == j:
                continue
            else: 
                bi_paths.append(f"{i}-{j}")
    for i in tickers:
        for j in tickers:
            for k in tickers:
                if i == j or i == k or j == k:
                    continue
                else: 
                    tri_paths.append(f"{i}-{j}-{k}")
    return tickers, bi_paths, tri_paths

def tri_check_CB(tri_paths, product_list, products_results):
    tri_checked = []
    tri_conversion = []
    for i in tri_paths:
        if i not in tri_checked:
            tick1, tick2, tick3 = i.split('-')
            if f"{tick2}-{tick1}" in product_list:
                c1 = float(products_results[f"{tick2}-{tick1}"]["price"])
                print(f"{tick2}-{tick1}: ",c1)
            elif f"{tick1}-{tick2}" in product_list:
                if float(products_results[f"{tick1}-{tick2}"]["price"]) == 0:
                    c1 = 0
                else:
                    c1 = 1/float(products_results[f"{tick1}-{tick2}"]["price"])
                print(f"{tick2}-{tick1}: ",c1)
            else:
                continue

            if f"{tick3}-{tick2}" in product_list:
                c2 = float(products_results[f"{tick3}-{tick2}"]["price"])
                print(f"{tick3}-{tick2}: ",c2)
            elif f"{tick2}-{tick3}" in product_list:
                if float(products_results[f"{tick2}-{tick3}"]["price"]) == 0:
                    c1 = 0
                else:
                    c2 = 1/float(products_results[f"{tick2}-{tick3}"]["price"])
                print(f"{tick3}-{tick2}: ",c2)
            else:
                continue

            if f"{tick1}-{tick3}" in product_list:
                c3 = float(products_results[f"{tick1}-{tick3}"]["price"])
                print(f"{tick1}-{tick3}: ",c3)
            elif f"{tick3}-{tick1}" in product_list:
                if float(products_results[f"{tick3}-{tick1}"]["price"]) == 0:
                    c3 = 0
                else:
                    c3 = 1/float(products_results[f"{tick3}-{tick1}"]["price"])
                print(f"{tick1}-{tick3}: ",c3)
            else:
                continue

            tri_checked.append(f"{tick1}-{tick2}-{tick3}")
            tri_conversion.append(c1*c2*c3)
    return tri_checked, tri_conversion

# fail
def check_pricebooks_CB(pair, limit='10'):
    
    prod_id = f"?product_id={pair}"
    if limit == '':
        limit_string = ''
    else:
        limit_string = f"&limit={limit}"
    timestamp = str(int(time.time())) 
    method = 'GET'
    requestPath = f"/api/v3/brokerage/product_book{prod_id}{limit_string}"
    body = ''

    message = timestamp + method + requestPath + body
    signature = hmac.new(Coinbase_Secret.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()
    payload = ''
    headers = {
    'Content-Type': 'application/json',
    'CB-ACCESS-KEY': Coinbase_Key,
    'CB-ACCESS-SIGN': signature.hex(),
    'CB-ACCESS-TIMESTAMP': timestamp

    }
    
    conn = http.client.HTTPSConnection("api.coinbase.com")
    conn.request("GET", f"/api/v3/brokerage/product_book{prod_id}{limit_string}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    r_json = data.decode("utf-8")
    return r_json

### Current position in testing ----------------------------------------------------------------------

### will need to figure out how to automate the retrieval of the two factor verification code.
def transfer_CB(profile_id, amount, currency, crypto_address, dest_tag , no_dest, twofact_code, nonce, add_net_fee=False, net=""):
    timestamp = str(int(time.time())) 
    method = 'POST'
    requestPath = "/withdrawals/crypto"
    body = ''

    message = timestamp + method + requestPath + body
    signature = hmac.new(Coinbase_Secret.encode('utf-8'), message.encode('utf-8'), digestmod=hashlib.sha256).digest()

    headers = {
    'Content-Type': 'application/json',
    'CB-ACCESS-KEY': Coinbase_Key,
    'CB-ACCESS-SIGN': signature.hex(),
    'CB-ACCESS-TIMESTAMP': timestamp

    }
    conn = http.client.HTTPSConnection("api.exchange.coinbase.com")
    payload = json.dumps({
    "profile_id": profile_id,
    "amount": amount,
    "currency": currency,
    "crypto_address": crypto_address,
    "destination_tag": dest_tag,
    "no_destination_tag": no_dest,
    "two_factor_code": twofact_code,
    "nonce": nonce,
    "add_network_fee_to_total": add_net_fee,
    "network": net
    })
    conn.request("POST", "/withdrawals/crypto", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return print(data.decode("utf-8"))

def stuff_panda_cross(quote_ticker, num_markets, tickers_1, results_1, tickers_2, results_2, tickers_3 = [], results_3 = [], tickers_4 = [], results_4 = []):
    results = {}
    results['0'] = results_1
    results['1'] = results_2
    if num_markets > 2:
        results['2'] = results_3
    if num_markets > 3:
        results['3'] = results_4
    
    tick_list = []
    for i in tickers_1:
        tick1, tick2 = i.split('-')
        if tick1 not in tick_list:
            tick_list.append(tick1)
        if tick2 not in tick_list:
            tick_list.append(tick2)
        
    for i in tickers_2:
        tick1, tick2 = i.split('-')
        if tick1 not in tick_list:
            tick_list.append(tick1)
        if tick2 not in tick_list:
            tick_list.append(tick2)
            
    if num_markets > 2:
        for i in tickers_3:
            tick1, tick2 = i.split('-')
            if tick1 not in tick_list:
                tick_list.append(tick1)
            if tick2 not in tick_list:
                tick_list.append(tick2)

    if num_markets > 3:
        for i in tickers_4:
            tick1, tick2 = i.split('-')
            if tick1 not in tick_list:
                tick_list.append(tick1)
            if tick2 not in tick_list:
                tick_list.append(tick2)
    
    tick_list.remove(quote_ticker)
    quotes = []
    for i in range(num_markets):
        quote = []
        
        for tick in tick_list:
            try:
                quote.append(float(results[f"{i}"][f"{tick}-{quote_ticker}"]["price"]))
            except KeyError:
                try:
                    quote.append(float(results[f"{i}"][f"{tick}-{quote_ticker}"]["price"]))
                except KeyError:
                    quote.append(float("nan"))
                    continue
                
        quotes.append(quote)

    data_pd = pd.DataFrame(data = {"ticker": tick_list, "price_1": quotes[0], "price_2": quotes[1], "price_3": quotes[2], "price_4": quotes[3]})

    return data_pd

def cross_check(panda, num_markets): 
    cross_results = pd.DataFrame(columns = ["ticker", "gap_1", "gap_2", "gap_3", "gap_4", "gaps_ranked"])
    for i, row in panda.iterrows():
        row_prices = pd.DataFrame(data = {"market": range(4 + 1)[1:], "price": [row["price_1"], row["price_2"], row["price_3"], row["price_4"]]})
        sorted_pricesd = row_prices.sort_values("price", ascending=False)
        sorted_pricesa = row_prices.sort_values("price", ascending=True)
        gaps_ranked = list(sorted_pricesd["market"])
        gaps_ranked = f"{gaps_ranked}"
        gap_1 = float(row["price_1"])/float(sorted_pricesa.iloc[0,:]["price"])
        gap_2 = float(row["price_2"])/float(sorted_pricesa.iloc[0,:]["price"])
        gap_3 = float(row["price_3"])/float(sorted_pricesa.iloc[0,:]["price"])
        gap_4 = float(row["price_4"])/float(sorted_pricesa.iloc[0,:]["price"])
        ticker = row["ticker"]
        row_results = pd.DataFrame(data = {"ticker": ticker, "gap_1": gap_1, "gap_2": gap_2, "gap_3": gap_3, "gap_4": gap_4, "gaps_ranked": gaps_ranked})
        cross_results = pd.concat([cross_results, row_results], ignore_index=True)

    return cross_results

def tri_update_panda_CB(tri_panda, products_results, product_list):
    tri_conversion_list = []
    c1_list = []
    cc1_list = []
    c2_list = []
    cc2_list = []
    c3_list = []
    cc3_list = []
    v1_list = []
    vp1_list = []
    v2_list = []
    vp2_list = []
    v3_list = []
    vp3_list = []
    
    for i in range(len(tri_panda)):
        tick1, tick2, tick3 = tri_panda.iloc[i]["tri_path"].split('-')
        if f"{tick2}-{tick1}" in product_list:
            c1 = float(products_results[f"{tick2}-{tick1}"]["price"])
            c1_list.append(c1)
            cc1_list.append(products_results[f"{tick2}-{tick1}"]["price_percentage_change_24h"])
            v1_list.append(products_results[f"{tick2}-{tick1}"]["volume_24h"])
            vp1_list.append(products_results[f"{tick2}-{tick1}"]["volume_percentage_change_24h"])
        elif f"{tick1}-{tick2}" in product_list:
            c1 =1/float(products_results[f"{tick1}-{tick2}"]["price"])
            c1_list.append(c1)
            cc1_list.append(products_results[f"{tick1}-{tick2}"]["price_percentage_change_24h"])
            v1_list.append(products_results[f"{tick1}-{tick2}"]["volume_24h"])
            vp1_list.append(products_results[f"{tick1}-{tick2}"]["volume_percentage_change_24h"])
        else:
            continue

        if f"{tick3}-{tick2}" in product_list:
            c2 = float(products_results[f"{tick3}-{tick2}"]["price"])
            c2_list.append(c2)
            cc2_list.append(products_results[f"{tick3}-{tick2}"]["price_percentage_change_24h"])
            v2_list.append(products_results[f"{tick3}-{tick2}"]["volume_24h"])
            vp2_list.append(products_results[f"{tick3}-{tick2}"]["volume_percentage_change_24h"])
        elif f"{tick2}-{tick3}" in product_list:
            c2 = 1/float(products_results[f"{tick2}-{tick3}"]["price"])
            c2_list.append(c2)
            cc2_list.append(products_results[f"{tick2}-{tick3}"]["price_percentage_change_24h"])
            v2_list.append(products_results[f"{tick2}-{tick3}"]["volume_24h"])
            vp2_list.append(products_results[f"{tick2}-{tick3}"]["volume_percentage_change_24h"])
        else:
            continue

        if f"{tick1}-{tick3}" in product_list:
            c3 = float(products_results[f"{tick1}-{tick3}"]["price"])
            c3_list.append(c3)
            cc3_list.append(products_results[f"{tick1}-{tick3}"]["price_percentage_change_24h"])
            v3_list.append(products_results[f"{tick1}-{tick3}"]["volume_24h"])
            vp3_list.append(products_results[f"{tick1}-{tick3}"]["volume_percentage_change_24h"])
        elif f"{tick3}-{tick1}" in product_list:
            c3 = 1/float(products_results[f"{tick3}-{tick1}"]["price"])
            c3_list.append(1/float(products_results[f"{tick3}-{tick1}"]["price"]))
            cc3_list.append(products_results[f"{tick3}-{tick1}"]["price_percentage_change_24h"])
            v3_list.append(products_results[f"{tick3}-{tick1}"]["volume_24h"])
            vp3_list.append(products_results[f"{tick3}-{tick1}"]["volume_percentage_change_24h"])
        else:
            continue
        tri_conversion_list.append(c1*c2*c3)
        
    tri_panda["tri_conversion"] = tri_conversion_list
    tri_panda["c1"] = c1_list
    tri_panda["cc1"] = cc1_list
    tri_panda["c2"] = c2_list
    tri_panda["cc2"] = cc2_list
    tri_panda["c3"] = c3_list
    tri_panda["cc3"] = cc3_list
    tri_panda["v1"] = v1_list
    tri_panda["vp1"] = vp1_list
    tri_panda["v2"] = v2_list
    tri_panda["vp2"] = vp2_list
    tri_panda["v3"] = v3_list
    tri_panda["vp3"] = vp3_list
        
    return tri_panda

def tri_update_panda_Gemini(tri_panda, products_results, product_list):
    tri_conversion_list = []
    c1_list = []
    cc1_list = []
    c2_list = []
    cc2_list = []
    c3_list = []
    cc3_list = []
    
    for i in range(len(tri_panda)):
        tick1, tick2, tick3 = tri_panda.iloc[i]["tri_path"].split('-')
        if f"{tick2}-{tick1}" in product_list:
            c1 = float(products_results[f"{tick2}-{tick1}"]["price"])
            c1_list.append(c1)
            cc1_list.append(products_results[f"{tick2}-{tick1}"]["percentChange24h"])

        elif f"{tick1}-{tick2}" in product_list:
            c1 =1/float(products_results[f"{tick1}-{tick2}"]["price"])
            c1_list.append(c1)
            cc1_list.append(products_results[f"{tick1}-{tick2}"]["percentChange24h"])

        else:
            continue

        if f"{tick3}-{tick2}" in product_list:
            c2 = float(products_results[f"{tick3}-{tick2}"]["price"])
            c2_list.append(c2)
            cc2_list.append(products_results[f"{tick3}-{tick2}"]["percentChange24h"])

        elif f"{tick2}-{tick3}" in product_list:
            c2 = 1/float(products_results[f"{tick2}-{tick3}"]["price"])
            c2_list.append(c2)
            cc2_list.append(products_results[f"{tick2}-{tick3}"]["percentChange24h"])

        else:
            continue

        if f"{tick1}-{tick3}" in product_list:
            c3 = float(products_results[f"{tick1}-{tick3}"]["price"])
            c3_list.append(c3)
            cc3_list.append(products_results[f"{tick1}-{tick3}"]["percentChange24h"])

        elif f"{tick3}-{tick1}" in product_list:
            c3 = 1/float(products_results[f"{tick3}-{tick1}"]["price"])
            c3_list.append(c3)
            cc3_list.append(products_results[f"{tick3}-{tick1}"]["percentChange24h"])

        else:
            continue
        tri_conversion_list.append(c1*c2*c3)
        
    tri_panda["tri_conversion"] = tri_conversion_list
    tri_panda["c1"] = c1_list
    tri_panda["cc1"] = cc1_list
    tri_panda["c2"] = c2_list
    tri_panda["cc2"] = cc2_list
    tri_panda["c3"] = c3_list
    tri_panda["cc3"] = cc3_list
        
    return tri_panda

def update_dict_Kraken(du, du_list, di):
    for i in du_list:
        symbol = du[i]['symbol']
        du[i]['price'] = di[symbol]["c"][0]
        du[i]['lot_volume'] = di[symbol]["c"][1]
        du[i]['vol_today'] = di[symbol]["v"][0]
        du[i]['vol_24h'] = di[symbol]["v"][1]
    
    return du
        
def update_dict_Gemini(du, du_list, di):
    for i in du_list:
        symbol = du[i]['symbol']
        du[i]['price'] = di[symbol]['price']
        du[i]['percentChange24h'] = di[symbol]['percentChange24h']
    
    return du
def tri_update_panda_Kraken(tri_panda, products_results, product_list):
    tri_conversion_list = []
    c1_list = []
    lot_volume_1_list = []
    vol_today_1_list = []
    vol_24h_1_list = []
    c2_list = []
    lot_volume_2_list = []
    vol_today_2_list = []
    vol_24h_2_list = []
    c3_list = []
    lot_volume_3_list = []
    vol_today_3_list = []
    vol_24h_3_list = []
    
    for i in range(len(tri_panda)):
        tick1, tick2, tick3 = tri_panda.iloc[i]["tri_path"].split('-')
        if f"{tick2}-{tick1}" in product_list:
            c1 = float(products_results[f"{tick2}-{tick1}"]["price"])
            c1_list.append(c1)
            lot_volume_1_list.append(products_results[f"{tick2}-{tick1}"]["lot_volume"])
            vol_today_1_list.append(products_results[f"{tick2}-{tick1}"]["vol_today"])
            vol_24h_1_list.append(products_results[f"{tick2}-{tick1}"]["vol_24h"])
        elif f"{tick1}-{tick2}" in product_list:
            if float(products_results[f"{tick1}-{tick2}"]["price"]) == 0:
                c1 = 0
            else:
                c1 =1/float(products_results[f"{tick1}-{tick2}"]["price"])
            c1_list.append(c1)
            lot_volume_1_list.append(products_results[f"{tick1}-{tick2}"]["lot_volume"])
            vol_today_1_list.append(products_results[f"{tick1}-{tick2}"]["vol_today"])
            vol_24h_1_list.append(products_results[f"{tick1}-{tick2}"]["vol_24h"])
        else:
            continue

        if f"{tick3}-{tick2}" in product_list:
            c2 = float(products_results[f"{tick3}-{tick2}"]["price"])
            c2_list.append(c2)
            lot_volume_2_list.append(products_results[f"{tick3}-{tick2}"]["lot_volume"])
            vol_today_2_list.append(products_results[f"{tick3}-{tick2}"]["vol_today"])
            vol_24h_2_list.append(products_results[f"{tick3}-{tick2}"]["vol_24h"])
        elif f"{tick2}-{tick3}" in product_list:
            if float(products_results[f"{tick2}-{tick3}"]["price"]) == 0:
                c2 = 0
            else:
                c2 = 1/float(products_results[f"{tick2}-{tick3}"]["price"])
            c2_list.append(c2)
            lot_volume_2_list.append(products_results[f"{tick2}-{tick3}"]["lot_volume"])
            vol_today_2_list.append(products_results[f"{tick2}-{tick3}"]["vol_today"])
            vol_24h_2_list.append(products_results[f"{tick2}-{tick3}"]["vol_24h"])
        else:
            continue

        if f"{tick1}-{tick3}" in product_list:
            c3 = float(products_results[f"{tick1}-{tick3}"]["price"])
            c3_list.append(c3)
            lot_volume_3_list.append(products_results[f"{tick1}-{tick3}"]["lot_volume"])
            vol_today_3_list.append(products_results[f"{tick1}-{tick3}"]["vol_today"])
            vol_24h_3_list.append(products_results[f"{tick1}-{tick3}"]["vol_24h"])
        elif f"{tick3}-{tick1}" in product_list:
            if float(products_results[f"{tick3}-{tick1}"]["price"]) == 0:
                c3 = 0
            else:
                c3 = 1/float(products_results[f"{tick3}-{tick1}"]["price"])
            c3_list.append(c3)
            lot_volume_3_list.append(products_results[f"{tick3}-{tick1}"]["lot_volume"])
            vol_today_3_list.append(products_results[f"{tick3}-{tick1}"]["vol_today"])
            vol_24h_3_list.append(products_results[f"{tick3}-{tick1}"]["vol_24h"])
        else:
            continue
        tri_conversion_list.append(c1*c2*c3)
        
    tri_panda["tri_conversion"] = tri_conversion_list
    tri_panda["c1"] = c1_list
    tri_panda["lot_volume_1"] = lot_volume_1_list
    tri_panda["vol_today_1"] = vol_today_1_list
    tri_panda["vol_24h_1"] = vol_24h_1_list
    tri_panda["c2"] = c2_list
    tri_panda["lot_volume_2"] = lot_volume_2_list
    tri_panda["vol_today_2"] = vol_today_2_list
    tri_panda["vol_24h_2"] = vol_24h_2_list
    tri_panda["c3"] = c3_list
    tri_panda["lot_volume_3"] = lot_volume_3_list
    tri_panda["vol_today_3"] = vol_today_3_list
    tri_panda["vol_24h_3"] = vol_24h_3_list
        
    return tri_panda

def unpack_tuples(tuples):
  mylist1 = list(tuples)

  new_list = []
  if len(mylist1) > 1:
    temp_list1 = []
    for i in mylist1:
      if isinstance(i, list) or type(i) is tuple:
        temp_1 = [*i,]
        if len(temp_1) > 1:
          temp_list2 = []
          for j in temp_1:
            if isinstance(j, list) or type(j) is tuple:
              temp_2 = [*j,]
              if len(temp_2) > 1:
                temp_list3 = []
                for k in temp_2:
                  if isinstance(k, list) or type(k) is tuple:
                    temp_3 = [*k,]
                    if len(temp_3) > 1:
                      temp_list4 = []
                      for l in temp_3:
                        if isinstance(l, list) or type(l) is tuple:
                          temp_4 = [*l,]
                          temp_list4.append(temp_4)
                        else:
                          temp_list4.append(l)
                      temp_list3.append(temp_list4)
                    else:
                      temp_list3.append(temp_3[0])
                  else:
                    temp_list3.append(k)
                temp_list2.append(temp_list3)
              else:
                temp_list2.append(temp_2[0])
            else:
              temp_list2.append(j)
          temp_list1.append(temp_list2)
        else:
          temp_list1.append(temp_1[0])
      else:
        temp_list1.append(i)
    new_list = temp_list1
  else:
    new_list = mylist1
  return new_list

def available_tickers_bipaths(product_list):
    global ku_tickers
    ku_tickers = []
    bi_paths = []
    for i in product_list:
        tick1, tick2 = i.split('-')
        if tick1 not in ku_tickers:
            ku_tickers.append(tick1)
        if tick2 not in ku_tickers:
            ku_tickers.append(tick2)

    for i in ku_tickers:
        for j in ku_tickers:
            if i == j:
                continue
            else: 
                bi_paths.append(f"{i}-{j}")
    
    return ku_tickers, bi_paths

def sub_trichecks_conversions(tri_checked_list):
    tri_conversion1 = []
    for tri_path in tri_checked_list:
        if tri_path:
            tick1, tick2, tick3 = tri_path.split('-')
            if Kucoin_Products[f"{tick2}-{tick1}"]["price"]:
                con1 = float(Kucoin_Products[f"{tick2}-{tick1}"]["price"])
                print(f"{tick2}-{tick1}: ",con1)

            elif Kucoin_Products[f"{tick1}-{tick2}"]["price"]:
                con1 = 1/float(Kucoin_Products[f"{tick1}-{tick2}"]["price"])
                print(f"{tick2}-{tick1}: ",con1)
            else:
                continue

            if Kucoin_Products[f"{tick3}-{tick2}"]["price"]:
                con2 = float(Kucoin_Products[f"{tick3}-{tick2}"]["price"])
                print(f"{tick3}-{tick2}: ",con2)

            elif Kucoin_Products[f"{tick2}-{tick3}"]["price"]:
                con2 = 1/float(Kucoin_Products[f"{tick2}-{tick3}"]["price"])
                print(f"{tick3}-{tick2}: ",con2)
            else:
                continue

            if Kucoin_Products[f"{tick1}-{tick3}"]["price"]:
                con3 = float(Kucoin_Products[f"{tick1}-{tick3}"]["price"])
                print(f"{tick1}-{tick3}: ",con3)
                            
            elif Kucoin_Products[f"{tick3}-{tick1}"]["price"]:
                con3 = 1/float(Kucoin_Products[f"{tick3}-{tick1}"]["price"])
                print(f"{tick1}-{tick3}: ",con3)
            else:
                continue

            tri_conversion1.append(con1*con2*con3)
                                
    return tri_conversion1

def sub_trichecks_(cur_tick):
    tri_checked1 = []
    for j in ku_tickers:
            for k in ku_tickers:
                if cur_tick == j or cur_tick == k or j == k:
                    continue
                else: 
                    tri_path = f"{cur_tick}-{j}-{k}"
                    
                    if tri_path not in tri_checked1:
                        tick1, tick2, tick3 = tri_path.split('-')
                        if f"{tick2}-{tick1}" in Kucoin_Prod_List:
                            if Kucoin_Products[f"{tick2}-{tick1}"]["price"]:
                                c1 = float(Kucoin_Products[f"{tick2}-{tick1}"]["price"])
                                print(f"{tick2}-{tick1}: ",c1)
                            else:
                                continue
                        elif f"{tick1}-{tick2}" in Kucoin_Prod_List:
                            if Kucoin_Products[f"{tick1}-{tick2}"]["price"]:
                                c1 = 1/float(Kucoin_Products[f"{tick1}-{tick2}"]["price"])
                                print(f"{tick2}-{tick1}: ",c1)
                            else:
                                continue
                        else:
                            continue

                        if f"{tick3}-{tick2}" in Kucoin_Prod_List:
                            if Kucoin_Products[f"{tick3}-{tick2}"]["price"]:
                                c2 = float(Kucoin_Products[f"{tick3}-{tick2}"]["price"])
                                print(f"{tick3}-{tick2}: ",c2)
                            else:
                                continue
                        elif f"{tick2}-{tick3}" in Kucoin_Prod_List:
                            if Kucoin_Products[f"{tick2}-{tick3}"]["price"]:
                                c2 = 1/float(Kucoin_Products[f"{tick2}-{tick3}"]["price"])
                                print(f"{tick3}-{tick2}: ",c2)
                            else:
                                continue
                        else:
                            continue

                        if f"{tick1}-{tick3}" in Kucoin_Prod_List:
                            if Kucoin_Products[f"{tick1}-{tick3}"]["price"]:
                                c3 = float(Kucoin_Products[f"{tick1}-{tick3}"]["price"])
                                print(f"{tick1}-{tick3}: ",c3)
                            else:
                                continue
                        elif f"{tick3}-{tick1}" in Kucoin_Prod_List:
                            if Kucoin_Products[f"{tick3}-{tick1}"]["price"]:
                                c3 = 1/float(Kucoin_Products[f"{tick3}-{tick1}"]["price"])
                                print(f"{tick1}-{tick3}: ",c3)
                            else:
                                continue
                        else:
                            continue
                        
                        if c1*c2*c3:    
                            if c1*c2*c3 < 1.02:
                                continue
                            else:
                                if ((f"{tick2}-{tick3}-{tick1}" in tri_checked1) or (f"{tick3}-{tick1}-{tick2}" in tri_checked1)):
                                    continue
                                else:
                                    tri_checked1.append(f"{tick1}-{tick2}-{tick3}")
                                    print(f"{tick1}-{tick2}-{tick3}")
    if tri_checked1:
#    if len(tri_checked1) > 0:
        return tri_checked1
    else:
       return

def task1(start_end):
#        tri_checked2 = []
        for i in ku_tickers[start_end[0]:start_end[1]]:
            sub_checked1 = sub_trichecks_(i)
            
#            for j in sub_checked1:
#                tri_checked2.append(j)
                
        return sub_checked1

def available_trichecks_(ku_tickers):
    if __name__ == '__main__':
        global result
        inc = len(ku_tickers)//16
        start_end = [[0, inc], [inc+1, inc*2], [(inc*2)+1, inc*3], [(inc*3)+1, inc*4], [(inc*4)+1, inc*5],
                    [(inc*5)+1, inc*6], [(inc*6)+1, inc*7], [(inc*7)+1, inc*8],[(inc*8)+1, inc*9], [(inc*9)+1, inc*10],
                    [(inc*10)+1, inc*11], [(inc*11)+1, inc*12], [(inc*12)+1, inc*13], [(inc*13)+1, inc*14], 
                    [(inc*14)+1, inc*15], [(inc*15)+1, len(ku_tickers)]]
        
        p = Pool()
        result = p.imap(task1, start_end)

        p.close()
        p.join()

        print(result)

        tri_checked = unpack_tuples(result)

        print(tri_checked)


        tri_conversions = sub_trichecks_conversions(tri_checked)

        print(tri_conversions)

        tri_panda_Kucoin = pd.DataFrame(data = {'tri_paths': tri_checked, 'tri_conversions': tri_conversions})

        
        return tri_panda_Kucoin
    
# GUI Stuffs ------------------------------------------------------------------------------------------

# Tricheck_Coinbase Tab:

def clear_data():
    tv1.delete(*tv1.get_children())
    return None

def Load_data(df):
    
    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
        
#        tv1.b=tk.Button(ta
# b3,text="update",command=tab3.ButtonPushed)

    return None

def Tricheck_Coinbase_CallBack():
    global tri_results_CB
    global tri_on_CB
    global filtered_subset
    global CB_Prod_List
    global CB_Products

    if tri_on_CB == False:
        tri_on_CB = True
        CB_Products, CB_Prod_List =  check_all_CB()
        tickers, bi_paths, tri_paths = available_tickers_paths(CB_Prod_List)
        tri_checked, tri_conversion = tri_check_CB(tri_paths, CB_Prod_List, CB_Products)
        data = []
        for i in range(len(tri_checked)):
            data.append([tri_checked[i], tri_conversion[i]])
        tri_results_CB = pd.DataFrame(data, columns=['tri_path', 'tri_conversion'])

    if tri_on_CB == True: 
        CB_Products, CB_Prod_List = check_all_CB()
        tri_results_CB = tri_update_panda_CB(tri_results_CB, CB_Products, CB_Prod_List)

    filtered_subset = tri_results_CB
    label1.config( text = "" )
    label2.config( text = "" )
    label3.config( text = "" )

    return Load_data(filtered_subset)

def Tricheck_Coinbase_CallBack_test():
    global tri_results_CB
    global filtered_subset
    tri_results_CB = pd.DataFrame(columns=['tri_path','tri_conversion','c1','cc1','c2','cc2','c3','cc3','v1',
                                           'vp1','v2','vp2','v3','vp3'])
    tri_results_CB['tri_path'] = ["BTC-USDC-UNI", "USDC-UNI-BTC", "UNI-BTC-USDC", "EUR-USDC-TILT", "USDC-TILT-EUR", "TILT-EUR-USDC"]
    tri_results_CB['tri_conversion'] = [3.6,3.6,3.6,1.68,1.68,1.68]
    tri_results_CB['c1'] = [2,3,0.6,2,0.7,1.2]
    tri_results_CB['cc1'] = [1,1,1,1,1,1]
    tri_results_CB['c2'] = [3,0.6,2,0.7,1.2,2]
    tri_results_CB['cc2'] = [1,1,1,1,1,1]
    tri_results_CB['c3'] = [0.6,2,3,1.2,2,0.7]
    tri_results_CB['cc3'] = [1,1,1,1,1,1]
    tri_results_CB['v1'] = [1,1,0,1,1,1]
    tri_results_CB['vp1'] = [1,1,1,1,1,1]
    tri_results_CB['v2'] = [1,1,1,1,1,1]
    tri_results_CB['vp2'] = [1,1,1,1,1,1]
    tri_results_CB['v3'] = [1,1,1,1,1,1]
    tri_results_CB['vp3'] = [1,1,1,1,1,1]

    filtered_subset = tri_results_CB
    label1.config( text = "" )
    label2.config( text = "" )
    label3.config( text = "" )
    return Load_data(filtered_subset)

def clicked_CB(event):
    global CB_Prod_List

    selected = tv1.focus()
    (tri_path, tri_conversion, c1, cc1, c2, cc2, c3, cc3, v1, vp1, v2, vp2, v3, vp3) = tv1.item(selected, 'values') 

    tick1, tick2, tick3 = tri_path.split('-')
    if f"{tick2}-{tick1}" in CB_Prod_List:
        win1 = f"{tick2}-{tick1}"
    if f"{tick1}-{tick2}" in CB_Prod_List:
        win1 = f"{tick1}-{tick2}"
    

    if f"{tick3}-{tick2}" in CB_Prod_List:
        win2 = f"{tick3}-{tick2}"
    elif f"{tick2}-{tick3}" in CB_Prod_List:
        win2 = f"{tick2}-{tick3}"

    if f"{tick1}-{tick3}" in CB_Prod_List:
        win3 = f"{tick1}-{tick3}"
    elif f"{tick3}-{tick1}" in CB_Prod_List:
        win3 = f"{tick3}-{tick1}"

    url1 = f"https://www.coinbase.com/advanced-trade/{win1}"
    webbrowser.open(url1, new=1, autoraise=True)

    url2 = f"https://www.coinbase.com/advanced-trade/{win2}"
    webbrowser.open(url2, new=1, autoraise=True)

    url3 = f"https://www.coinbase.com/advanced-trade/{win3}"
    webbrowser.open(url3, new=1, autoraise=True)


root = tk.Tk()
root.geometry("1000x1000") # set the root dimensions
root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
#root.resizable(0, 0) # makes the root window fixed in size.
root.title("Cryptotrage 9000")
tabControl = ttk.Notebook(root)
  
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)
tab6 = ttk.Frame(tabControl)
  
tabControl.add(tab1, text ='Home')
tabControl.add(tab2, text ='Crosscheck')
tabControl.add(tab3, text ='Tricheck_Coinbase')
tabControl.add(tab4, text ='Tricheck_Gemini')
tabControl.add(tab5, text ='Tricheck_Kraken')
tabControl.add(tab6, text ='Tricheck_Kucoin')
tabControl.pack(expand = 1, fill ="both")
  
# Frame for TreeView
frame1 = tk.LabelFrame(tab3, text="DataFrame")
frame1.place(height=500, width=1000)

## Treeview Widget
tv1 = ttk.Treeview(frame1)
tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).
tv1.bind("<Double-1>", clicked_CB)

treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

# Create TriCheck button
B = tk.Button(tab3, text ="TriCheck", command = Tricheck_Coinbase_CallBack)
B.place(x=25, y=550)

# datatype of menu text
clicked = tk.StringVar(tab3)
  
# initial menu text
clicked.set( "v1" )

# Change the label text for filter to be added
filter_2_print_list_cb = []
def show1_cb(filter_2_print):
    global filter_list_CB
    global comparison_list_CB
#    filter_2_print = f"{column_name}, {condition}, {value}, {comparison}, {conatins}"
    filter_2_print_list_cb.append(filter_2_print, comparison_list_CB)
#    for i in filter_2_print_list_cb:
#    label1.config( text = filter_2_print )
# Change the label text for final filter set
def show2_cb(filtered_subset):
    #label_2 = clicked.get()
    label2.config( text = f"{filtered_subset}" )
#    filter_set_2_print = f"{filtered_subset}"

# Variable to keep track of the option
# selected in OptionMenu
column_name_CB = tk.StringVar(tab3)
  
# Set the default value of the variable
column_name_CB.set("tri_path")

# Create Label for sorting status
label_column_cb= tk.Label( tab3 , text = "Column:" )
label_column_cb.place(x=0, y=580)

# Variable to keep track of the option
# selected in OptionMenu
condition_CB = tk.StringVar(tab3)
  
# Set the default value of the variable
condition_CB.set(".str.contains()")

# Create Label for sorting status
label_condition_cb= tk.Label( tab3 , text = "Condition:" )
label_condition_cb.place(x=125, y=580)

# Create Label for sorting status
label_condition_cb= tk.Label( tab3 , text = "Contains:" )
label_condition_cb.place(x=250, y=580)

# Create Label for sorting status
label_condition_cb= tk.Label( tab3 , text = "Value:" )
label_condition_cb.place(x=400, y=580)

# Variable to keep track of the option
# selected in OptionMenu
comparison_CB = tk.StringVar(tab3)
  
# Set the default value of the variable
comparison_CB.set("")

# Create Label for sorting status
label_comparison_cb= tk.Label( tab3 , text = "&|:" )
label_comparison_cb.place(x=530, y=580)

# selected in OptionMenu
sort_by_CB = tk.StringVar(tab3)

# Set the default value of the variable
sort_by_CB.set("tri_path")

# selected in OptionMenu
ascend_CB = tk.StringVar(tab3)

# Set the default value of the variable
ascend_CB.set("Ascending")

 # Dropdown menu options
column_names = ["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", "cc3", "v1", "vp1", "v2", 
                "vp2", "v3", "vp3"]

conditions = [".str.contains()", ".isna()", "==", ">", ">=", "<", "<="]

comparisons = ["", " & ", " | "]

sort_bys_CB = ["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", "cc3", "v1", "vp1", "v2", 
                "vp2", "v3", "vp3"]

ascends_CB = ["Ascending", "Decending"]

ascends_dict_CB = {"Ascending" : " True ", "Decending" : " False "}

filter_list_CB = []
comparison_list_CB = []

def add_filter():
    global filter_list_CB
    global comparison_list_CB
    global comparison_CB
    global value_CB
    global condition_CB
    global column_name_CB
    global tri_results_CB_filter
    global contains_CB

    tri_results_CB_filter = "filtered_subset"

    if condition_CB.get() == ".str.contains()":
        tri_results_CB_filter = f"filtered_subset['{column_name_CB.get()}'].str.contains('{contains_CB.get()}') == {value_CB.get()}"

    elif condition_CB.get() == ".isna()":
        tri_results_CB_filter = f"filtered_subset['{column_name_CB.get()}'].isna() == {value_CB.get()}"

    elif condition_CB.get() == "==":
        tri_results_CB_filter = f"filtered_subset['{column_name_CB.get()}'] == {value_CB.get()}"

    elif condition_CB.get() == ">":
        tri_results_CB_filter = f"filtered_subset['{column_name_CB.get()}'] > {value_CB.get()}"

    elif condition_CB.get() == ">=":
        tri_results_CB_filter = f"filtered_subset['{column_name_CB.get()}'] >= {value_CB.get()}"

    elif condition_CB.get() == "<":
        tri_results_CB_filter = f"filtered_subset['{column_name_CB.get()}'] < {value_CB.get()}"

    elif condition_CB.get() == "<=":
        tri_results_CB_filter = f"filtered_subset['{column_name_CB.get()}'] <= {value_CB.get()}"

    else:
        print(condition_CB.get())

    filter_list_CB.append(tri_results_CB_filter)
    comparison_list_CB.append(comparison_CB.get())

    for i in range(len(filter_list_CB)):
        if i == 0:
            combo_2_print = f"({filter_list_CB[i]}){comparison_list_CB[i]}"
        else:
            combo_2_print = combo_2_print + f"({filter_list_CB[i]}){comparison_list_CB[i]}"

    label1.config( text = combo_2_print )

    return print(tri_results_CB_filter)
    

def create_filter_set():
    global comparison_list_CB
    global filter_list_CB
    global filtered_subset
    global filtered_subtext
    
    label1.config( text = "" )
    label2.config( text = "" )
    label3.config( text = "" )

    k = len(filter_list_CB)

    if len(tri_results_CB) > 0:
        filtered_subset = tri_results_CB
        filtered_subset.reset_index()

        if k == 1:
            filtered_subtext = f"filtered_subset[{filter_list_CB[0]}]"
            print(filtered_subtext)
            print(column_name_CB.get())
            print(condition_CB.get())
            print(comparison_CB.get())
            print(value_CB.get())
            print(filtered_subset)
            exec(f"global filtered_subset; filtered_subset = {filtered_subtext}")
            print(filtered_subset)

        if k > 1:
            combo = ""
            for i in range(k):
                if i < k-1:
                    combo = combo + f"({filter_list_CB[i]}){comparison_list_CB[i]}"
                else:
                    combo = combo + f"({filter_list_CB[i]}){comparison_list_CB[i]}"
                    filtered_subtext = f"filtered_subset[{combo}]"
                    print(filtered_subtext)
                    print(column_name_CB.get())
                    print(condition_CB.get())
                    print(comparison_CB.get())
                    print(value_CB.get())
                    print(filtered_subset)
                    exec(f"global filtered_subset; filtered_subset = {filtered_subtext}")
                    print(filtered_subset)
    
    else:
        filtered_subset = pd.DataFrame(columns=["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", 
                "cc3", "v1", "vp1", "v2", "vp2", "v3", "vp3"])

    label2.config( text = f"{filtered_subtext}" )
    return Load_data(filtered_subset), print("finalized")

def sort_checked_CB():
    global filtered_subset
    global sort_check_CB
    global sort_by_CB
    global ascend_CB

    exec(f"global sorted_subset_CB; sorted_subset_CB = filtered_subset.sort_values(by= '{sort_by_CB.get()}', ascending={ascends_dict_CB[ascend_CB.get()]})")
    label3.config( text = f"{ascend_CB.get()}" )
    return Load_data(sorted_subset_CB), print("sorted")

def clear_filter_set():
    global filter_list_CB
    global comparison_list_CB

    filter_list_CB = []
    comparison_list_CB = []

    label1.config( text = "" )

    return None

def Load_CB_Products():
    global CB_Products
    global CB_Prod_List
    file1 = open("CB_Products",'rb')
    CB_Products = pickle.load(file1)
    file2 = open("CB_Products",'rb')
    CB_Prod_List = pickle.load(file2)

def save_current_df_CB():
    global filtered_subset
    global CB_Products
    global CB_Prod_List
    
    with open("CB_Products","wb") as f:
        pickle.dump(CB_Products, f)

    with open("CB_Prod_List","wb") as f:
        pickle.dump(CB_Prod_List, f)
    filtered_subset.to_csv("tri_results_CB.csv")
    return

# Create Dropdown menu
drop1 = tk.OptionMenu( tab3 , column_name_CB , *column_names )
drop1.place(x=0, y=600)
drop1.config(width = 12)

# Create Dropdown menu
drop2 = tk.OptionMenu( tab3 , condition_CB , *conditions )
drop2.place(x=125, y=600)
drop2.config(width = 12)

# Create Dropdown menu
drop3 = tk.OptionMenu( tab3 , comparison_CB , *comparisons )
drop3.place(x=530, y=600)
drop3.config(width = 3)

# Create Dropdown menu
drop_sort = tk.OptionMenu( tab3 , sort_by_CB , *sort_bys_CB )
drop_sort.place(x=650, y=600)
drop_sort.config(width = 12)

# Create Dropdown menu
drop_ascend = tk.OptionMenu( tab3 , ascend_CB , *ascends_CB )
drop_ascend.place(x=775, y=600)
drop_ascend.config(width = 12)

# Create Label for sorting status
label3= tk.Label( tab3 , text = " " )
label3.place(x=700, y=575)

# Create Label for sorting status
label_sortby_cb = tk.Label( tab3 , text = "Sort by:" )
label_sortby_cb.place(x=650, y=575)

# Create Entry Box1
value_CB = tk.StringVar(tab3)
value_CB_entry = tk.Entry(tab3, textvariable=value_CB).place(x=400, y=600)

# Create Entry Box2
contains_CB = tk.StringVar(tab3)
contains_CB_entry = tk.Entry(tab3, textvariable=contains_CB).place(x=250, y=600)

# Create button, it will change label text
button1 = tk.Button( tab3 , text = "Add Filter" , command = add_filter).place(x=100, y=550)

# Create button, it will change label text
button2 = tk.Button( tab3 , text = "Finalize Filter Set" , command = create_filter_set).place(x=200, y=550)

# Create button, it will change label text
button3 = tk.Button( tab3 , text = "Clear Filter Set" , command = clear_filter_set).place(x=325, y=550)

# Create Label
label1= tk.Label( tab3 , text = " " )
label1.place(x=100, y=525)

# Create Label
label2 = tk.Label( tab3 , text = " " )
label2.place(x=100, y=500)

# Create Label
label_filter_CB= tk.Label( tab3 , text = "Filter Set:" )
label_filter_CB.place(x=25, y=500)

# Create Label
label_filter_CB= tk.Label( tab3 , text = "Filter(s):" )
label_filter_CB.place(x=25, y=525)

# Create button
check1_CB = tk.Button(tab3, text ="Sort", command = sort_checked_CB)
check1_CB.place(x=650, y=550)

# Create button
check1_CB = tk.Button(tab3, text = "Save Current DF", command = save_current_df_CB)
check1_CB.place(x=25, y=700)

def openFile():
    global tri_on_CB
    global tri_results_CB
    global filtered_subset

    tri_on_CB = True
    filepath = filedialog.askopenfilename(initialdir= os.getcwd(),
                                          title="Load CSV",
                                          filetypes= (("CSV Files","*.csv"),))
    
    tri_results_CB = pd.read_csv(filepath)
    tri_results_CB = tri_results_CB.drop('Unnamed: 0', axis=1)
    filtered_subset = tri_results_CB
    Load_data(filtered_subset)

# Create button, it will change label text
button4 = tk.Button( tab3 , text = "Load CSV" , command = openFile).place(x=125, y=700)

# Create button, to load pickled results from previous session
button5 = tk.Button( tab3 , text = "Load_CB_Products" , command = Load_CB_Products).place(x=125, y=725)

########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################

# Home Tab


label_Home_Top = tk.Label( tab1 , text = "Welcome to Cryptotrage 9000. \nThis application is to help identify arbitrage opportunities within Coinbase, Gemini, Kraken, and Kucoin. \n Enjoy!" )
label_Home_Top.place(x=0, y=0)

image = Image.open("cryptocurrency-bitcoin-iStock-1434149985.jpg")
photo = ImageTk.PhotoImage(image)

# Label widget to display the image
label = tk.Label(tab1, image=photo)
label.place(x=0, y=50)
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################

# Crosscheck Tab:

def clear_data_Ccheck():
    tv_Ccheck.delete(*tv_Ccheck.get_children())
    return None

def Load_data_Ccheck(df):
    
    clear_data_Ccheck()
    tv_Ccheck["column"] = list(df.columns)
    tv_Ccheck["show"] = "headings"
    for column in tv_Ccheck["columns"]:
        tv_Ccheck.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv_Ccheck.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert

    return None

def Crosscheck_CallBack():
    global tri_results_Ccheck
    global tri_on_Ccheck
    global filtered_subset_Ccheck
    global CB_Products
    global CB_Prod_List
    global Kucoin_Prod_List
    global Kucoin_Products
    global Kraken_Prod_List
    global Kraken_Products
    global Kraken_Prod_List2
    global Kraken_Products2
    global Gemini_Prod_List
    global Gemini_Products
    global Gemini_Prod_List2
    global Gemini_Products2
    global Cross_results

    if tri_on_Ccheck == False:
        tri_on_Ccheck = True
        
        CB_Products, CB_Prod_List =  check_all_CB()
        Gemini_Products, Gemini_Prod_List = check_all_Gemini()
        Kucoin_Products, Kucoin_Prod_List = check_all_Kucoin()
        Kraken_Products, Kraken_Prod_List, In_The_Kraken = check_all_Kraken()

        Gemini_Products2, Gemini_Prod_List2 = formator_Gemini(Gemini_Products, Gemini_Prod_List)
        Kraken_Products2, Kraken_Prod_List2 = formator_Kraken(Kraken_Products, Kraken_Prod_List)

        data_pd = stuff_panda_cross(quote_ticker = quote_ticker.get(), num_markets = 4, tickers_1 = CB_Prod_List, results_1 = CB_Products, tickers_2 = Gemini_Prod_List2, results_2 = Gemini_Products2, tickers_3 = Kraken_Prod_List2, results_3 = Kraken_Products2, tickers_4 = Kucoin_Prod_List, results_4 = Kucoin_Products)

        Cross_results = cross_check(panda = data_pd, num_markets = 4)

    else: 
        CB_Products, CB_Prod_List =  check_all_CB()
        Gemini_Products, Gemini_Prod_List = check_all_Gemini()
        Kucoin_Products, Kucoin_Prod_List = check_all_Kucoin()
        Kraken_Products, Kraken_Prod_List, In_The_Kraken = check_all_Kraken()

        Gemini_Products2 = update_dict_Gemini(Gemini_Products2, Gemini_Prod_List2, Gemini_Products)
        Kraken_Products2 = update_dict_Kraken(Kraken_Products2, Kraken_Prod_List2, Kraken_Products)

        data_pd = stuff_panda_cross(quote_ticker = quote_ticker.get(), num_markets = 4, tickers_1 = CB_Prod_List, results_1 = CB_Products, tickers_2 = Gemini_Prod_List2, results_2 = Gemini_Products2, tickers_3 = Kraken_Prod_List2, results_3 = Kraken_Products2, tickers_4 = Kucoin_Prod_List, results_4 = Kucoin_Products)

        Cross_results = cross_check(panda = data_pd, num_markets = 4)
    
    filtered_subset_Ccheck = Cross_results
    label1_Ccheck.config( text = "" )
    label2_Ccheck.config( text = "" )
    label3_Ccheck.config( text = "" )

    return Load_data_Ccheck(filtered_subset_Ccheck)

def Crosscheck_CallBack_test():
    global tri_results_Ccheck
    global filtered_subset_Ccheck
    tri_results_Ccheck = pd.DataFrame(columns=['tri_path','tri_conversion','c1','cc1','c2','cc2','c3','cc3','v1',
                                           'vp1','v2','vp2','v3','vp3'])
    tri_results_Ccheck['tri_path'] = ["BTC-USDC-UNI", "USDC-UNI-BTC", "UNI-BTC-USDC", "EUR-USDC-TILT", "USDC-TILT-EUR", "TILT-EUR-USDC"]
    tri_results_Ccheck['tri_conversion'] = [3.6,3.6,3.6,1.68,1.68,1.68]
    tri_results_Ccheck['c1'] = [2,3,0.6,2,0.7,1.2]
    tri_results_Ccheck['cc1'] = [1,1,1,1,1,1]
    tri_results_Ccheck['c2'] = [3,0.6,2,0.7,1.2,2]
    tri_results_Ccheck['cc2'] = [1,1,1,1,1,1]
    tri_results_Ccheck['c3'] = [0.6,2,3,1.2,2,0.7]
    tri_results_Ccheck['cc3'] = [1,1,1,1,1,1]
    tri_results_Ccheck['v1'] = [1,1,0,1,1,1]
    tri_results_Ccheck['vp1'] = [1,1,1,1,1,1]
    tri_results_Ccheck['v2'] = [1,1,1,1,1,1]
    tri_results_Ccheck['vp2'] = [1,1,1,1,1,1]
    tri_results_Ccheck['v3'] = [1,1,1,1,1,1]
    tri_results_Ccheck['vp3'] = [1,1,1,1,1,1]

    filtered_subset_Ccheck = tri_results_Ccheck
    label1_Ccheck.config( text = "" )
    label2_Ccheck.config( text = "" )
    label3_Ccheck.config( text = "" )
    return Load_data_Ccheck(filtered_subset_Ccheck)

def clicked_Ccheck(event):
    global CB_Prod_List
    global Gemini_Prod_List
    global Kraken_Prod_List2
    global Kucoin_Prod_List
    global quote_ticker

    selected = tv_Ccheck.focus()
    (ticker,gap_1,gap_2,gap_3,gap_4,gaps_ranked) = tv_Ccheck.item(selected, 'values') 

    if f"{ticker}-{quote_ticker.get()}" in CB_Prod_List:
        win1 = f"{ticker}-{quote_ticker.get()}"
#    elif f"{quote_ticker.get()}-{ticker}" in CB_Prod_List:
    else:
        win1 = f"{quote_ticker.get()}-{ticker}"

    if f"{ticker}{quote_ticker.get()}" in Gemini_Prod_List:
        win2 = f"{ticker}{quote_ticker.get()}"
#    elif f"{quote_ticker.get()}{ticker}" in Gemini_Prod_List:
    else:
        win2 = f"{quote_ticker.get()}{ticker}"

    if f"{ticker}-{quote_ticker.get()}" in Kraken_Prod_List2:
        win3 = f"{ticker}-{quote_ticker.get()}"
#    elif f"{quote_ticker.get()}-{ticker}" in Kraken_Prod_List2:
    else:
        win3 = f"{quote_ticker.get()}-{ticker}"

    if f"{ticker}-{quote_ticker.get()}" in Kucoin_Prod_List:
        win4 = f"{ticker}-{quote_ticker.get()}"
#    elif f"{quote_ticker.get()}-{ticker}" in Kucoin_Prod_List:
    else:
        win4 = f"{quote_ticker.get()}-{ticker}"

    url1 = f"https://www.coinbase.com/advanced-trade/{win1}"
    webbrowser.open(url1, new=1, autoraise=True)

    url2 = f"https://exchange.gemini.com/trade/{win2}"
    webbrowser.open(url2, new=1, autoraise=True)

    url3 = f"https://pro.kraken.com/app/trade/{win3}"
    webbrowser.open(url3, new=1, autoraise=True)

    url4 = f"https://www.kucoin.com/trade/{win4}"
    webbrowser.open(url4, new=1, autoraise=True)

    
frame_Ccheck = tk.LabelFrame(tab2, text="DataFrame")
frame_Ccheck.place(height=500, width=1000)

## Treeview Widget
tv_Ccheck = ttk.Treeview(frame_Ccheck)
tv_Ccheck.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).
tv_Ccheck.bind("<Double-1>", clicked_Ccheck)

treescrolly_Ccheck = tk.Scrollbar(frame_Ccheck, orient="vertical", command=tv_Ccheck.yview) # command means update the yaxis view of the widget
treescrollx_Ccheck = tk.Scrollbar(frame_Ccheck, orient="horizontal", command=tv_Ccheck.xview) # command means update the xaxis view of the widget
tv_Ccheck.configure(xscrollcommand=treescrollx_Ccheck.set, yscrollcommand=treescrolly_Ccheck.set) # assign the scrollbars to the Treeview Widget
treescrollx_Ccheck.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly_Ccheck.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

# Create TriCheck button
B_Ccheck = tk.Button(tab2, text ="Crosscheck", command = Crosscheck_CallBack)
B_Ccheck.place(x=25, y=550)

# datatype of menu text
clicked0_Ccheck = tk.StringVar(tab2)
  
# initial menu text
clicked0_Ccheck.set( "v1" )

# Change the label text for filter to be added
filter_2_print_list_Ccheck = []
def show1_Ccheck(filter_2_print):
    global filter_list_Ccheck
    global comparison_list_Ccheck
    filter_2_print_list_Ccheck.append(filter_2_print, comparison_list_Ccheck)

# Change the label text for final filter set
def show2_Ccheck(filtered_subset):
    #label_2 = clicked.get()
    label2_Ccheck.config( text = f"{filtered_subset}" )
#    filter_set_2_print = f"{filtered_subset}"

# Variable to keep track of the option
# selected in OptionMenu
column_name_Ccheck = tk.StringVar(tab2)
  
# Set the default value of the variable
column_name_Ccheck.set("tri_path")

# Create Label for sorting status
label_column_Ccheck= tk.Label( tab2 , text = "Column:" )
label_column_Ccheck.place(x=0, y=580)

# Variable to keep track of the option
# selected in OptionMenu
condition_Ccheck = tk.StringVar(tab2)
  
# Set the default value of the variable
condition_Ccheck.set(".str.contains()")

# Create Label for sorting status
label_condition_Ccheck= tk.Label( tab2 , text = "Condition:" )
label_condition_Ccheck.place(x=125, y=580)

# Create Label for sorting status
label_condition_Ccheck= tk.Label( tab2 , text = "Contains:" )
label_condition_Ccheck.place(x=250, y=580)

# Create Label for sorting status
label_condition_Ccheck= tk.Label( tab2 , text = "Value:" )
label_condition_Ccheck.place(x=400, y=580)

# Variable to keep track of the option
# selected in OptionMenu
comparison_Ccheck = tk.StringVar(tab2)
  
# Set the default value of the variable
comparison_Ccheck.set("")

# Create Label for sorting status
label_comparison_Ccheck= tk.Label( tab2 , text = "&|:" )
label_comparison_Ccheck.place(x=530, y=580)

# selected in OptionMenu
sort_by_Ccheck = tk.StringVar(tab2)

# Set the default value of the variable
sort_by_Ccheck.set("tri_path")

# selected in OptionMenu
ascend_Ccheck = tk.StringVar(tab2)

# Set the default value of the variable
ascend_Ccheck.set("Ascending")

 # Dropdown menu options
column_names_Ccheck = ["ticker", "gap_1", "gap_2", "gap_3", "gap_4", "gap_ranked"]

conditions_Ccheck = [".str.contains()", ".isna()", "==", ">", ">=", "<", "<="]

comparisons_Ccheck = ["", " & ", " | "]

sort_bys_Ccheck = ["ticker", "gap_1", "gap_2", "gap_3", "gap_4", "gap_ranked"]

ascends_Ccheck = ["Ascending", "Decending"]

ascends_dict_Ccheck = {"Ascending" : " True ", "Decending" : " False "}

filter_list_Ccheck = []
comparison_list_Ccheck = []

def add_filter_Ccheck():
    global filter_list_Ccheck
    global comparison_list_Ccheck
    global comparison_Ccheck
    global value_Ccheck
    global condition_Ccheck
    global column_name_Ccheck
    global tri_results_Ccheck_filter
    global contains_Ccheck

    tri_results_Ccheck_filter = "filtered_subset_Ccheck"

    if condition_Ccheck.get() == ".str.contains()":
        tri_results_Ccheck_filter = f"filtered_subset_Ccheck['{column_name_Ccheck.get()}'].str.contains('{contains_Ccheck.get()}') == {value_Ccheck.get()}"

    elif condition_Ccheck.get() == ".isna()":
        tri_results_Ccheck_filter = f"filtered_subset_Ccheck['{column_name_Ccheck.get()}'].isna() == {value_Ccheck.get()}"

    elif condition_Ccheck.get() == "==":
        tri_results_Ccheck_filter = f"filtered_subset_Ccheck['{column_name_Ccheck.get()}'] == {value_Ccheck.get()}"

    elif condition_Ccheck.get() == ">":
        tri_results_Ccheck_filter = f"filtered_subset_Ccheck['{column_name_Ccheck.get()}'] > {value_Ccheck.get()}"

    elif condition_Ccheck.get() == ">=":
        tri_results_Ccheck_filter = f"filtered_subset_Ccheck['{column_name_Ccheck.get()}'] >= {value_Ccheck.get()}"

    elif condition_Ccheck.get() == "<":
        tri_results_Ccheck_filter = f"filtered_subset_Ccheck['{column_name_Ccheck.get()}'] < {value_Ccheck.get()}"

    elif condition_Ccheck.get() == "<=":
        tri_results_Ccheck_filter = f"filtered_subset_Ccheck['{column_name_Ccheck.get()}'] <= {value_Ccheck.get()}"

    else:
        print(condition_Ccheck.get())

    filter_list_Ccheck.append(tri_results_Ccheck_filter)
    comparison_list_Ccheck.append(comparison_Ccheck.get())

    for i in range(len(filter_list_Ccheck)):
        if i == 0:
            combo_2_print = f"({filter_list_Ccheck[i]}){comparison_list_Ccheck[i]}"
        else:
            combo_2_print = combo_2_print + f"({filter_list_Ccheck[i]}){comparison_list_Ccheck[i]}"

    label1_Ccheck.config( text = combo_2_print )

    return print(tri_results_Ccheck_filter)
    

def create_filter_set_Ccheck():
    global comparison_list_Ccheck
    global filter_list_Ccheck
    global filtered_subset_Ccheck
    global filtered_subtext_Ccheck
    
    label1_Ccheck.config( text = "" )
    label2_Ccheck.config( text = "" )
    label3_Ccheck.config( text = "" )

    k = len(filter_list_Ccheck)

    if len(tri_results_Ccheck) > 0:
        filtered_subset_Ccheck = tri_results_Ccheck
        filtered_subset_Ccheck.reset_index()

        if k == 1:
            filtered_subtext_Ccheck = f"filtered_subset_Ccheck[{filter_list_Ccheck[0]}]"
            print(filtered_subtext_Ccheck)
            print(column_name_Ccheck.get())
            print(condition_Ccheck.get())
            print(comparison_Ccheck.get())
            print(value_Ccheck.get())
            print(filtered_subset_Ccheck)
            exec(f"global filtered_subset_Ccheck; filtered_subset_Ccheck = {filtered_subtext_Ccheck}")
            print(filtered_subset_Ccheck)

        if k > 1:
            combo = ""
            for i in range(k):
                if i < k-1:
                    combo = combo + f"({filter_list_Ccheck[i]}){comparison_list_Ccheck[i]}"
                else:
                    combo = combo + f"({filter_list_Ccheck[i]}){comparison_list_Ccheck[i]}"
                    filtered_subtext_Ccheck = f"filtered_subset_Ccheck[{combo}]"
                    print(filtered_subtext_Ccheck)
                    print(column_name_Ccheck.get())
                    print(condition_Ccheck.get())
                    print(comparison_Ccheck.get())
                    print(value_Ccheck.get())
                    print(filtered_subset_Ccheck)
                    exec(f"global filtered_subset_Ccheck; filtered_subset_Ccheck = {filtered_subtext_Ccheck}")
                    print(filtered_subset_Ccheck)
    
    else:
        filtered_subset_Ccheck = pd.DataFrame(columns=["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", 
                "cc3", "v1", "vp1", "v2", "vp2", "v3", "vp3"])

    label2_Ccheck.config( text = f"{filtered_subtext_Ccheck}" )
    return Load_data_Ccheck(filtered_subset_Ccheck), print("finalized")
#    return filtered_subset

def sort_checked_Ccheck():
    global filtered_subset_Ccheck
    global sort_check_Ccheck
    global sort_by_Ccheck
    global ascend_Ccheck

    exec(f"global sorted_subset_Ccheck; sorted_subset_Ccheck = filtered_subset_Ccheck.sort_values(by= '{sort_by_Ccheck.get()}', ascending={ascends_dict_Ccheck[ascend_Ccheck.get()]})")
    label3_Ccheck.config( text = f"{ascend_Ccheck.get()}" )
    return Load_data_Ccheck(sorted_subset_Ccheck), print("sorted")

def clear_filter_set_Ccheck():
    global filter_list_Ccheck
    global comparison_list_Ccheck

    filter_list_Ccheck = []
    comparison_list_Ccheck = []
    label1_Ccheck.config( text = "" )

    return None

def Load_Ccheck_Products():
    global CB_Products
    global CB_Prod_List
    global Kucoin_Prod_List
    global Kucoin_Products
    global Kraken_Prod_List
    global Kraken_Products
    global Kraken_Prod_List2
    global Kraken_Products2
    global Gemini_Prod_List
    global Gemini_Products
    global Gemini_Prod_List2
    global Gemini_Products2
    global filtered_subset_Ccheck

    file1 = open("CB_Products",'rb')
    CB_Products = pickle.load(file1)
    file2 = open("CB_Prod_List",'rb')
    CB_Prod_List = pickle.load(file2)
    file3 = open("Kucoin_Prod_List",'rb')
    Kucoin_Prod_List = pickle.load(file3)
    file4 = open("Kucoin_Products",'rb')
    Kucoin_Products = pickle.load(file4)
    file5 = open("Kraken_Prod_List",'rb')
    Kraken_Prod_List = pickle.load(file5)
    file6 = open("Kraken_Products",'rb')
    Kraken_Products = pickle.load(file6)
    file7 = open("Kraken_Prod_List2",'rb')
    Kraken_Prod_List2 = pickle.load(file7)
    file8 = open("Kraken_Products2",'rb')
    Kraken_Products2 = pickle.load(file8)
    file9 = open("Gemini_Prod_List",'rb')
    Gemini_Prod_List = pickle.load(file9)
    file10 = open("Gemini_Products",'rb')
    Gemini_Products = pickle.load(file10)
    file11 = open("Gemini_Prod_List2",'rb')
    Gemini_Prod_List2 = pickle.load(file11)
    file12 = open("Gemini_Products2",'rb')
    Gemini_Products2 = pickle.load(file12)
    file12 = open("Gemini_Products2",'rb')
    filtered_subset_Ccheck = pickle.load(file12)
    
def save_current_df_Ccheck():
    global CB_Products
    global CB_Prod_List
    global Kucoin_Prod_List
    global Kucoin_Products
    global Kraken_Prod_List
    global Kraken_Products
    global Kraken_Prod_List2
    global Kraken_Products2
    global Gemini_Prod_List
    global Gemini_Products
    global Gemini_Prod_List2
    global Gemini_Products2
    global filtered_subset_Ccheck
    
    with open("CB_Products","wb") as f:
        pickle.dump(CB_Products, f)

    with open("CB_Prod_List","wb") as f:
        pickle.dump(CB_Prod_List, f)

    with open("Kucoin_Prod_List","wb") as f:
        pickle.dump(Kucoin_Prod_List, f)

    with open("Kucoin_Products","wb") as f:
        pickle.dump(Kucoin_Products, f)

    with open("Kraken_Prod_List","wb") as f:
        pickle.dump(Kraken_Prod_List, f)

    with open("Kraken_Products","wb") as f:
        pickle.dump(Kraken_Products, f)

    with open("Kraken_Prod_List2","wb") as f:
        pickle.dump(Kraken_Prod_List2, f)

    with open("Kraken_Products2","wb") as f:
        pickle.dump(Kraken_Products2, f)

    with open("Gemini_Prod_List","wb") as f:
        pickle.dump(Gemini_Prod_List, f)

    with open("Gemini_Products","wb") as f:
        pickle.dump(Gemini_Products, f)

    with open("Gemini_Prod_List2","wb") as f:
        pickle.dump(Gemini_Prod_List2, f)

    with open("Gemini_Products2","wb") as f:
        pickle.dump(Gemini_Products2, f)

    Cross_results.to_csv("Cross_results.csv")
    return

# Create Dropdown menu
drop1_Ccheck = tk.OptionMenu( tab2 , column_name_Ccheck , *column_names_Ccheck )
drop1_Ccheck.place(x=0, y=600)
drop1_Ccheck.config(width = 12)

# Create Dropdown menu
drop2_Ccheck = tk.OptionMenu( tab2 , condition_Ccheck , *conditions_Ccheck )
drop2_Ccheck.place(x=125, y=600)
drop2_Ccheck.config(width = 12)

# Create Dropdown menu
drop3_Ccheck = tk.OptionMenu( tab2 , comparison_Ccheck , *comparisons_Ccheck )
drop3_Ccheck.place(x=530, y=600)
drop3_Ccheck.config(width = 3)

# Create Dropdown menu
drop_sort_Ccheck = tk.OptionMenu( tab2 , sort_by_Ccheck , *sort_bys_Ccheck )
drop_sort_Ccheck.place(x=650, y=600)
drop_sort_Ccheck.config(width = 12)

# Create Dropdown menu
drop_ascend_Ccheck = tk.OptionMenu( tab2 , ascend_Ccheck , *ascends_Ccheck )
drop_ascend_Ccheck.place(x=775, y=600)
drop_ascend_Ccheck.config(width = 12)

# Create Label for sorting status
label3_Ccheck= tk.Label( tab2 , text = " " )
label3_Ccheck.place(x=700, y=575)

# Create quote_ticker Entry Box1
quote_ticker = tk.StringVar(tab2)
quote_ticker_entry = tk.Entry(tab2, textvariable=quote_ticker).place(x=400, y=800)

# Create Label for sorting status
label_sortby_Ccheck = tk.Label( tab2 , text = "Sort by:" )
label_sortby_Ccheck.place(x=650, y=575)

# Create Entry Box1
value_Ccheck = tk.StringVar(tab2)
value_Ccheck_entry = tk.Entry(tab2, textvariable=value_Ccheck).place(x=400, y=600)

# Create Entry Box2
contains_Ccheck = tk.StringVar(tab2)
contains_Ccheck_entry = tk.Entry(tab2, textvariable=contains_Ccheck).place(x=250, y=600)

# Create button, it will change label text
button1_Ccheck = tk.Button( tab2 , text = "Add Filter" , command = add_filter_Ccheck).place(x=100, y=550)

# Create button, it will change label text
button2_Ccheck = tk.Button( tab2 , text = "Finalize Filter Set" , command = create_filter_set_Ccheck).place(x=200, y=550)

# Create button, it will change label text
button3_Ccheck = tk.Button( tab2 , text = "Clear Filter Set" , command = clear_filter_set_Ccheck).place(x=325, y=550)

# Create Label
label1_Ccheck= tk.Label( tab2 , text = " " )
label1_Ccheck.place(x=100, y=525)

# Create Label
label2_Ccheck = tk.Label( tab2 , text = " " )
label2_Ccheck.place(x=100, y=500)

# Create Label
label_filter_Ccheck= tk.Label( tab2 , text = "Filter Set:" )
label_filter_Ccheck.place(x=25, y=500)

# Create Label
label_filter_Ccheck= tk.Label( tab2 , text = "Filter(s):" )
label_filter_Ccheck.place(x=25, y=525)

# Create button
check1_Ccheck = tk.Button(tab2, text ="Sort", command = sort_checked_Ccheck)
check1_Ccheck.place(x=650, y=550)

# Create button
check1_Ccheck = tk.Button(tab2, text = "Save Current DF", command = save_current_df_Ccheck)
check1_Ccheck.place(x=25, y=700)

def openFile_Ccheck():
    global tri_on_Ccheck
    global tri_results_Ccheck
    global filtered_subset_Ccheck

    tri_on_Ccheck = True
    filepath = filedialog.askopenfilename(initialdir= os.getcwd(),
                                          title="Load CSV",
                                          filetypes= (("CSV Files","*.csv"),))
    
    tri_results_Ccheck = pd.read_csv(filepath)
    tri_results_Ccheck = tri_results_Ccheck.drop('Unnamed: 0', axis=1)
    filtered_subset_Ccheck = tri_results_Ccheck
    Load_data_Ccheck(filtered_subset_Ccheck)

# Create button, it will change label text
button4_Ccheck = tk.Button( tab2 , text = "Load CSV" , command = openFile_Ccheck).place(x=125, y=700)

# Create button, to load pickled results from previous session
button5_Ccheck = tk.Button( tab2 , text = "Load_Ccheck_Products" , command = Load_Ccheck_Products).place(x=125, y=725)

############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################

# Tricheck_Gemini Tab:

def clear_data_Gemini():
    tv_Gemini.delete(*tv_Gemini.get_children())
    return None

def Load_data_Gemini(df):
    
    clear_data_Gemini()
    tv_Gemini["column"] = list(df.columns)
    tv_Gemini["show"] = "headings"
    for column in tv_Gemini["columns"]:
        tv_Gemini.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv_Gemini.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert

    return None

def Tricheck_Gemini_CallBack():
    global tri_results_Gemini
    global tri_on_Gemini
    global filtered_subset_Gemini
    global Gemini_Prod_List
    global Gemini_Products
    global Gemini_Prod_List2
    global Gemini_Products2 

    if tri_on_Gemini == False:
        tri_on_Gemini = True
        Gemini_Products, Gemini_Prod_List =  check_all_Gemini()
        Gemini_Products2, Gemini_Prod_List2 = formator_Gemini(Gemini_Products, Gemini_Prod_List)
        tickers, bi_paths, tri_paths = available_tickers_paths(Gemini_Prod_List2)
        tri_checked, tri_conversion = tri_check_CB(tri_paths, Gemini_Prod_List2, Gemini_Products2)
        data = []
        for i in range(len(tri_checked)):
            data.append([tri_checked[i], tri_conversion[i]])
        tri_results_Gemini = pd.DataFrame(data, columns=['tri_path', 'tri_conversion'])
        tri_results_Gemini = tri_update_panda_Gemini(tri_results_Gemini, Gemini_Products2, Gemini_Prod_List2)
        
    else: 
        Gemini_Products, Gemini_Prod_List = check_all_Gemini()
        Gemini_Products2 = update_dict_Gemini(Gemini_Products2, Gemini_Prod_List2, Gemini_Products)
        tri_results_Gemini = tri_update_panda_Gemini(tri_results_Gemini, Gemini_Products2, Gemini_Prod_List2)

    filtered_subset_Gemini = tri_results_Gemini
    label1_Gemini.config( text = "" )
    label2_Gemini.config( text = "" )
    label3_Gemini.config( text = "" )
    return Load_data_Gemini(filtered_subset_Gemini)

def Tricheck_Gemini_CallBack_test():
    global tri_results_Gemini
    global filtered_subset_Gemini
    tri_results_Gemini = pd.DataFrame(columns=['tri_path','tri_conversion','c1','cc1','c2','cc2','c3','cc3','v1',
                                           'vp1','v2','vp2','v3','vp3'])
    tri_results_Gemini['tri_path'] = ["BTC-USDC-UNI", "USDC-UNI-BTC", "UNI-BTC-USDC", "EUR-USDC-TILT", "USDC-TILT-EUR", "TILT-EUR-USDC"]
    tri_results_Gemini['tri_conversion'] = [3.6,3.6,3.6,1.68,1.68,1.68]
    tri_results_Gemini['c1'] = [2,3,0.6,2,0.7,1.2]
    tri_results_Gemini['cc1'] = [1,1,1,1,1,1]
    tri_results_Gemini['c2'] = [3,0.6,2,0.7,1.2,2]
    tri_results_Gemini['cc2'] = [1,1,1,1,1,1]
    tri_results_Gemini['c3'] = [0.6,2,3,1.2,2,0.7]
    tri_results_Gemini['cc3'] = [1,1,1,1,1,1]
    tri_results_Gemini['v1'] = [1,1,0,1,1,1]
    tri_results_Gemini['vp1'] = [1,1,1,1,1,1]
    tri_results_Gemini['v2'] = [1,1,1,1,1,1]
    tri_results_Gemini['vp2'] = [1,1,1,1,1,1]
    tri_results_Gemini['v3'] = [1,1,1,1,1,1]
    tri_results_Gemini['vp3'] = [1,1,1,1,1,1]

    filtered_subset_Gemini = tri_results_Gemini
    label1_Gemini.config( text = "" )
    label2_Gemini.config( text = "" )
    label3_Gemini.config( text = "" )
    return Load_data_Gemini(filtered_subset_Gemini)

def clicked_Gemini(event):
    global Gemini_Prod_List

    selected = tv_Gemini.focus()
    (tri_path, tri_conversion, c1, cc1, c2, cc2, c3, cc3) = tv_Gemini.item(selected, 'values') 

    tick1, tick2, tick3 = tri_path.split('-')
    if f"{tick2}{tick1}" in Gemini_Prod_List:
        win1 = f"{tick2}{tick1}"
    if f"{tick1}{tick2}" in Gemini_Prod_List:
        win1 = f"{tick1}{tick2}"
    
    if f"{tick3}{tick2}" in Gemini_Prod_List:
        win2 = f"{tick3}{tick2}"
    elif f"{tick2}{tick3}" in Gemini_Prod_List:
        win2 = f"{tick2}{tick3}"

    if f"{tick1}{tick3}" in Gemini_Prod_List:
        win3 = f"{tick1}{tick3}"
    elif f"{tick3}{tick1}" in Gemini_Prod_List:
        win3 = f"{tick3}{tick1}"

    url1 = f"https://exchange.gemini.com/trade/{win1}"
    webbrowser.open(url1, new=1, autoraise=True)

    url2 = f"https://exchange.gemini.com/trade/{win2}"
    webbrowser.open(url2, new=1, autoraise=True)

    url3 = f"https://exchange.gemini.com/trade/{win3}"
    webbrowser.open(url3, new=1, autoraise=True)

# Frame for TreeView
frame_Gemini = tk.LabelFrame(tab4, text="DataFrame")
frame_Gemini.place(height=500, width=1000)

## Treeview Widget
tv_Gemini = ttk.Treeview(frame_Gemini)
tv_Gemini.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).
tv_Gemini.bind("<Double-1>", clicked_Gemini)

treescrolly_Gemini = tk.Scrollbar(frame_Gemini, orient="vertical", command=tv_Gemini.yview) # command means update the yaxis view of the widget
treescrollx_Gemini = tk.Scrollbar(frame_Gemini, orient="horizontal", command=tv_Gemini.xview) # command means update the xaxis view of the widget
tv_Gemini.configure(xscrollcommand=treescrollx_Gemini.set, yscrollcommand=treescrolly_Gemini.set) # assign the scrollbars to the Treeview Widget
treescrollx_Gemini.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly_Gemini.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

# Create TriCheck button
B_Gemini = tk.Button(tab4, text ="TriCheck", command = Tricheck_Gemini_CallBack)
B_Gemini.place(x=25, y=550)

# datatype of menu text
clicked2 = tk.StringVar(tab4)
  
# initial menu text
clicked2.set( "v1" )

# Change the label text for filter to be added
filter_2_print_list_Gemini = []
def show1_Gemini(filter_2_print):
    global filter_list_Gemini
    global comparison_list_Gemini

    filter_2_print_list_Gemini.append(filter_2_print, comparison_list_Gemini)

# Change the label text for final filter set
def show2_Gemini(filtered_subset):

    label2_Gemini.config( text = f"{filtered_subset}" )

# Variable to keep track of the option
# selected in OptionMenu
column_name_Gemini = tk.StringVar(tab4)
  
# Set the default value of the variable
column_name_Gemini.set("tri_path")

# Create Label for sorting status
label_column_Gemini= tk.Label( tab4 , text = "Column:" )
label_column_Gemini.place(x=0, y=580)

# Variable to keep track of the option
# selected in OptionMenu
condition_Gemini = tk.StringVar(tab4)
  
# Set the default value of the variable
condition_Gemini.set(".str.contains()")

# Create Label for sorting status
label_condition_Gemini= tk.Label( tab4 , text = "Condition:" )
label_condition_Gemini.place(x=125, y=580)

# Create Label for sorting status
label_condition_Gemini= tk.Label( tab4 , text = "Contains:" )
label_condition_Gemini.place(x=250, y=580)

# Create Label for sorting status
label_condition_Gemini= tk.Label( tab4 , text = "Value:" )
label_condition_Gemini.place(x=400, y=580)

# Variable to keep track of the option
# selected in OptionMenu
comparison_Gemini = tk.StringVar(tab4)
  
# Set the default value of the variable
comparison_Gemini.set("")

# Create Label for sorting status
label_comparison_Gemini= tk.Label( tab4 , text = "&|:" )
label_comparison_Gemini.place(x=530, y=580)

# selected in OptionMenu
sort_by_Gemini = tk.StringVar(tab4)

# Set the default value of the variable
sort_by_Gemini.set("tri_path")

# selected in OptionMenu
ascend_Gemini = tk.StringVar(tab4)

# Set the default value of the variable
ascend_Gemini.set("Ascending")

 # Dropdown menu options
column_names_Gemini = ["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", "cc3"]

conditions_Gemini = [".str.contains()", ".isna()", "==", ">", ">=", "<", "<="]

comparisons_Gemini = ["", " & ", " | "]

sort_bys_Gemini = ["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", "cc3"]

ascends_Gemini = ["Ascending", "Decending"]

ascends_dict_Gemini = {"Ascending" : " True ", "Decending" : " False "}

filter_list_Gemini = []
comparison_list_Gemini = []

def add_filter_Gemini():
    global filter_list_Gemini
    global comparison_list_Gemini
    global comparison_Gemini
    global value_Gemini
    global condition_Gemini
    global column_name_Gemini
    global tri_results_Gemini_filter
    global contains_Gemini

    tri_results_Gemini_filter = "filtered_subset_Gemini"

    if condition_Gemini.get() == ".str.contains()":
        tri_results_Gemini_filter = f"filtered_subset_Gemini['{column_name_Gemini.get()}'].str.contains('{contains_Gemini.get()}') == {value_Gemini.get()}"

    elif condition_Gemini.get() == ".isna()":
        tri_results_Gemini_filter = f"filtered_subset_Gemini['{column_name_Gemini.get()}'].isna() == {value_Gemini.get()}"

    elif condition_Gemini.get() == "==":
        tri_results_Gemini_filter = f"filtered_subset_Gemini['{column_name_Gemini.get()}'] == {value_Gemini.get()}"

    elif condition_Gemini.get() == ">":
        tri_results_Gemini_filter = f"filtered_subset_Gemini['{column_name_Gemini.get()}'] > {value_Gemini.get()}"

    elif condition_Gemini.get() == ">=":
        tri_results_Gemini_filter = f"filtered_subset_Gemini['{column_name_Gemini.get()}'] >= {value_Gemini.get()}"

    elif condition_Gemini.get() == "<":
        tri_results_Gemini_filter = f"filtered_subset_Gemini['{column_name_Gemini.get()}'] < {value_Gemini.get()}"

    elif condition_Gemini.get() == "<=":
        tri_results_Gemini_filter = f"filtered_subset_Gemini['{column_name_Gemini.get()}'] <= {value_Gemini.get()}"

    else:
        print(condition_Gemini.get())

    filter_list_Gemini.append(tri_results_Gemini_filter)
    comparison_list_Gemini.append(comparison_Gemini.get())

    for i in range(len(filter_list_Gemini)):
        if i == 0:
            combo_2_print = f"({filter_list_Gemini[i]}){comparison_list_Gemini[i]}"
        else:
            combo_2_print = combo_2_print + f"({filter_list_Gemini[i]}){comparison_list_Gemini[i]}"

    label1_Gemini.config( text = combo_2_print )

    return print(tri_results_Gemini_filter)
    

def create_filter_set_Gemini():
    global comparison_list_Gemini
    global filter_list_Gemini
    global filtered_subset_Gemini
    global filtered_subtext_Gemini
    
    label1_Gemini.config( text = "" )
    label2_Gemini.config( text = "" )
    label3_Gemini.config( text = "" )

    k = len(filter_list_Gemini)

    if len(tri_results_Gemini) > 0:
        filtered_subset_Gemini = tri_results_Gemini
        filtered_subset_Gemini.reset_index()

        if k == 1:
            filtered_subtext_Gemini = f"filtered_subset_Gemini[{filter_list_Gemini[0]}]"
            print(filtered_subtext_Gemini)
            print(column_name_Gemini.get())
            print(condition_Gemini.get())
            print(comparison_Gemini.get())
            print(value_Gemini.get())
            print(filtered_subset_Gemini)
            exec(f"global filtered_subset_Gemini; filtered_subset_Gemini = {filtered_subtext_Gemini}")
            print(filtered_subset_Gemini)

        if k > 1:
            combo = ""
            for i in range(k):
                if i < k-1:
                    combo = combo + f"({filter_list_Gemini[i]}){comparison_list_Gemini[i]}"
                else:
                    combo = combo + f"({filter_list_Gemini[i]}){comparison_list_Gemini[i]}"
                    filtered_subtext_Gemini = f"filtered_subset_Gemini[{combo}]"
                    print(filtered_subtext_Gemini)
                    print(column_name_Gemini.get())
                    print(condition_Gemini.get())
                    print(comparison_Gemini.get())
                    print(value_Gemini.get())
                    print(filtered_subset_Gemini)
                    exec(f"global filtered_subset_Gemini; filtered_subset_Gemini = {filtered_subtext_Gemini}")
                    print(filtered_subset_Gemini)
    
    else:
        filtered_subset_Gemini = pd.DataFrame(columns=["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", 
                "cc3"])

    label2_Gemini.config( text = f"{filtered_subtext_Gemini}" )
    return Load_data_Gemini(filtered_subset_Gemini), print("finalized")
#    return filtered_subset

def sort_checked_Gemini():
    global filtered_subset_Gemini
    global sort_check_Gemini
    global sort_by_Gemini
    global ascend_Gemini

    exec(f"global sorted_subset_Gemini; sorted_subset_Gemini = filtered_subset_Gemini.sort_values(by= '{sort_by_Gemini.get()}', ascending={ascends_dict_Gemini[ascend_Gemini.get()]})")
    label3_Gemini.config( text = f"{ascend_Gemini.get()}" )
    return Load_data_Gemini(sorted_subset_Gemini), print("sorted")

def clear_filter_set_Gemini():
    global filter_list_Gemini
    global comparison_list_Gemini

    filter_list_Gemini = []
    comparison_list_Gemini = []

    label1_Gemini.config( text = "" )

    return None

def Load_Gemini_Products():
    global Gemini_Products
    global Gemini_Prod_List
    global Gemini_Products2
    global Gemini_Prod_List2

    file1 = open("Gemini_Products",'rb')
    Gemini_Products = pickle.load(file1)
    file2 = open("Gemini_Prod_List",'rb')
    Gemini_Prod_List = pickle.load(file2)
    file3 = open("Gemini_Products",'rb')
    Gemini_Products2 = pickle.load(file3)
    file4 = open("Gemini_Prod_List",'rb')
    Gemini_Prod_List2 = pickle.load(file4)

def save_current_df_Gemini():
    global filtered_subset_Gemini
    global Gemini_Products
    global Gemini_Prod_List
    global Gemini_Products2
    global Gemini_Prod_List2
    
    with open("Gemini_Products","wb") as f:
        pickle.dump(Gemini_Products, f)

    with open("Gemini_Prod_List","wb") as f:
        pickle.dump(Gemini_Prod_List, f)

    with open("Gemini_Products2","wb") as f:
        pickle.dump(Gemini_Products2, f)

    with open("Gemini_Prod_List2","wb") as f:
        pickle.dump(Gemini_Prod_List2, f)
    filtered_subset_Gemini.to_csv("tri_results_Gemini.csv")
    return

# Create Dropdown menu
drop1_Gemini = tk.OptionMenu( tab4 , column_name_Gemini , *column_names_Gemini )
drop1_Gemini.place(x=0, y=600)
drop1_Gemini.config(width = 12)

# Create Dropdown menu
drop2_Gemini = tk.OptionMenu( tab4 , condition_Gemini , *conditions_Gemini )
drop2_Gemini.place(x=125, y=600)
drop2_Gemini.config(width = 12)

# Create Dropdown menu
drop3_Gemini = tk.OptionMenu( tab4 , comparison_Gemini , *comparisons_Gemini )
drop3_Gemini.place(x=530, y=600)
drop3_Gemini.config(width = 3)

# Create Dropdown menu
drop_sort_Gemini = tk.OptionMenu( tab4 , sort_by_Gemini , *sort_bys_Gemini )
drop_sort_Gemini.place(x=650, y=600)
drop_sort_Gemini.config(width = 12)

# Create Dropdown menu
drop_ascend_Gemini = tk.OptionMenu( tab4 , ascend_Gemini , *ascends_Gemini )
drop_ascend_Gemini.place(x=775, y=600)
drop_ascend_Gemini.config(width = 12)

# Create Label for sorting status
label3_Gemini= tk.Label( tab4 , text = " " )
label3_Gemini.place(x=700, y=575)

# Create Label for sorting status
label_sortby_Gemini = tk.Label( tab4 , text = "Sort by:" )
label_sortby_Gemini.place(x=650, y=575)

# Create Entry Box1
value_Gemini = tk.StringVar(tab4)
value_Gemini_entry = tk.Entry(tab4, textvariable=value_Gemini).place(x=400, y=600)

# Create Entry Box2
contains_Gemini = tk.StringVar(tab4)
contains_Gemini_entry = tk.Entry(tab4, textvariable=contains_Gemini).place(x=250, y=600)

# Create button, it will change label text
button1_Gemini = tk.Button( tab4 , text = "Add Filter" , command = add_filter_Gemini).place(x=100, y=550)

# Create button, it will change label text
button2_Gemini = tk.Button( tab4 , text = "Finalize Filter Set" , command = create_filter_set_Gemini).place(x=200, y=550)

# Create button, it will change label text
button3_Gemini = tk.Button( tab4 , text = "Clear Filter Set" , command = clear_filter_set_Gemini).place(x=325, y=550)

# Create Label
label1_Gemini= tk.Label( tab4 , text = " " )
label1_Gemini.place(x=100, y=525)

# Create Label
label2_Gemini = tk.Label( tab4 , text = " " )
label2_Gemini.place(x=100, y=500)

# Create Label
label_filter_Gemini= tk.Label( tab4 , text = "Filter Set:" )
label_filter_Gemini.place(x=25, y=500)

# Create Label
label_filter_Gemini= tk.Label( tab4 , text = "Filter(s):" )
label_filter_Gemini.place(x=25, y=525)

# Create button
check1_Gemini = tk.Button(tab4, text ="Sort", command = sort_checked_Gemini)
check1_Gemini.place(x=650, y=550)

# Create button
check1_Gemini = tk.Button(tab4, text = "Save Current DF", command = save_current_df_Gemini)
check1_Gemini.place(x=25, y=700)

def openFile_Gemini():
    global tri_on_Gemini
    global tri_results_Gemini
    global filtered_subset_Gemini

    tri_on_Gemini = True
    filepath = filedialog.askopenfilename(initialdir= os.getcwd(),
                                          title="Load CSV",
                                          filetypes= (("CSV Files","*.csv"),))
    
    tri_results_Gemini = pd.read_csv(filepath)
    tri_results_Gemini = tri_results_Gemini.drop('Unnamed: 0', axis=1)
    filtered_subset_Gemini = tri_results_Gemini
    Load_data_Gemini(filtered_subset_Gemini)

# Create button, it will change label text
button4_Gemini = tk.Button( tab4 , text = "Load CSV" , command = openFile_Gemini).place(x=125, y=700)

# Create button, to load pickled results from previous session
button5_Gemini = tk.Button( tab4 , text = "Load_Gemini_Products" , command = Load_Gemini_Products).place(x=125, y=725)

########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################

# Tricheck_Kraken Tab:

def clear_data_Kraken():
    tv_Kraken.delete(*tv_Kraken.get_children())

def Load_data_Kraken(df):
    
    clear_data_Kraken()
    tv_Kraken["column"] = list(df.columns)
    tv_Kraken["show"] = "headings"
    for column in tv_Kraken["columns"]:
        tv_Kraken.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv_Kraken.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
        
def Tricheck_Kraken_CallBack():
    global tri_results_Kraken
    global tri_on_Kraken
    global filtered_subset_Kraken
    global Kraken_Prod_List
    global Kraken_Products
    global Kraken_Prod_List2
    global Kraken_Products2

    if tri_on_Kraken == False:
        tri_on_Kraken = True
        Kraken_Products, Kraken_Prod_List, In_The_Kraken =  check_all_Kraken()
        Kraken_Products2, Kraken_Prod_List2 = formator_Kraken(Kraken_Products, Kraken_Prod_List)
        tickers, bi_paths, tri_paths = available_tickers_paths(Kraken_Prod_List2)
        tri_checked, tri_conversion = tri_check_CB(tri_paths, Kraken_Prod_List2, Kraken_Products2)
        data = []
        for i in range(len(tri_checked)):
            data.append([tri_checked[i], tri_conversion[i]])
        tri_results_Kraken = pd.DataFrame(data, columns=['tri_path', 'tri_conversion'])
        tri_results_Kraken = tri_update_panda_Kraken(tri_results_Kraken, Kraken_Products2, Kraken_Prod_List2)
        
    else: 
        Kraken_Products, Kraken_Prod_List, In_The_Kraken  = check_all_Kraken()
        Kraken_Products2 = update_dict_Kraken(Kraken_Products2, Kraken_Prod_List2, Kraken_Products)
        tri_results_Kraken = tri_update_panda_Kraken(tri_results_Kraken, Kraken_Products2, Kraken_Prod_List2)
        
    filtered_subset_Kraken = tri_results_Kraken
    label1_Kraken.config( text = "" )
    label2_Kraken.config( text = "" )
    label3_Kraken.config( text = "" )

    return Load_data_Kraken(filtered_subset_Kraken)

def Tricheck_Kraken_CallBack_test():
    global tri_results_Kraken
    global filtered_subset_Kraken
    tri_results_Kraken = pd.DataFrame(columns=['tri_path','tri_conversion','c1','cc1','c2','cc2','c3','cc3','v1',
                                           'vp1','v2','vp2','v3','vp3'])
    tri_results_Kraken['tri_path'] = ["BTC-USDC-UNI", "USDC-UNI-BTC", "UNI-BTC-USDC", "EUR-USDC-TILT", "USDC-TILT-EUR", "TILT-EUR-USDC"]
    tri_results_Kraken['tri_conversion'] = [3.6,3.6,3.6,1.68,1.68,1.68]
    tri_results_Kraken['c1'] = [2,3,0.6,2,0.7,1.2]
    tri_results_Kraken['cc1'] = [1,1,1,1,1,1]
    tri_results_Kraken['c2'] = [3,0.6,2,0.7,1.2,2]
    tri_results_Kraken['cc2'] = [1,1,1,1,1,1]
    tri_results_Kraken['c3'] = [0.6,2,3,1.2,2,0.7]
    tri_results_Kraken['cc3'] = [1,1,1,1,1,1]
    tri_results_Kraken['v1'] = [1,1,0,1,1,1]
    tri_results_Kraken['vp1'] = [1,1,1,1,1,1]
    tri_results_Kraken['v2'] = [1,1,1,1,1,1]
    tri_results_Kraken['vp2'] = [1,1,1,1,1,1]
    tri_results_Kraken['v3'] = [1,1,1,1,1,1]
    tri_results_Kraken['vp3'] = [1,1,1,1,1,1]

    filtered_subset_Kraken = tri_results_Kraken
    label1_Kraken.config( text = "" )
    label2_Kraken.config( text = "" )
    label3_Kraken.config( text = "" )
    return Load_data_Kraken(filtered_subset_Kraken)

def clicked_Kraken(event):
    global Kraken_Prod_List2
    global Kraken_Products2

    selected = tv_Kraken.focus()
    (tri_path, tri_conversion, c1, lot_volume_1, vol_today_1, vol_24h_1, c2, 
    lot_volume_2, vol_today_2, vol_24h_2, c3, lot_volume_3, vol_today_3, vol_24h_3) = tv_Kraken.item(selected, 'values') 



    tick1, tick2, tick3 = tri_path.split('-')
    if f"{tick2}-{tick1}" in Kraken_Prod_List2:
        win1 = f"{tick2}-{tick1}"
    elif f"{tick1}-{tick2}" in Kraken_Prod_List2:
        win1 = f"{tick1}-{tick2}"
    
    if f"{tick3}-{tick2}" in Kraken_Prod_List2:
        win2 = f"{tick3}-{tick2}"
    elif f"{tick2}-{tick3}" in Kraken_Prod_List2:
        win2 = f"{tick2}-{tick3}"

    if f"{tick1}-{tick3}" in Kraken_Prod_List2:
        win3 = f"{tick1}-{tick3}"
    elif f"{tick3}-{tick1}" in Kraken_Prod_List2:
        win3 = f"{tick3}-{tick1}"
    print(win1)
    print(win2)
    print(win3)

    url1 = f"https://pro.kraken.com/app/trade/{win1}"
    webbrowser.open(url1, new=1, autoraise=True)

    url2 = f"https://pro.kraken.com/app/trade/{win2}"
    webbrowser.open(url2, new=1, autoraise=True)

    url3 = f"https://pro.kraken.com/app/trade/{win3}"
    webbrowser.open(url3, new=1, autoraise=True)

# Frame for TreeView
frame_Kraken = tk.LabelFrame(tab5, text="DataFrame")
frame_Kraken.place(height=500, width=1000)

## Treeview Widget
tv_Kraken = ttk.Treeview(frame_Kraken)
tv_Kraken.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).
tv_Kraken.bind("<Double-1>", clicked_Kraken)

treescrolly_Kraken = tk.Scrollbar(frame_Kraken, orient="vertical", command=tv_Kraken.yview) # command means update the yaxis view of the widget
treescrollx_Kraken = tk.Scrollbar(frame_Kraken, orient="horizontal", command=tv_Kraken.xview) # command means update the xaxis view of the widget
tv_Kraken.configure(xscrollcommand=treescrollx_Kraken.set, yscrollcommand=treescrolly_Kraken.set) # assign the scrollbars to the Treeview Widget
treescrollx_Kraken.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly_Kraken.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

# Create TriCheck button
B_Kraken = tk.Button(tab5, text ="TriCheck", command = Tricheck_Kraken_CallBack)
B_Kraken.place(x=25, y=550)

# datatype of menu text
clicked3 = tk.StringVar(tab5)
  
# initial menu text
clicked3.set( "v1" )

# Change the label text for filter to be added
filter_2_print_list_Kraken = []
def show1_Kraken(filter_2_print):
    global filter_list_Kraken
    global comparison_list_Kraken
#    filter_2_print = f"{column_name}, {condition}, {value}, {comparison}, {conatins}"
    filter_2_print_list_Kraken.append(filter_2_print, comparison_list_Kraken)
#    for i in filter_2_print_list_cb:
#    label1.config( text = filter_2_print )
# Change the label text for final filter set
def show2_Kraken(filtered_subset):
    #label_2 = clicked.get()
    label2_Kraken.config( text = f"{filtered_subset}" )
#    filter_set_2_print = f"{filtered_subset}"

# Variable to keep track of the option
# selected in OptionMenu
column_name_Kraken = tk.StringVar(tab5)
  
# Set the default value of the variable
column_name_Kraken.set("tri_path")

# Create Label for sorting status
label_column_Kraken= tk.Label( tab5 , text = "Column:" )
label_column_Kraken.place(x=0, y=580)

# Variable to keep track of the option
# selected in OptionMenu
condition_Kraken = tk.StringVar(tab5)
  
# Set the default value of the variable
condition_Kraken.set(".str.contains()")

# Create Label for sorting status
label_condition_Kraken= tk.Label( tab5 , text = "Condition:" )
label_condition_Kraken.place(x=125, y=580)

# Create Label for sorting status
label_condition_Kraken= tk.Label( tab5 , text = "Contains:" )
label_condition_Kraken.place(x=250, y=580)

# Create Label for sorting status
label_condition_Kraken= tk.Label( tab5 , text = "Value:" )
label_condition_Kraken.place(x=400, y=580)

# Variable to keep track of the option
# selected in OptionMenu
comparison_Kraken = tk.StringVar(tab5)
  
# Set the default value of the variable
comparison_Kraken.set("")

# Create Label for sorting status
label_comparison_Kraken= tk.Label( tab5 , text = "&|:" )
label_comparison_Kraken.place(x=530, y=580)

# selected in OptionMenu
sort_by_Kraken = tk.StringVar(tab5)

# Set the default value of the variable
sort_by_Kraken.set("tri_path")

# selected in OptionMenu
ascend_Kraken = tk.StringVar(tab5)

# Set the default value of the variable
ascend_Kraken.set("Ascending")

 # Dropdown menu options
column_names_Kraken = ["tri_path", "tri_conversion", "c1", "lot_volume_1", "vol_today_1", "vol_24h_1", "c2", 
                       "lot_volume_2", "vol_today_2", "vol_24h_2", "c3", "lot_volume_3", "vol_today_3", "vol_24h_3"]

conditions_Kraken = [".str.contains()", ".isna()", "==", ">", ">=", "<", "<="]

comparisons_Kraken = ["", " & ", " | "]

sort_bys_Kraken = ["tri_path", "tri_conversion", "c1", "lot_volume_1", "vol_today_1", "vol_24h_1", "c2", 
                       "lot_volume_2", "vol_today_2", "vol_24h_2", "c3", "lot_volume_3", "vol_today_3", "vol_24h_3"]

ascends_Kraken = ["Ascending", "Decending"]

ascends_dict_Kraken = {"Ascending" : " True ", "Decending" : " False "}

filter_list_Kraken = []
comparison_list_Kraken = []

def add_filter_Kraken():
    global filter_list_Kraken
    global comparison_list_Kraken
    global comparison_Kraken
    global value_Kraken
    global condition_Kraken
    global column_name_Kraken
    global tri_results_Kraken_filter
    global contains_Kraken

    tri_results_Kraken_filter = "filtered_subset_Kraken"

    if condition_Kraken.get() == ".str.contains()":
        tri_results_Kraken_filter = f"filtered_subset_Kraken['{column_name_Kraken.get()}'].str.contains('{contains_Kraken.get()}') == {value_Kraken.get()}"

    elif condition_Kraken.get() == ".isna()":
        tri_results_Kraken_filter = f"filtered_subset_Kraken['{column_name_Kraken.get()}'].isna() == {value_Kraken.get()}"

    elif condition_Kraken.get() == "==":
        tri_results_Kraken_filter = f"filtered_subset_Kraken['{column_name_Kraken.get()}'] == {value_Kraken.get()}"

    elif condition_Kraken.get() == ">":
        tri_results_Kraken_filter = f"filtered_subset_Kraken['{column_name_Kraken.get()}'] > {value_Kraken.get()}"

    elif condition_Kraken.get() == ">=":
        tri_results_Kraken_filter = f"filtered_subset_Kraken['{column_name_Kraken.get()}'] >= {value_Kraken.get()}"

    elif condition_Kraken.get() == "<":
        tri_results_Kraken_filter = f"filtered_subset_Kraken['{column_name_Kraken.get()}'] < {value_Kraken.get()}"

    elif condition_Kraken.get() == "<=":
        tri_results_Kraken_filter = f"filtered_subset_Kraken['{column_name_Kraken.get()}'] <= {value_Kraken.get()}"

    else:
        print(condition_Kraken.get())

    filter_list_Kraken.append(tri_results_Kraken_filter)
    comparison_list_Kraken.append(comparison_Kraken.get())

    for i in range(len(filter_list_Kraken)):
        if i == 0:
            combo_2_print = f"({filter_list_Kraken[i]}){comparison_list_Kraken[i]}"
        else:
            combo_2_print = combo_2_print + f"({filter_list_Kraken[i]}){comparison_list_Kraken[i]}"

    label1_Kraken.config( text = combo_2_print )

    return print(tri_results_Kraken_filter)
    

def create_filter_set_Kraken():
    global comparison_list_Kraken
    global filter_list_Kraken
    global filtered_subset_Kraken
    global filtered_subtext_Kraken
    
    label1_Kraken.config( text = "" )
    label2_Kraken.config( text = "" )
    label3_Kraken.config( text = "" )

    k = len(filter_list_Kraken)

    if len(tri_results_Kraken) > 0:
        filtered_subset_Kraken = tri_results_Kraken
        filtered_subset_Kraken.reset_index()

        if k == 1:
            filtered_subtext_Kraken = f"filtered_subset_Kraken[{filter_list_Kraken[0]}]"
            print(filtered_subtext_Kraken)
            print(column_name_Kraken.get())
            print(condition_Kraken.get())
            print(comparison_Kraken.get())
            print(value_Kraken.get())
            print(filtered_subset_Kraken)
            exec(f"global filtered_subset_Kraken; filtered_subset_Kraken = {filtered_subtext_Kraken}")
            print(filtered_subset_Kraken)

        if k > 1:
            combo = ""
            for i in range(k):
                if i < k-1:
                    combo = combo + f"({filter_list_Kraken[i]}){comparison_list_Kraken[i]}"
                else:
                    combo = combo + f"({filter_list_Kraken[i]}){comparison_list_Kraken[i]}"
                    filtered_subtext_Kraken = f"filtered_subset_Kraken[{combo}]"
                    print(filtered_subtext_Kraken)
                    print(column_name_Kraken.get())
                    print(condition_Kraken.get())
                    print(comparison_Kraken.get())
                    print(value_Kraken.get())
                    print(filtered_subset_Kraken)
                    exec(f"global filtered_subset_Kraken; filtered_subset_Kraken = {filtered_subtext_Kraken}")
                    print(filtered_subset_Kraken)
    
    else:
        filtered_subset_Kraken = pd.DataFrame(columns=["tri_path", "tri_conversion", "c1", "lot_volume_1", "vol_today_1", "vol_24h_1", "c2", 
                                                        "lot_volume_2", "vol_today_2", "vol_24h_2", "c3", "lot_volume_3", "vol_today_3", "vol_24h_3"])

    label2_Kraken.config( text = f"{filtered_subtext_Kraken}" )
    return Load_data_Kraken(filtered_subset_Kraken), print("finalized")
#    return filtered_subset

def sort_checked_Kraken():
    global filtered_subset_Kraken
    global sort_check_Kraken
    global sort_by_Kraken
    global ascend_Kraken

    exec(f"global sorted_subset_Kraken; sorted_subset_Kraken = filtered_subset_Kraken.sort_values(by= '{sort_by_Kraken.get()}', ascending={ascends_dict_Kraken[ascend_Kraken.get()]})")
    label3_Kraken.config( text = f"{ascend_Kraken.get()}" )
    return Load_data_Kraken(sorted_subset_Kraken), print("sorted")

def clear_filter_set_Kraken():
    global filter_list_Kraken
    global comparison_list_Kraken

    filter_list_Kraken = []
    comparison_list_Kraken = []

    label1_Kraken.config( text = "" )

    return None

def Load_Kraken_Products():
    global Kraken_Products
    global Kraken_Prod_List
    global Kraken_Products2
    global Kraken_Prod_List2

    file1 = open("Kraken_Products",'rb')
    Kraken_Products = pickle.load(file1)
    file2 = open("Kraken_Prod_List",'rb')
    Kraken_Prod_List = pickle.load(file2)
    file3 = open("Kraken_Products2",'rb')
    Kraken_Products2 = pickle.load(file3)
    file4 = open("Kraken_Prod_List2",'rb')
    Kraken_Prod_List2 = pickle.load(file4)

def save_current_df_Kraken():
    global filtered_subset_Kraken
    global Kraken_Products
    global Kraken_Prod_List
    global Kraken_Products2
    global Kraken_Prod_List2
    
    with open("Kraken_Products","wb") as f:
        pickle.dump(Kraken_Products, f)

    with open("Kraken_Products2","wb") as f:
        pickle.dump(Kraken_Products2, f)

    with open("Kraken_Prod_List","wb") as f:
        pickle.dump(Kraken_Prod_List, f)

    with open("Kraken_Prod_List2","wb") as f:
        pickle.dump(Kraken_Prod_List2, f)
    filtered_subset_Kraken.to_csv("tri_results_Kraken.csv")
    return

# Create Dropdown menu
drop1_Kraken = tk.OptionMenu( tab5 , column_name_Kraken , *column_names_Kraken )
drop1_Kraken.place(x=0, y=600)
drop1_Kraken.config(width = 12)

# Create Dropdown menu
drop2_Kraken = tk.OptionMenu( tab5 , condition_Kraken , *conditions_Kraken )
drop2_Kraken.place(x=125, y=600)
drop2_Kraken.config(width = 12)

# Create Dropdown menu
drop3_Kraken = tk.OptionMenu( tab5 , comparison_Kraken , *comparisons_Kraken )
drop3_Kraken.place(x=530, y=600)
drop3_Kraken.config(width = 3)

# Create Dropdown menu
drop_sort_Kraken = tk.OptionMenu( tab5 , sort_by_Kraken , *sort_bys_Kraken )
drop_sort_Kraken.place(x=650, y=600)
drop_sort_Kraken.config(width = 12)

# Create Dropdown menu
drop_ascend_Kraken = tk.OptionMenu( tab5 , ascend_Kraken , *ascends_Kraken )
drop_ascend_Kraken.place(x=775, y=600)
drop_ascend_Kraken.config(width = 12)

# Create Label for sorting status
label3_Kraken= tk.Label( tab5 , text = " " )
label3_Kraken.place(x=700, y=575)

# Create Label for sorting status
label_sortby_Kraken = tk.Label( tab5 , text = "Sort by:" )
label_sortby_Kraken.place(x=650, y=575)

# Create Entry Box1
value_Kraken = tk.StringVar(tab5)
value_Kraken_entry = tk.Entry(tab5, textvariable=value_Kraken).place(x=400, y=600)

# Create Entry Box2
contains_Kraken = tk.StringVar(tab5)
contains_Kraken_entry = tk.Entry(tab5, textvariable=contains_Kraken).place(x=250, y=600)

# Create button, it will change label text
button1_Kraken = tk.Button( tab5 , text = "Add Filter" , command = add_filter_Kraken).place(x=100, y=550)

# Create button, it will change label text
button2_Kraken = tk.Button( tab5 , text = "Finalize Filter Set" , command = create_filter_set_Kraken).place(x=200, y=550)

# Create button, it will change label text
button3_Kraken = tk.Button( tab5 , text = "Clear Filter Set" , command = clear_filter_set_Kraken).place(x=325, y=550)

# Create Label
label1_Kraken= tk.Label( tab5 , text = " " )
label1_Kraken.place(x=100, y=525)

# Create Label
label2_Kraken = tk.Label( tab5 , text = " " )
label2_Kraken.place(x=100, y=500)

# Create Label
label_filter_Kraken= tk.Label( tab5 , text = "Filter Set:" )
label_filter_Kraken.place(x=25, y=500)

# Create Label
label_filter_Kraken= tk.Label( tab5 , text = "Filter(s):" )
label_filter_Kraken.place(x=25, y=525)

# Create button
check1_Kraken = tk.Button(tab5, text ="Sort", command = sort_checked_Kraken)
check1_Kraken.place(x=650, y=550)

# Create button
check1_Kraken = tk.Button(tab5, text = "Save Current DF", command = save_current_df_Kraken)
check1_Kraken.place(x=25, y=700)

def openFile_Kraken():
    global tri_on_Kraken
    global tri_results_Kraken
    global filtered_subset_Kraken

    tri_on_Kraken = True
    filepath = filedialog.askopenfilename(initialdir= os.getcwd(),
                                          title="Load CSV",
                                          filetypes= (("CSV Files","*.csv"),))
    
    tri_results_Kraken = pd.read_csv(filepath)
    tri_results_Kraken = tri_results_Kraken.drop('Unnamed: 0', axis=1)
    filtered_subset_Kraken = tri_results_Kraken
    Load_data_Kraken(filtered_subset_Kraken)

# Create button, it will change label text
button4_Kraken = tk.Button( tab5 , text = "Load CSV" , command = openFile_Kraken).place(x=125, y=700)

# Create button, to load pickled results from previous session
button5_Kraken = tk.Button( tab5 , text = "Load_Kraken_Products" , command = Load_Kraken_Products).place(x=125, y=725)

########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################

# Tricheck_Kucoin Tab:

def clear_data_Kucoin():
    tv_Kucoin.delete(*tv_Kucoin.get_children())
    return None

def Load_data_Kucoin(df):
    
    clear_data_Kucoin()
    tv_Kucoin["column"] = list(df.columns)
    tv_Kucoin["show"] = "headings"
    for column in tv_Kucoin["columns"]:
        tv_Kucoin.heading(column, text=column) # let the column heading = column name

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv_Kucoin.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
        
#        tv1.b=tk.Button(ta
# b3,text="update",command=tab3.ButtonPushed)

    return None

def Tricheck_Kucoin_CallBack():
    global tri_results_Kucoin
    global tri_on_Kucoin
    global filtered_subset_Kucoin
    global Kucoin_Prod_List
    global Kucoin_Products
    global ku_tickers

    if tri_on_Kucoin == False:
#        tri_on_Kucoin = True
        Kucoin_Products, Kucoin_Prod_List =  check_all_Kucoin()
        ku_tickers, bi_paths = available_tickers_bipaths(Kucoin_Prod_List)
        tri_results_Kucoin = available_trichecks_(ku_tickers)

        print(tri_results_Kucoin)

#    if tri_on_Kucoin == True: 
    
    filtered_subset_Kucoin = tri_results_Kucoin
    label1_Kucoin.config( text = "" )
    label2_Kucoin.config( text = "" )
    label3_Kucoin.config( text = "" )
    return Load_data_Kucoin(filtered_subset_Kucoin)

def Tricheck_Kucoin_CallBack_test():
    global tri_results_Kucoin
    global filtered_subset_Kucoin
    tri_results_Kucoin = pd.DataFrame(columns=['tri_path','tri_conversion','c1','cc1','c2','cc2','c3','cc3','v1',
                                           'vp1','v2','vp2','v3','vp3'])
    tri_results_Kucoin['tri_path'] = ["BTC-USDC-UNI", "USDC-UNI-BTC", "UNI-BTC-USDC", "EUR-USDC-TILT", "USDC-TILT-EUR", "TILT-EUR-USDC"]
    tri_results_Kucoin['tri_conversion'] = [3.6,3.6,3.6,1.68,1.68,1.68]
    tri_results_Kucoin['c1'] = [2,3,0.6,2,0.7,1.2]
    tri_results_Kucoin['cc1'] = [1,1,1,1,1,1]
    tri_results_Kucoin['c2'] = [3,0.6,2,0.7,1.2,2]
    tri_results_Kucoin['cc2'] = [1,1,1,1,1,1]
    tri_results_Kucoin['c3'] = [0.6,2,3,1.2,2,0.7]
    tri_results_Kucoin['cc3'] = [1,1,1,1,1,1]
    tri_results_Kucoin['v1'] = [1,1,0,1,1,1]
    tri_results_Kucoin['vp1'] = [1,1,1,1,1,1]
    tri_results_Kucoin['v2'] = [1,1,1,1,1,1]
    tri_results_Kucoin['vp2'] = [1,1,1,1,1,1]
    tri_results_Kucoin['v3'] = [1,1,1,1,1,1]
    tri_results_Kucoin['vp3'] = [1,1,1,1,1,1]

    filtered_subset_Kucoin = tri_results_Kucoin
    label1_Kucoin.config( text = "" )
    label2_Kucoin.config( text = "" )
    label3_Kucoin.config( text = "" )
    return Load_data_Kucoin(filtered_subset_Kucoin)

def clicked_Kucoin(event):
    global Kucoin_Prod_List

    selected = tv_Kucoin.focus()
    (tri_path, tri_conversion, c1, cc1, c2, cc2, c3, cc3, v1, vp1, v2, vp2, v3, vp3) = tv_Kucoin.item(selected, 'values') 

    tick1, tick2, tick3 = tri_path.split('-')
    if f"{tick2}-{tick1}" in Kucoin_Prod_List:
        win1 = f"{tick2}-{tick1}"
    if f"{tick1}-{tick2}" in Kucoin_Prod_List:
        win1 = f"{tick1}-{tick2}"
    

    if f"{tick3}-{tick2}" in Kucoin_Prod_List:
        win2 = f"{tick3}-{tick2}"
    elif f"{tick2}-{tick3}" in Kucoin_Prod_List:
        win2 = f"{tick2}-{tick3}"

    if f"{tick1}-{tick3}" in Kucoin_Prod_List:
        win3 = f"{tick1}-{tick3}"
    elif f"{tick3}-{tick1}" in Kucoin_Prod_List:
        win3 = f"{tick3}-{tick1}"

    url1 = f"https://www.coinbase.com/advanced-trade/{win1}"
    webbrowser.open(url1, new=1, autoraise=True)

    url2 = f"https://www.coinbase.com/advanced-trade/{win2}"
    webbrowser.open(url2, new=1, autoraise=True)

    url3 = f"https://www.coinbase.com/advanced-trade/{win3}"
    webbrowser.open(url3, new=1, autoraise=True)

# Frame for TreeView
frame_Kucoin = tk.LabelFrame(tab6, text="DataFrame")
frame_Kucoin.place(height=500, width=1000)

## Treeview Widget
tv_Kucoin = ttk.Treeview(frame_Kucoin)
tv_Kucoin.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).
tv_Kucoin.bind("<Double-1>", clicked_Kucoin)

treescrolly_Kucoin = tk.Scrollbar(frame_Kucoin, orient="vertical", command=tv_Kucoin.yview) # command means update the yaxis view of the widget
treescrollx_Kucoin = tk.Scrollbar(frame_Kucoin, orient="horizontal", command=tv_Kucoin.xview) # command means update the xaxis view of the widget
tv_Kucoin.configure(xscrollcommand=treescrollx_Kucoin.set, yscrollcommand=treescrolly_Kucoin.set) # assign the scrollbars to the Treeview Widget
treescrollx_Kucoin.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly_Kucoin.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

# Create TriCheck button
B_Kucoin = tk.Button(tab6, text ="TriCheck", command = Tricheck_Kucoin_CallBack)
B_Kucoin.place(x=25, y=550)

# datatype of menu text
clicked4 = tk.StringVar(tab6)
  
# initial menu text
clicked4.set( "v1" )

# Change the label text for filter to be added
filter_2_print_list_Kucoin = []
def show1_Kucoin(filter_2_print):
    global filter_list_Kucoin
    global comparison_list_Kucoin
#    filter_2_print = f"{column_name}, {condition}, {value}, {comparison}, {conatins}"
    filter_2_print_list_Kucoin.append(filter_2_print, comparison_list_Kucoin)

# Change the label text for final filter set
def show2_Kucoin(filtered_subset):
    #label_2 = clicked.get()
    label2_Kucoin.config( text = f"{filtered_subset}" )
#    filter_set_2_print = f"{filtered_subset}"

# Variable to keep track of the option
# selected in OptionMenu
column_name_Kucoin = tk.StringVar(tab6)
  
# Set the default value of the variable
column_name_Kucoin.set("tri_path")

# Create Label for sorting status
label_column_Kucoin= tk.Label( tab6 , text = "Column:" )
label_column_Kucoin.place(x=0, y=580)

# Variable to keep track of the option
# selected in OptionMenu
condition_Kucoin = tk.StringVar(tab6)
  
# Set the default value of the variable
condition_Kucoin.set(".str.contains()")

# Create Label for sorting status
label_condition_Kucoin= tk.Label( tab6 , text = "Condition:" )
label_condition_Kucoin.place(x=125, y=580)

# Create Label for sorting status
label_condition_Kucoin= tk.Label( tab6 , text = "Contains:" )
label_condition_Kucoin.place(x=250, y=580)

# Create Label for sorting status
label_condition_Kucoin= tk.Label( tab6 , text = "Value:" )
label_condition_Kucoin.place(x=400, y=580)

# Variable to keep track of the option
# selected in OptionMenu
comparison_Kucoin = tk.StringVar(tab6)
  
# Set the default value of the variable
comparison_Kucoin.set("")

# Create Label for sorting status
label_comparison_Kucoin= tk.Label( tab6 , text = "&|:" )
label_comparison_Kucoin.place(x=530, y=580)

# selected in OptionMenu
sort_by_Kucoin = tk.StringVar(tab6)

# Set the default value of the variable
sort_by_Kucoin.set("tri_path")

# selected in OptionMenu
ascend_Kucoin = tk.StringVar(tab6)

# Set the default value of the variable
ascend_Kucoin.set("Ascending")

 # Dropdown menu options
column_names_Kucoin = ["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", "cc3", "v1", "vp1", "v2", 
                "vp2", "v3", "vp3"]

conditions_Kucoin = [".str.contains()", ".isna()", "==", ">", ">=", "<", "<="]

comparisons_Kucoin = ["", " & ", " | "]

sort_bys_Kucoin = ["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", "cc3", "v1", "vp1", "v2", 
                "vp2", "v3", "vp3"]

ascends_Kucoin = ["Ascending", "Decending"]

ascends_dict_Kucoin = {"Ascending" : " True ", "Decending" : " False "}

filter_list_Kucoin = []
comparison_list_Kucoin = []

def add_filter_Kucoin():
    global filter_list_Kucoin
    global comparison_list_Kucoin
    global comparison_Kucoin
    global value_Kucoin
    global condition_Kucoin
    global column_name_Kucoin
    global tri_results_Kucoin_filter
    global contains_Kucoin

    tri_results_Kucoin_filter = "filtered_subset_Kucoin"

    if condition_Kucoin.get() == ".str.contains()":
        tri_results_Kucoin_filter = f"filtered_subset_Kucoin['{column_name_Kucoin.get()}'].str.contains('{contains_Kucoin.get()}') == {value_Kucoin.get()}"

    elif condition_Kucoin.get() == ".isna()":
        tri_results_Kucoin_filter = f"filtered_subset_Kucoin['{column_name_Kucoin.get()}'].isna() == {value_Kucoin.get()}"

    elif condition_Kucoin.get() == "==":
        tri_results_Kucoin_filter = f"filtered_subset_Kucoin['{column_name_Kucoin.get()}'] == {value_Kucoin.get()}"

    elif condition_Kucoin.get() == ">":
        tri_results_Kucoin_filter = f"filtered_subset_Kucoin['{column_name_Kucoin.get()}'] > {value_Kucoin.get()}"

    elif condition_Kucoin.get() == ">=":
        tri_results_Kucoin_filter = f"filtered_subset_KKucoin['{column_name_Kucoin.get()}'] >= {value_Kucoin.get()}"

    elif condition_Kucoin.get() == "<":
        tri_results_Kucoin_filter = f"filtered_subset_Kucoin['{column_name_Kucoin.get()}'] < {value_Kucoin.get()}"

    elif condition_Kucoin.get() == "<=":
        tri_results_Kucoin_filter = f"filtered_subset_Kucoin['{column_name_Kucoin.get()}'] <= {value_Kucoin.get()}"

    else:
        print(condition_Kucoin.get())

    filter_list_Kucoin.append(tri_results_Kucoin_filter)
    comparison_list_Kucoin.append(comparison_Kucoin.get())

    for i in range(len(filter_list_Kucoin)):
        if i == 0:
            combo_2_print = f"({filter_list_Kucoin[i]}){comparison_list_Kucoin[i]}"
        else:
            combo_2_print = combo_2_print + f"({filter_list_Kucoin[i]}){comparison_list_Kucoin[i]}"

    label1_Kucoin.config( text = combo_2_print )

    return print(tri_results_Kucoin_filter)
    

def create_filter_set_Kucoin():
    global comparison_list_Kucoin
    global filter_list_Kucoin
    global filtered_subset_Kucoin
    global filtered_subtext_Kucoin
    
    label1_Kucoin.config( text = "" )
    label2_Kucoin.config( text = "" )
    label3_Kucoin.config( text = "" )

    k = len(filter_list_Kucoin)

    if len(tri_results_Kucoin) > 0:
        filtered_subset_Kucoin = tri_results_Kucoin
        filtered_subset_Kucoin.reset_index()

        if k == 1:
            filtered_subtext_Kucoin = f"filtered_subset_Kucoin[{filter_list_Kucoin[0]}]"
            print(filtered_subtext_Kucoin)
            print(column_name_Kucoin.get())
            print(condition_Kucoin.get())
            print(comparison_Kucoin.get())
            print(value_Kucoin.get())
            print(filtered_subset_Kucoin)
            exec(f"global filtered_subset_Kucoin; filtered_subset_Kucoin = {filtered_subtext_Kucoin}")
            print(filtered_subset_Kucoin)

        if k > 1:
            combo = ""
            for i in range(k):
                if i < k-1:
                    combo = combo + f"({filter_list_Kucoin[i]}){comparison_list_Kucoin[i]}"
                else:
                    combo = combo + f"({filter_list_Kucoin[i]}){comparison_list_Kucoin[i]}"
                    filtered_subtext_Kucoin = f"filtered_subset_Kucoin[{combo}]"
                    print(filtered_subtext_Kucoin)
                    print(column_name_Kucoin.get())
                    print(condition_Kucoin.get())
                    print(comparison_Kucoin.get())
                    print(value_Kucoin.get())
                    print(filtered_subset_Kucoin)
                    exec(f"global filtered_subset_Kucoin; filtered_subset_Kucoin = {filtered_subtext_Kucoin}")
                    print(filtered_subset_Kucoin)
    
    else:
        filtered_subset_Kucoin = pd.DataFrame(columns=["tri_path", "tri_conversion", "c1", "cc1", "c2", "cc2", "c3", 
                "cc3", "v1", "vp1", "v2", "vp2", "v3", "vp3"])

    label2_Kucoin.config( text = f"{filtered_subtext_Kucoin}" )
    return Load_data_Kucoin(filtered_subset_Kucoin), print("finalized")
#    return filtered_subset

def sort_checked_Kucoin():
    global filtered_subset_Kucoin
    global sort_check_Kucoin
    global sort_by_Kucoin
    global ascend_Kucoin

    exec(f"global sorted_subset_Kucoin; sorted_subset_Kucoin = filtered_subset_Kucoin.sort_values(by= '{sort_by_Kucoin.get()}', ascending={ascends_dict_Kucoin[ascend_Kucoin.get()]})")
    label3_Kucoin.config( text = f"{ascend_Kucoin.get()}" )
    return Load_data_Kucoin(sorted_subset_Kucoin), print("sorted")

def clear_filter_set_Kucoin():
    global filter_list_Kucoin
    global comparison_list_Kucoin

    filter_list_Kucoin = []
    comparison_list_Kucoin = []

    label1_Kucoin.config( text = "" )

    return None

def Load_Kucoin_Products():
    global Kucoin_Products
    global Kucoin_Prod_List
    file1 = open("Kucoin_Products",'rb')
    Kucoin_Products = pickle.load(file1)
    file2 = open("Kucoin_Prod_List",'rb')
    Kucoin_Prod_List = pickle.load(file2)

def save_current_df_Kucoin():
    global filtered_subset_Kucoin
    global Kucoin_Products
    global Kucoin_Prod_List
    
    with open("Kucoin_Products","wb") as f:
        pickle.dump(Kucoin_Products, f)

    with open("Kucoin_Prod_List","wb") as f:
        pickle.dump(Kucoin_Prod_List, f)
    filtered_subset_Kucoin.to_csv("tri_results_Kucoin.csv")
    return

# Create Dropdown menu
drop1_Kucoin = tk.OptionMenu( tab6 , column_name_Kucoin , *column_names_Kucoin )
drop1_Kucoin.place(x=0, y=600)
drop1_Kucoin.config(width = 12)

# Create Dropdown menu
drop2_Kucoin = tk.OptionMenu( tab6 , condition_Kucoin , *conditions_Kucoin )
drop2_Kucoin.place(x=125, y=600)
drop2_Kucoin.config(width = 12)

# Create Dropdown menu
drop3_Kucoin = tk.OptionMenu( tab6 , comparison_Kucoin , *comparisons_Kucoin )
drop3_Kucoin.place(x=530, y=600)
drop3_Kucoin.config(width = 3)

# Create Dropdown menu
drop_sort_Kucoin = tk.OptionMenu( tab6 , sort_by_Kucoin , *sort_bys_Kucoin )
drop_sort_Kucoin.place(x=650, y=600)
drop_sort_Kucoin.config(width = 12)

# Create Dropdown menu
drop_ascend_Kucoin = tk.OptionMenu( tab6 , ascend_Kucoin , *ascends_Kucoin )
drop_ascend_Kucoin.place(x=775, y=600)
drop_ascend_Kucoin.config(width = 12)

# Create Label for sorting status
label3_Kucoin= tk.Label( tab6 , text = " " )
label3_Kucoin.place(x=700, y=575)

# Create Label for sorting status
label_sortby_Kucoin = tk.Label( tab6 , text = "Sort by:" )
label_sortby_Kucoin.place(x=650, y=575)

# Create Entry Box1
value_Kucoin = tk.StringVar(tab6)
value_Kucoin_entry = tk.Entry(tab6, textvariable=value_Kucoin).place(x=400, y=600)

# Create Entry Box2
contains_Kucoin = tk.StringVar(tab6)
contains_Kucoin_entry = tk.Entry(tab6, textvariable=contains_Kucoin).place(x=250, y=600)

# Create button, it will change label text
button1_Kucoin = tk.Button( tab6 , text = "Add Filter" , command = add_filter_Kucoin).place(x=100, y=550)

# Create button, it will change label text
button2_Kucoin = tk.Button( tab6 , text = "Finalize Filter Set" , command = create_filter_set_Kucoin).place(x=200, y=550)

# Create button, it will change label text
button3_Kucoin = tk.Button( tab6 , text = "Clear Filter Set" , command = clear_filter_set_Kucoin).place(x=325, y=550)

# Create Label
label1_Kucoin= tk.Label( tab6 , text = " " )
label1_Kucoin.place(x=100, y=525)

# Create Label
label2_Kucoin = tk.Label( tab6 , text = " " )
label2_Kucoin.place(x=100, y=500)

# Create Label
label_filter_Kucoin= tk.Label( tab6 , text = "Filter Set:" )
label_filter_Kucoin.place(x=25, y=500)

# Create Label
label_filter_Kucoin= tk.Label( tab6 , text = "Filter(s):" )
label_filter_Kucoin.place(x=25, y=525)

# Create button
check1_Kucoin = tk.Button(tab6, text ="Sort", command = sort_checked_Kucoin)
check1_Kucoin.place(x=650, y=550)

# Create button
check1_Kucoin = tk.Button(tab6, text = "Save Current DF", command = save_current_df_Kucoin)
check1_Kucoin.place(x=25, y=700)

def openFile_Kucoin():
    global tri_on_Kucoin
    global tri_results_Kucoin
    global filtered_subset_Kucoin

    tri_on_Kucoin = True
    filepath = filedialog.askopenfilename(initialdir= os.getcwd(),
                                          title="Load CSV",
                                          filetypes= (("CSV Files","*.csv"),))
    
    tri_results_Kucoin = pd.read_csv(filepath)
    tri_results_Kucoin = tri_results_Kucoin.drop('Unnamed: 0', axis=1)
    filtered_subset_Kucoin = tri_results_Kucoin
    Load_data_Kucoin(filtered_subset_Kucoin)

# Create button, it will change label text
button4_Kucoin = tk.Button( tab6 , text = "Load CSV" , command = openFile_Kucoin).place(x=125, y=700)

# Create button, to load pickled results from previous session
button5_Kucoin = tk.Button( tab6 , text = "Load_Kucoin_Products" , command = Load_Kucoin_Products).place(x=125, y=725)

root.mainloop() 
