CREATE TABLE invoice
(
    id      VARCHAR(36) NOT NULL,
    date    DATE        NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE invoiceitem
(
    id              VARCHAR(36)     NOT NULL,
    invoice_id      VARCHAR(36)     NOT NULL,
    units           INTEGER         NOT NULL,
    description     TEXT            NOT NULL,
    amount          NUMERIC(8, 2)   NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (invoice_id) REFERENCES invoice (id)
);