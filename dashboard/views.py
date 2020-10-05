# Django imports
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.forms import modelformset_factory
from django.db.models import Sum
from django.conf import settings as django_settings

# Other imports
from djmoney.money import Money

# App imports
from dashboard.forms import SignUpForm, LoginForm, UserForm, SettingsForm, MonetarySettings
from dashboard.services import BunqAPI
from dashboard.models import MonetaryAccounts
import time

class TestView(View):
    def get(self, request):
        time.sleep(10)
        return JsonResponse({"result": "test"})


class LoginView(View):
    """
    Login class that handles get and post requests.
    Logs a user in if the proper credentials are filled.
    """

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        # Check if the form is filled correctly
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            # If a user is returned grant authentication
            if user is not None:
                login(request, user)
                return redirect('home')

            # Return with a auth failed message
            auth_failed = True
            return render(request, 'login.html', {'form': form, 'auth_failed': auth_failed})

        # Return with a message something went wront
        form_not_valid = True
        return render(request, 'login.html', {'form': form, 'form_not_valid': form_not_valid})


class RegisterView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')

        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
        else:
            success = False
        return render(request, 'register.html', {'form': form, 'success': success})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request):
        user = self.request.user
        return render(request, self.template_name, {'user': user})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AccountsView(View):

    def get(self, request):
        user = request.user
        monetary_accounts = MonetaryAccounts.objects.filter(user_id=user.id, active=1)
        total_accounts = monetary_accounts.count()
        total_amount = Money(
            monetary_accounts.aggregate(Sum('balance')
        )['balance__sum'], django_settings.DEFAULT_CURRENCY)

        context = {
            'monetary_accounts': monetary_accounts,
            'total_accounts': total_accounts,
            'total_amount': total_amount
        }
        return render(request, 'accounts.html', context)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TransactionsView(View):

    def get(self, request):
        return render(request, 'transactions.html')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class CategoryView(View):

    def get(self, request):
        return render(request, 'category.html')


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SavingsView(View):
    template_name = 'savings.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class SettingsView(View):
    template_name = 'settings.html'
    prefix_user_form = 'user'
    prefix_settings_form = 'settings'

    def get(self, request):
        user = request.user
        user_form = UserForm(
            instance=user,
            prefix=self.prefix_user_form
        )
        settings_form = SettingsForm(
            instance=user.settings,
            prefix=self.prefix_settings_form
        )

        # Create accounts dictionary containing the id and the description
        accounts = {}
        accounts_objects = MonetaryAccounts.objects.filter(user_id=user.id)
        for objects in accounts_objects:
            accounts[objects.id] = objects.description

        # Create the modelformset_factory where all accounts of a user are generated
        monetary_formset = modelformset_factory(MonetaryAccounts, form=MonetarySettings, extra=0)
        monetary_form = monetary_formset(queryset=MonetaryAccounts.objects.filter(user_id=user.id))

        # Create context to render the template properly
        context = {
            'user_form': user_form,
            'settings_form': settings_form,
            'monetary_form': monetary_form,
            'accounts': accounts,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # Set user form
        user_form = UserForm(
            request.POST,
            instance=request.user,
            prefix=self.prefix_user_form
        )

        # Set settings form
        settings_form = SettingsForm(
            request.POST,
            instance=request.user.settings,
            prefix=self.prefix_settings_form
        )

        # Set monetary formset
        monetary_formset = modelformset_factory(
            MonetaryAccounts,
            form=MonetarySettings,
            extra=0
        )
        monetary_form = monetary_formset(
            request.POST,
            queryset=MonetaryAccounts.objects.filter(
                user_id=request.user.id
            )
        )

        # Save forms if forms are valid
        if user_form.is_valid():
            user_form.save()
        if settings_form.is_valid():
            settings_form.save()
        if monetary_form.is_valid():
            monetary_form.save()

        return redirect('settings')
