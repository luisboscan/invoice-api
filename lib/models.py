from lib.database import db


class Invoice(db.Model):
    __tablename__ = 'invoice'

    id = db.Column(db.String(36), primary_key=True)
    date = db.Column(db.Date, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%Y-%m-%d'),
        }


class InvoiceItem(db.Model):
    __tablename__ = 'invoiceitem'

    id = db.Column(db.String(36), primary_key=True)
    invoice_id = db.Column(db.String, db.ForeignKey(Invoice.id), nullable=False)
    units = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Numeric(precision=8, scale=2), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'invoiceId': self.invoice_id,
            'units': self.units,
            'description': self.description,
            'amount': float(self.amount),
        }
