# -*- coding: utf-8 -*-
# Copyright (c) 2017, Hemant Pema and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Wallet(Document):
	def validate(self):
		self.profit_or_loss = 0
		self.total = 0
		self.total_coins = 0
		
		for line in self.transactions:
			line.profit_or_loss=0
			self.total_coins = self.total_coins + line.quantity
			coin = frappe.get_doc('Coin', line.coin)
			if coin:
				self.total = self.total + line.spent
				if line.quantity >0:
					line.profit_or_loss = (coin.zar_price*line.quantity) - line.spent
				self.profit_or_loss = self.profit_or_loss + line.profit_or_loss