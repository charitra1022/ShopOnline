from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, Item, Transaction, ClientInfo, PDFInfo
from pyinvoice.templates import SimpleInvoice


# Business Provider details
providerEmail = 'shoponline@gmail.com'
providerName = "ShopOnline Pvt. Ltd."
providerAddress = '1234, MG Road'
providerCity = 'Koramangala, Bangalore'
providerState = 'Karnataka'
providerCountry = 'India'
providerZip = "560034"


# pdf Info
author = "ShopOnline"
subject = "invoice/receipt"


def createInvoice(client_details, txn_details, products, payment_mode):
    """
    :param client_details: Client details (name, email)
    :type client_details: list or tuple

    :param txn_details: transaction details (txn_id, date, amount, tax, invoice_id)
    :type txn_details: list or tuple

    :param products: Products [(title, quantity, unit_price),]
    :type products: list of tuple
    """

    # Customer details come here
    clientName = client_details[0]
    clientEmail = client_details[1]

    # Transaction Details
    txnId = txn_details[0]
    txnDate = txn_details[1]
    amountPaid = txn_details[2]
    tax = txn_details[3]
    invoiceId = txn_details[4]

    # Product details
    items = []
    for product in products:
        prodTitle = product[0]
        prodQuan = product[1]
        prodPrice = product[2]

        n = 30
        chunks = '\n'.join([prodTitle[i:i+n]
                           for i in range(0, len(prodTitle), n)])
        items.append(Item(chunks, prodTitle, prodQuan, prodPrice))

    pdfTitle = str(invoiceId)
    pdfInfo = PDFInfo(title=pdfTitle, author=author, subject=subject)
    doc = SimpleInvoice(f'media/invoice/{invoiceId}.pdf', pdf_info=pdfInfo)

    # Paid stamp
    doc.is_paid = True
    doc.client_info = ClientInfo(
        email=clientEmail,
        name=clientName,
    )
    doc.service_provider_info = ServiceProviderInfo(
        name=providerName,
        street=providerAddress,
        city=providerCity,
        state=providerState,
        country=providerCountry,
        post_code=providerZip,
    )
    [doc.add_item(i) for i in items]

    # Invoice info
    doc.invoice_info = InvoiceInfo(invoiceId, txnDate, txnDate)

    # Tax rate
    doc.set_item_tax_rate(tax)

    # Transactions detail
    doc.add_transaction(Transaction(
        payment_mode.value, txnId, txnDate, amountPaid))
    doc.set_bottom_tip(
        f"Email: {providerEmail}<br />Contact us for any queries.")
    doc.finish()
