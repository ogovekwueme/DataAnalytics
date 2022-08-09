from django.shortcuts import render, redirect
from django.contrib import messages
from odoo_visuals.forms import UserLogin
from odoorpc import ODOO
from .odoo import Odoo
from django_pandas import DataFrame
from . import config
import sys
from datetime import datetime, date, timedelta



# Create your views here.
odoo = None

def customer_report(sales, period='overall'):
    overall = '2018-01-01'
    year = date.today().year
    month = date.today().month
    if period == 'year':
        ud = date(year, 1, 1)
        used_date = ud.strftime('%Y-%m-%d')
    elif period =='Month':
        ud = date(year, month, 1)
        used_date =ud.strftime('%Y-%m-%d')
    elif period == 'week':
        today = date.today()
        weekday = today.weekday
        if weekday > 0:
            mon = today - timedelta(days=weekday)
            used_date = mon.strftime('%Y-%m-%d')
    else:
        used_date = overall
    search_sales = sales.search(['|',('state','=','done'), ('state','=','sale'), ('date_order','>=',used_date)])
    if search_sales:
        names = {}
        for sale in search_sales:
            info = sales.browse(sale)
            names[info.partner_id.name] = names.get(info.partner_id.name, 0) + info.amount_total

    return names

def product_report(sales_lines, period='overall'):
    overall = '2018-01-01'
    year = date.today().year
    month = date.today().month
    if period == 'year':
        ud = date(year, 1, 1)
        used_date = ud.strftime('%Y-%m-%d')
    elif period == 'month':
        ud = date(year, month, 1)
        used_date = ud.strftime('%Y-%m-%d')
    else:
        used_date = overall

    all_prods = sales_lines.search([('create_date','>=',used_date)])
    names = {}
    categories = {}
    prices = {}
    for line in all_prods:
      try:
        #print(line)
        info = sales_lines.browse(line)
        if info.order_id.state == 'sale' or info.order_id.state == 'done':
            #print(info.name, info.product_uom_qty)
            names[info.name] = names.get(info.name, 0) + info.product_uom_qty
            categories[info.product_id.categ_id.name] = categories.get(info.product_id.categ_id.name, 0) + 1
            prices[info.product_id.categ_id.name] = prices.get(info.product_id.categ_id.name, 0) + info.price_total
      except:
        print(sys.exc_info())
        continue
    return names, categories, prices

def index(request):
    global odoo
    form =UserLogin()
    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try: 
                odoo = Odoo(config.host, config.port, config.db, email, password)
                user = odoo.get_user()
                request.session['user'] = user.name
                messages.success(request, 'You have successfully logged in')
                return redirect('dashboard')
            except:
                print('Error:', sys.exc_info())
                messages.error(request, 'Cannot log into Odoo ERP, please try again.')
        else:
            messages.error(request, 'Something is wrong with the form, please re-try.')
    return render(request, 'odoo_visuals/index.html', {'form': form})


def logout(request):
    del request.session['user']
    return render(request, 'odoo_visuals/index.html')

def dashboard(request):
    global odoo
    context_dict = {}
    if request.session['user']:
        context_dict['user'] = request.session.get('user')
        sales = odoo.get_sales()
        overall_report = customer_report(sales)
        sorted_os = sorted(overall_sales, reverse=True)[:30] # first 30 names
        values = map(lambda x: overall_sales[x], sorted_os)
        context_dict['names'] = sorted_os
        context_dict['values'] = values
    return render(request, 'odoo_visuals/dashboard.html', context_dict)


def customers(request):
        pass
