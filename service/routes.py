"""
Account Service

This microservice handles the lifecycle of Accounts
"""
# pylint: disable=unused-import
from flask import jsonify, request, make_response, abort, url_for   # noqa; F401
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Import Flask application


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
            # paths=url_for("list_accounts", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """
    Creates an Account
    This endpoint will create an Account based the data in the body that is posted
    """
    app.logger.info("Request to create an Account")
    check_content_type("application/json")
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    # Uncomment once get_accounts has been implemented
    # location_url = url_for("get_accounts", account_id=account.id, _external=True)
    location_url = "/"  # Remove once get_accounts has been implemented
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

######################################################################
# LIST ALL ACCOUNTS
######################################################################


@app.route("/accounts", methods=["GET"])
def list_accounts():
    accounts = Account().all()
    data = [account.serialize() for account in accounts]
    location_url = "/accounts"
    return make_response(
        jsonify(data), status.HTTP_200_OK, {"Location": location_url}
    )


######################################################################
# READ AN ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_accounts(account_id):
    """
   Gets an Account
    """
    app.logger.info("Request to get an Account")

    account = Account.find(account_id)
    if account is None:
        abort(status.HTTP_404_NOT_FOUND, f"Account with {account_id} not available")
    location_url = f"/accounts/{account_id}"  # Remove once get_accounts has been implemented
    return make_response(
        jsonify(account.serialize()), status.HTTP_200_OK, {"Location": location_url}
    )

# ... place you code here to READ an account ...


######################################################################
# UPDATE AN EXISTING ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_accounts(account_id):
    account = Account.find(account_id)
    if account is None:
        abort(status.HTTP_404_NOT_FOUND, f"Account with {account_id} not available")
    account.deserialize(request.get_json())  # Parse data from PUT requests
    account.update()
    location_url = f"/accounts/{account_id}"  # Remove once get_accounts has been implemented
    return make_response(
        jsonify(account.serialize()), status.HTTP_200_OK, {"Location": location_url}
    )

######################################################################
# DELETE AN ACCOUNT
######################################################################


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_accounts(account_id):
    account = Account.find(account_id)
    if account is None:
        abort(status.HTTP_404_NOT_FOUND, f"Account with {account_id} not available")
    account.delete()
    location_url = f"/accounts/{account_id}"  # Remove once get_accounts has been implemented
    return make_response(
        jsonify({}), status.HTTP_204_NO_CONTENT, {"Location": location_url}
    )

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
