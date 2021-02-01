from buycoins.client import BuyCoinsClient
from buycoins.errors import check_response
from buycoins.exceptions import AccountError, ClientError


class NGNT(BuyCoinsClient):
    """The NGNT class handles the generations of virtual bank deposit account.
    """

    def createDepositAccount(self, accountName: str):
        """Creates a virtual deposit account under the supplied name.

        Args:
            accountName (str): Name of the new virtual deposit account to be generated*.

        Returns:
            response: A JSON object containing the response from the request.

        """

        if not accountName:
            return AccountError("Invalid account name passed", 404).response

        self.accountName = accountName

        __variables = {
            "accountName": self.accountName
        }

        self.__query = """
            mutation createDepositAccount($accountName: String!) {
                createDepositAccount(accountName: $accountName) {
                    accountNumber
                    accountName
                    accountType
                    bankName
                    accountReference
              }
            }
        """
        try:
            response = self._execute_request(query=self.__query, variables=__variables)
        except (AccountError, ClientError) as e:
            return e.response
        else:
            if not check_response(AccountError, response, 404):
                return response["data"]["createDepositAccount"]
            return check_response(AccountError, response, 404)