from django.shortcuts import render, redirect
from django.contrib import messages
from odoo_visuals.forms import UserLogin
from odoorpc import ODOO
from .odoo import Odoo
from . import config
import sys

# Create your views here.
odoo = None

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
    return render(request, 'odoo_visuals/dashboard.html', context_dict)
