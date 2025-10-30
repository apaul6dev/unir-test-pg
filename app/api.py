import http.client

from flask import Flask
from app.calc import InvalidPermissions
from app import util
from app.calc import Calculator

CALCULATOR = Calculator()
api_application = Flask(__name__)
HEADERS = {"Content-Type": "text/plain", "Access-Control-Allow-Origin": "*"}


def _execute_operation(op_name, op_1, op_2=None):
    """Helper to execute calculator operations and handle errors."""
    try:
        num_1 = util.convert_to_number(op_1)
        if op_2 is not None:
            num_2 = util.convert_to_number(op_2)
            result = getattr(CALCULATOR, op_name)(num_1, num_2)
        else:
            result = getattr(CALCULATOR, op_name)(num_1)
        return ("{}".format(result), http.client.OK, HEADERS)
    except (TypeError, ValueError) as e:
        return (str(e), http.client.BAD_REQUEST, HEADERS)
    except InvalidPermissions as e:
        return (str(e), http.client.FORBIDDEN, HEADERS)


@api_application.route("/")
def hello():
    return "Hello from The Calculator!\n"

@api_application.route("/calc/add/<op_1>/<op_2>", methods=["GET"])
def add(op_1, op_2):
    return _execute_operation("add", op_1, op_2)

@api_application.route("/calc/substract/<op_1>/<op_2>", methods=["GET"])
def substract(op_1, op_2):
    return _execute_operation("substract", op_1, op_2)

@api_application.route("/calc/multiply/<op_1>/<op_2>", methods=["GET"])
def multiply(op_1, op_2):
    return _execute_operation("multiply", op_1, op_2)

@api_application.route("/calc/divide/<op_1>/<op_2>", methods=["GET"])
def divide(op_1, op_2):
    return _execute_operation("divide", op_1, op_2)

@api_application.route("/calc/power/<op_1>/<op_2>", methods=["GET"])
def power(op_1, op_2):
    return _execute_operation("power", op_1, op_2)

@api_application.route("/calc/sqrt/<op_1>", methods=["GET"])
def sqrt(op_1):
    return _execute_operation("sqrt", op_1)

@api_application.route("/calc/log10/<op_1>", methods=["GET"])
def log10(op_1):
    return _execute_operation("log10", op_1)
