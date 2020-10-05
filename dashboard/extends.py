from bunq.sdk.model.core.bunq_model import BunqModel
from bunq.sdk.json import converter

# Extends the endpoint.Events docstring
EVENTS_DOCSTRING = """
:param _additional_transaction_information: return additional transaction information
:type _additional_transaction_information: object_.AdditionalTransactionInformation
"""


# Custom function to add to endpoints.Event of bunq_sdk
@property
def additional_transaction_information(self):
    """
    :rtype: object_.AdditionalTransactionInformation
    """

    return self._additional_transaction_information


# Custom class to add to the object_ file of bunq_sdk
class AdditionalTransactionInformation(BunqModel):
    """
    :param _category: Category of payment
    :type _category: str
    """

    _category = None

    @property
    def category(self):
        """
        :rtype: str
        """
        return self._category

    def is_all_field_none(self):
        """
        :rtype: bool
        """
        if self._category is not None:
            return False

        return True

    @staticmethod
    def from_json(json_str):
        """
        :type json_str: str

        :rtype: AdditionalTransactionInformation
        """

        return converter.json_to_class(AdditionalTransactionInformation, json_str)
