import os
import pathlib
import socket
import warnings

# Django imports
from django.conf import settings as django_settings

# Django related imports
from djmoney.money import Money

# Bunq imports
from bunq.sdk.context.bunq_context import ApiContext, BunqContext
from bunq.sdk.context.api_environment_type import ApiEnvironmentType
from bunq.sdk.http.pagination import Pagination
from bunq.sdk.model.generated import endpoint, object_

# Import override/extend functions. This has to be imported as last.
from dashboard import extends
from dashboard.models import Settings, MonetaryAccounts
from dashboard.exceptions import BunqBudgetInvalidEnvironmentException

# Patch the bunq_sdk with the classes and functions from extends
object_.AdditionalTransactionInformation = extends.AdditionalTransactionInformation
endpoint.Event.__doc__ = endpoint.Event.__doc__ + extends.EVENTS_DOCSTRING
endpoint.Event._additional_transaction_information = None
endpoint.Event.additional_transaction_information = extends.additional_transaction_information


class BunqAPI():
    """
    """

    def __init__(self, user):
        """
        Initialize the Bunq API for first use.
        """
        # Remove warnings of the bunq sdk module
        warnings.filterwarnings(action='ignore', module='bunq')

        # Set basic settings to invoke the Bunq API
        self.user = user
        self.settings = Settings.objects.get(user=user)
        self.bunq_api_environment = self.settings.bunq_api_environment
        self.bunq_api_key = self.settings.bunq_api_key
        self.bunq_api_device_description = socket.gethostname()
        self.bunq_api_context_file_path = os.path.join(
            django_settings.BUNQ_API_ROOT_FILE_PATH,
            f'bunq-{self.bunq_api_environment.lower()}.conf'
        )

        # Setup pagination
        self.pagination = Pagination()
        self.pagination.count = 200

        # Determine if the right API context is set
        if self.bunq_api_environment == "SANDBOX":
            self.bunq_api_environment_type = ApiEnvironmentType.SANDBOX
        elif self.bunq_api_environment == "PRODUCTION":
            self.bunq_api_environment_type = ApiEnvironmentType.PRODUCTION
        else:
            raise BunqBudgetInvalidEnvironmentException(
                "Invalid API environment setting. \
                Choose either SANDBOX or PRODUCTION"
            )

        # If the filepath does not exists, initialize the API
        if not pathlib.Path(self.bunq_api_context_file_path).exists():
            # Create ApiContext
            ApiContext.create(
                self.bunq_api_environment_type,
                self.bunq_api_key,
                self.bunq_api_device_description
            ).save(self.bunq_api_context_file_path)

        # Load API context
        self.api_context = ApiContext.restore(self.bunq_api_context_file_path)
        BunqContext.load_api_context(self.api_context)

    @property
    def get_events(self):
        """
        Prepare the app at startup time. Setup the Bunq API for first use
        and always load the BunqContext at startup.
        """

        # Load API context on starting the app
        return endpoint.Event.list(params=self.pagination.url_params_count_only)

    @property
    def get_monetary_accounts(self):
        return endpoint.MonetaryAccount.list(
            params=self.pagination.url_params_count_only
        ).value

    @property
    def get_monetary_accounts_bank(self):
        return endpoint.MonetaryAccountBank.list(
            params=self.pagination.url_params_count_only
        ).value

    @property
    def get_monetary_accounts_joint(self):
        return endpoint.MonetaryAccountJoint.list(
            params=self.pagination.url_params_count_only
        ).value

    @property
    def get_monetary_accounts_savings(self):
        return endpoint.MonetaryAccountSavings.list(
            params=self.pagination.url_params_count_only
        ).value

    def get_iban_from_alias(self, alias):
        for i in alias:
            if i.type_ == 'IBAN':
                return i.value

        return None

    def get_display_names_joint(self, all_co_owner):
        display_name = []
        for owner in all_co_owner:
            display_name.append(owner.alias.display_name)

        return display_name

    def sync_monetary_accounts_bank_to_db(self):
        accounts = self.get_monetary_accounts_bank

        for account in accounts:
            MonetaryAccounts.objects.update_or_create(
                user=self.user,
                monetary_account_id=account.id_,
                monetary_account_type='MB',
                iban=self.get_iban_from_alias(account.alias),
                display_name=account.display_name,
                description=account.description,
                balance=Money(account.balance.value, account.balance.currency),
                status=account.status
            )

    def sync_monetary_accounts_joint_to_db(self):
        accounts = self.get_monetary_accounts_joint

        for account in accounts:
            MonetaryAccounts.objects.update_or_create(
                user=self.user,
                monetary_account_id=account.id_,
                monetary_account_type='MJ',
                iban=self.get_iban_from_alias(account.alias),
                display_name=" / ".join(self.get_display_names_joint(account.all_co_owner)),
                description=account.description,
                balance=Money(account.balance.value, account.balance.currency),
                status=account.status
            )

    def sync_monetary_accounts_savings_to_db(self):
        accounts = self.get_monetary_accounts_savings

        for account in accounts:
            MonetaryAccounts.objects.update_or_create(
                user=self.user,
                monetary_account_id=account.id_,
                monetary_account_type='MS',
                iban=self.get_iban_from_alias(account.alias),
                description=account.description,
                balance=Money(account.balance.value, account.balance.currency),
                savings_goal=Money(account.savings_goal.value, account.savings_goal.currency),
                savings_goal_progress=account.savings_goal_progress,
                status=account.status
            )

    def sync_monetary_accounts(self):
        self.sync_monetary_accounts_bank_to_db()
        self.sync_monetary_accounts_joint_to_db()
        self.sync_monetary_accounts_savings_to_db()
