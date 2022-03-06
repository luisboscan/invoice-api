import uuid
from datetime import datetime
from decimal import Decimal

from flask import Blueprint, request, jsonify

from lib import jsonschemas
from lib.error import errorcodes
from lib.error.apierrors import InvalidRequestApiError, ApiError
from lib.error.errors import NotFoundError
from lib.models import Invoice, InvoiceItem
from lib.repositories import InvoiceRepository, InvoiceItemRepository
from lib.validation import validate_schema

api = Blueprint('api', __name__)


@api.route("/invoices", methods=['GET'])
def get_invoices():
    invoices = InvoiceRepository.get_all()
    response = [invoice.to_json() for invoice in invoices]
    return jsonify(response)


@api.route("/invoices", methods=['POST'])
def create_invoice():
    request_body = request.json
    validate_schema(request_body, jsonschemas, 'create_invoice')
    date = request_body['date']
    try:
        parsed_date = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise InvalidRequestApiError(reasons=[ApiError(
            code=errorcodes.invalid_value.code,
            message=f"'{date}' is not a valid value for date format YYYY-MM-DD",
            path=['date']
        )])
    invoice = Invoice(
        id=str(uuid.uuid4()),
        date=parsed_date,
    )
    InvoiceRepository.save(invoice)
    return jsonify(invoice.to_json())


@api.route("/invoices/<invoice_id>", methods=['GET'])
def get_invoice(invoice_id: str):
    invoice = InvoiceRepository.get_by_id(invoice_id)
    return jsonify(invoice.to_json())


@api.route("/invoices/<invoice_id>/items", methods=['GET'])
def get_invoice_items(invoice_id: str):
    invoice = InvoiceRepository.find_by_id(invoice_id)
    if invoice is None:
        raise NotFoundError
    invoice_items = InvoiceItemRepository.get_all_by_invoice_id(invoice_id=invoice_id)
    response = [invoice_item.to_json() for invoice_item in invoice_items]
    return jsonify(response)


@api.route("/invoices/<invoice_id>/items", methods=['POST'])
def add_invoice_item(invoice_id: str):
    request_body = request.json
    validate_schema(request_body, jsonschemas, 'add_invoice_item')
    invoice = InvoiceRepository.find_by_id(invoice_id)
    if invoice is None:
        raise NotFoundError
    invoice_item = InvoiceItem(
        id=str(uuid.uuid4()),
        invoice_id=invoice_id,
        units=request_body['units'],
        description=request_body['description'],
        amount=Decimal(request_body['amount']),
    )
    InvoiceItemRepository.save(invoice_item)
    return jsonify(invoice_item.to_json())


@api.route("/invoices/<invoice_id>/items/<item_id>", methods=['GET'])
def get_invoice_item(invoice_id: str, item_id: str):
    invoice = InvoiceRepository.find_by_id(invoice_id)
    if invoice is None:
        raise NotFoundError
    invoice_item = InvoiceItemRepository.get_by_invoice_id_and_item_id(invoice_id=invoice_id, item_id=item_id)
    return jsonify(invoice_item.to_json())
