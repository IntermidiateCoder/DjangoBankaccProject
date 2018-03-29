from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import time
import sys
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from .models import *


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'introduction_page'

	def get_queryset(self):
		"""Return the last five published questions."""
		pass

class RegisterView(generic.ListView):
	model = User
	template_name = 'polls/register.html'


def add_user_db(request):
	try:
		if User.objects.filter(username=request.POST['username']).exists():
			return render(request, 'polls/register.html', {
			'error_message': "Name taken!",
			})
			user.delete()
		elif User.objects.filter(email=request.POST['email']).exists():
			return render(request, 'polls/register.html', {
			'error_message': "Email taken!",
			})
			user.delete()
		else:
			user = User.objects.create_user(request.POST['username'], request.POST['email'],
			request.POST['password'])
			user.first_name = request.POST['first_name']
			user.last_name = request.POST['last_name']

	except(KeyError, Choice.DoesNotExist):
		return render(request, 'polls/register.html', {
			'error_message': "You didn't fill the form correctly.",
			})
		user.delete()
	else:
		user.save()
		user.balance_set.create()
		user.save()
		return HttpResponseRedirect(reverse('polls:login'))

@login_required
def my_view(request):
	myuser = request.user
	myuser_balance = Balance.objects.filter(owner=myuser)
	preview_balance = str(myuser_balance.get()) + "₪"
	preview_name = myuser.first_name + " " + myuser.last_name
	preview_email = myuser.email
	return render(request, 'polls/myview.html', {
		'name': preview_name,
		'balance': preview_balance,
		'email': preview_email,
		})

@login_required
def income(request):
	return render(request, 'polls/income.html', {
		'income_types': Category.objects.all()
		})

@login_required
def log_basic(request):
	myuser = request.user
	myuser_logs = Log.objects.filter(owner=myuser)
	return render(request, 'polls/log_basic.html', {
		'logs': myuser_logs
		})

@login_required
def past_trans(request):
	myuser = request.user
	myuser_logs = Log.objects.filter(owner=myuser)
	return render(request, 'polls/past_trans.html', {
		'logs': myuser_logs
		})

@login_required
def iograph(request):
	myuser = request.user
	myuser_logs = Log.objects.filter(owner=myuser)
	return render(request, 'polls/iograph.html', {
		'logs': myuser_logs
		})

@login_required
def balancegraph(request):
	myuser = request.user
	myuser_logs = Log.objects.filter(owner=myuser)
	return render(request, 'polls/balancegraph.html', {
		'logs': myuser_logs
		})

@login_required
def tweakbalance(request):
	amount = int(request.POST['amount'])
	type_of_trans="Income"
	if(request.POST['signofmoney'] == 'outcome'):
			amount *= -1
			type_of_trans="Outcome"
	myuser = request.user
	myuser_balance = Balance.objects.filter(owner=myuser).get()
	myuser_balance.balance = int(myuser_balance.balance) + int(amount)
	myuser_balance.save()
	myuser.save()
	history_name = time.strftime("%x") + " " + type_of_trans + ", " + request.POST['category']
	"""Add transaction to history log"""
	myuser.log_set.create(balance = myuser_balance.balance, history_name=history_name, category=request.POST['category'], income_or_outcome=type_of_trans, amount=amount)
	return HttpResponseRedirect(reverse('polls:income'), {'success': True})

@login_required
def history_log(request):
	myuser = request.user
	myuser_logs = Log.objects.filter(owner=myuser)
	return render(request, 'polls/logs.html', {
		'logs': myuser_logs
		})

class TransactionsView(BaseLineChartView):
	def get_labels(self):
		"""Return 7 labels for the x-axis."""
		myuser = self.request.user
		myuser_logs = Log.objects.filter(owner=myuser)
		income = [log.amount for log in myuser_logs if log.income_or_outcome == 'Income']
		outcome = [-1 * log.amount for log in myuser_logs if log.income_or_outcome == 'Outcome']
		
		transactions = max(len(income), len(outcome)) 
		return [i for i in range(1, transactions+1)]

	def get_providers(self):
		"""Return names of datasets."""
		return ["Income", "Expenses"]

	def get_data(self):
		"""Return 3 datasets to plot."""
		myuser = self.request.user
		myuser_logs = Log.objects.filter(owner=myuser)
		income = [log.amount for log in myuser_logs if log.income_or_outcome == 'Income']
		outcome = [-1 * log.amount for log in myuser_logs if log.income_or_outcome == 'Outcome']
		
		return [income,
				outcome]

class BalanceView(BaseLineChartView):
	def get_labels(self):
		"""Return 7 labels for the x-axis."""
		myuser = self.request.user
		myuser_logs = Log.objects.filter(owner=myuser)
		income = [log.amount for log in myuser_logs if log.income_or_outcome == 'Income']
		outcome = [-1 * log.amount for log in myuser_logs if log.income_or_outcome == 'Outcome']
		
		transactions = len(income)+  len(outcome) 
		return [i for i in range(1, transactions+1)]

	def get_providers(self):
		"""Return names of datasets."""
		return ["Balance"]

	def get_data(self):
		"""Return 3 datasets to plot."""
		myuser = self.request.user
		myuser_logs = Log.objects.filter(owner=myuser)
		balance = [log.balance for log in myuser_logs]
		
		return [balance]