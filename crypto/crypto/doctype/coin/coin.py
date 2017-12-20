# -*- coding: utf-8 -*-
# Copyright (c) 2017, Hemant Pema and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import requests, json

class Coin(Document):
	pass

@frappe.whitelist()
def update_coins_rate():
    last_run = frappe.get_doc('Coin API')
    if frappe.utils.time_diff_in_seconds(frappe.utils.now(),last_run.last_polled)>600:
        api_url = "https://api.coinmarketcap.com/v1/ticker/?convert=ZAR"
        response = requests.get(api_url)
        for coin in json.loads(response.text):
            exists = frappe.db.exists('Coin', {'id': coin['id']})
            if not exists:
                newcoin = frappe.new_doc('Coin')
                newcoin.id = coin['id']
                newcoin.coin_name = coin['name']
                newcoin.symbol = coin['symbol']
                newcoin.rank=int(coin['rank'])
                newcoin.usd_price = coin['price_usd']
                newcoin.zar_price = coin['price_zar']
                newcoin.insert()
            else:
                exists = frappe.get_doc('Coin',exists)
                exists.rank=int(coin['rank'])
                exists.usd_price = coin['price_usd']
                exists.zar_price = coin['price_zar']
                exists.save()

    if frappe.utils.time_diff_in_seconds(frappe.utils.now(),last_run.last_polled)>10:
        coins = frappe.get_all('Coin')
        for coin in coins:
            exists = frappe.get_doc('Coin',coin['name'])
            api_url = "https://min-api.cryptocompare.com/data/price?fsym={0}&tsyms=USD,ZAR".format(exists.symbol)
            response = requests.get(api_url)
            r= json.loads(response.text)
            #return r["USD"]
            try:
                exists.usd_price = r["USD"]
                exists.zar_price = r["ZAR"]
            except:
                exists.usd_price = 0
                exists.zar_price = 0
            exists.save()

            last_run.last_polled=frappe.utils.now()
            last_run.save()
            frappe.db.commit()

        wallets = frappe.get_all('Wallet')
        for w in wallets:
            wallet = frappe.get_doc('Wallet', w['name'])
            wallet.profit_or_loss = 0
            wallet.total = 0
            wallet.total_coins = 0
            wallet.user = wallet.owner
            for line in wallet.transactions:
                line.profit_or_loss=0
                wallet.total_coins = wallet.total_coins + line.quantity
                coin = frappe.get_doc('Coin', line.coin)
                if coin:
                    wallet.total = wallet.total + line.spent
                    if line.quantity >0:
                    line.profit_or_loss = (coin.zar_price*line.quantity) - line.spent
                    wallet.profit_or_loss = wallet.profit_or_loss + line.profit_or_loss
                line.save()
            wallet.save()
            frappe.db.commit()

    return last_run.last_polled