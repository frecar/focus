# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from app.invoices.form import InvoiceForm
from app.orders.models import  Offer, Invoice, ProductLine
from django.utils.translation import ugettext as _
from app.stock.models import Product
from core import Core
from core.decorators import require_permission, login_required

@require_permission("LIST", Invoice)
def overview(request):
    offers = Core.current_user().get_permitted_objects("VIEW", Invoice).filter(trashed=False)
    return render(request, "invoices/overview.html", {'title': _('Invoices'),
                                                      'invoices': offers})


@require_permission("VIEW", Invoice, "id")
def view(request, id):
    invoice = Invoice.all_objects.get(id=id)
    return render(request, "invoices/view.html", {'title': invoice.title,
                                                  'invoice': invoice})


@require_permission("CREATE", Invoice)
def add(request):
    return form(request)


@require_permission("EDIT", Invoice, "id")
def edit(request, id):
    return form(request, id)


@login_required()
def form(request, id=None):
    products = []

    if id:
        instance = get_object_or_404(Invoice, id=id)
        products.extend(instance.product_lines.all())
        invoice_number = instance.invoice_number

    else:
        instance = Invoice()
        invoice_number = Invoice.calculate_next_invoice_number()

    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=instance)
        products = []

        i = 0
        for p in request.POST.getlist('product_number'):
            p = ProductLine()
            p.description = request.POST.getlist('product_description')[i]
            p.price = request.POST.getlist('product_unit_cost')[i]
            p.count = request.POST.getlist('product_qty')[i]

            try:
                product = Product.objects.get(id=int(request.POST.getlist('product_number')[i]))
                p.product = product
            except:
                p.product = None

            products.append(p)
            i += 1

        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            o.update_products(products)

            request.message_success(_("Successfully saved offer"))

            return redirect(view, o.id)
    else:
        form = InvoiceForm(instance=instance, initial={'invoice_number': invoice_number})

    return render(request, "invoices/form.html", {'form': form,
                                                'invoice': instance,
                                                'products': products})
