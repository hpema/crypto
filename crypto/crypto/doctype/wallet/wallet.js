// Copyright (c) 2017, Hemant Pema and contributors
// For license information, please see license.txt

cur_frm.add_fetch('coin', 'zar_price', 'zar_price');

frappe.ui.form.on('Wallet', {
	refresh: function(frm) {
		
	}
});
