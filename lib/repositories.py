from typing import List, Optional

from lib.database import db
from lib.error.errors import NotFoundError
from lib.models import Invoice, InvoiceItem


class InvoiceRepository:

    @classmethod
    def get_all(cls) -> List[Invoice]:
        return Invoice.query.all()

    @classmethod
    def find_by_id(cls, invoice_id: str) -> Optional[Invoice]:
        return Invoice.query.filter_by(id=invoice_id).first()

    @classmethod
    def get_by_id(cls, invoice_id: str) -> Invoice:
        result = cls.find_by_id(invoice_id)
        if result is None:
            raise NotFoundError
        return result

    @classmethod
    def save(cls, invoice: Invoice) -> None:
        db.session.add(invoice)
        db.session.commit()


class InvoiceItemRepository:

    @classmethod
    def get_all_by_invoice_id(cls, invoice_id: str) -> List[InvoiceItem]:
        return InvoiceItem.query.filter_by(invoice_id=invoice_id)

    @classmethod
    def find_by_invoice_id_and_item_id(cls, invoice_id: str, item_id: str) -> Optional[InvoiceItem]:
        return InvoiceItem.query.filter_by(invoice_id=invoice_id, id=item_id).first()

    @classmethod
    def get_by_invoice_id_and_item_id(cls, invoice_id: str, item_id: str) -> InvoiceItem:
        result = cls.find_by_invoice_id_and_item_id(invoice_id=invoice_id, item_id=item_id)
        if result is None:
            raise NotFoundError
        return result

    @classmethod
    def save(cls, invoice_item: InvoiceItem) -> None:
        db.session.add(invoice_item)
        db.session.commit()
