import os
import logging
from unittest import TestCase
from tests.factories import AccountFactory
from service.common import status  # HTTP Status Codes
from service.models import db, Account, init_db
from service.routes import app


DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)

BASE_URL = "/accounts"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestErrorHanlders(TestCase):
    """Error HanldersTests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()  # ✅ This is what was missing
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
    
    ###################################################################
    #  ERROR HANLDER   T E S T   C A S E S
    ######################################################################
    
    def test_data_validation_error(self):
        """It should trigger DataValidationError and return 400"""
        # Send incomplete payload to trigger KeyError inside deserialize
        response = self.client.post(
            BASE_URL, json={"email": "invalid@test.com"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_method_not_allowed(self):
        """It should trigger 405 Method Not Allowed"""
        # POST is allowed, but PUT without an account ID is not (on /accounts)
        response = self.client.put(BASE_URL)  # PUT without /<id> will trigger 405
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

                # POST is allowed, but PUT without an account ID is not (on /accounts)
        response = self.client.delete(BASE_URL)  # PUT without /<id> will trigger 405
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
       
