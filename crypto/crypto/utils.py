import frappe
import requests, json

@frappe.whitelist()
def get_exchange_rate():
    api_url = "https://api.coinmarketcap.com/v1/ticker/?convert=ZAR"
    response = requests.get(api_url)
    print response.text
    return json.loads(response.text)[0]['price_zar']