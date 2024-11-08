import os
from datetime import date, timedelta

from django.contrib import messages
from django.db import connection
from django.db.models import Avg, Count, Max, Min, Q, Subquery, Sum
from django.db.utils import OperationalError
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic import CreateView, DeleteView
from django.views.generic.edit import UpdateView

from .forms import *
from .models import *


def home_admin(request):
    return render(request, 'catalog/HomeAdmin.html')

def sales_of_item(request):
    items = Item.objects.annotate(
        sales_count=Count('receipt'),  # Підрахунок кількості продажів
        sales_total=Sum('receipt__the_item_cost')  # Загальна сума продажів
    )
    context = {'items': items}
    return render(request, 'catalog/ItemsAndSales.html', context)


def edit_request(request):
    result = ''
    error_message = None
    items = Item.objects.all()
    fabrics = Fabric.objects.all()
    suppliers = Supplier.objects.all()
    column_names = []
    if request.method == 'POST':
        form = SQLQueryForm(request.POST)
        if form.is_valid():
            sql_query = form.cleaned_data['sql_query']
            with connection.cursor() as cursor:
                try:
                    cursor.execute(sql_query)  # виконання SQL запиту
                    result = cursor.fetchall()   #витягнути всі строки з результату
                    column_names = [col[0] for col in cursor.description]
                except OperationalError as e:
                    error_message = "Нічого не знайдено"
    else:
        form = SQLQueryForm()

    return render(request, 'catalog/Requests.html',
                  {'items': items, 'fabrics': fabrics, 'suppliers': suppliers, 'form': form, 'result': result,
                   'error_message': error_message, 'column_names': column_names})


def list_item(request):
    items = Item.objects.all()
    sort_form = SortByItem(request.POST or None)
    form = ItemFilterForm(request.GET)
    q_objects = Q()
    if form.is_valid():
        brand_values = form.cleaned_data.get('brand', [])
        size_values = form.cleaned_data.get('size', [])
        gender_values = form.cleaned_data.get('gender', [])
        color_values = form.cleaned_data.get('color', [])
        fabric_values = form.cleaned_data.get('fabric', [])
        chemical_treatment_values = form.cleaned_data.get('chemical_treatment', [])
        state_values = form.cleaned_data.get('state', [])
        seasonality_values = form.cleaned_data.get('seasonality', [])
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        supplier_values = form.cleaned_data.get('supplier', [])
        filters = Q()
        if brand_values:
            filters &= Q(brand__in=brand_values)
        if size_values:
            filters &= Q(size__in=size_values)
        if gender_values:
            filters &= Q(gender__in=gender_values)
        if color_values:
            filters &= Q(color__in=color_values)
        if fabric_values:
            filters &= Q(fabric__in=fabric_values)
        if chemical_treatment_values:
            filters &= Q(chemical_treatment__in=chemical_treatment_values)
        if state_values:
            filters &= Q(state__in=state_values)
        if seasonality_values:
            filters &= Q(seasonality__in=seasonality_values)
        if min_price is not None:
            filters &= Q(price__gte=min_price)
        if max_price is not None:
            filters &= Q(price__lte=max_price)
        if supplier_values:
            filters &= Q(supplier__in=supplier_values)
        q_objects &= filters
    if sort_form.is_valid():
        is_reversed = sort_form.cleaned_data['is_reversed']
        if sort_form.cleaned_data['sort_by'] == 'id_item':
            items = items.order_by(f'{"-" if is_reversed else ""}id_item')
        if sort_form.cleaned_data['sort_by'] == 'type':
            items = items.order_by(f'{"-" if is_reversed else ""}type')
        if sort_form.cleaned_data['sort_by'] == 'brand':
            items = items.order_by(f'{"-" if is_reversed else ""}brand')
        if sort_form.cleaned_data['sort_by'] == 'size':
            items = items.order_by(f'{"-" if is_reversed else ""}size')
        if sort_form.cleaned_data['sort_by'] == 'gender':
            items = items.order_by(f'{"-" if is_reversed else ""}gender')
        if sort_form.cleaned_data['sort_by'] == 'color':
            items = items.order_by(f'{"-" if is_reversed else ""}color')
        if sort_form.cleaned_data['sort_by'] == 'fabric':
            items = items.order_by(f'{"-" if is_reversed else ""}fabric')
        if sort_form.cleaned_data['sort_by'] == 'chemical_treatment':
            items = items.order_by(f'{"-" if is_reversed else ""}chemical_treatment')
        if sort_form.cleaned_data['sort_by'] == 'state':
            items = items.order_by(f'{"-" if is_reversed else ""}state')
        if sort_form.cleaned_data['sort_by'] == 'seasonality':
            items = items.order_by(f'{"-" if is_reversed else ""}seasonality')
        if sort_form.cleaned_data['sort_by'] == 'price':
            items = items.order_by(f'{"-" if is_reversed else ""}price')
        if sort_form.cleaned_data['sort_by'] == 'supplier':
            items = items.order_by(f'{"-" if is_reversed else ""}supplier')
    items = items.filter(q_objects)
    context = {'items': items,
               'sort_form': sort_form,
               'form': form}
    return render(request, 'catalog/tables/table_item.html', context)


def list_fabric(request):
    fabrics = Fabric.objects.all()
    sort_form = SortByFabric(request.POST or None)
    form = FabricFilterForm(request.GET)
    q_objects = Q()
    if form.is_valid():
        destiny_values = form.cleaned_data.get('destiny')
        elasticity_values = form.cleaned_data.get('elasticity')
        breathability_values = form.cleaned_data.get('breathability')
        surface_texture_values = form.cleaned_data.get('surface_texture')
        compression_resistance_values = form.cleaned_data.get('compression_resistance')
        color_fastness_values = form.cleaned_data.get('color_fastness')

        filterss = Q()

        if destiny_values:
            filterss &= Q(destiny__in=destiny_values)
        if elasticity_values:
            filterss &= Q(elasticity__in=elasticity_values)
        if breathability_values:
            filterss &= Q(breathability__in=breathability_values)
        if surface_texture_values:
            filterss &= Q(surface_texture__in=surface_texture_values)
        if compression_resistance_values:
            filterss &= Q(compression_resistance__in=compression_resistance_values)
        if color_fastness_values:
            filterss &= Q(color_fastness__in=color_fastness_values)

        q_objects &= filterss

    if sort_form.is_valid():
        is_reversed = sort_form.cleaned_data['is_reversed']
        if sort_form.cleaned_data['sort_by'] == 'id_fabric':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}id_fabric')
        if sort_form.cleaned_data['sort_by'] == 'fabric_name':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}fabric_name')
        if sort_form.cleaned_data['sort_by'] == 'destiny':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}destiny')
        if sort_form.cleaned_data['sort_by'] == 'elasticity':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}elasticity')
        if sort_form.cleaned_data['sort_by'] == 'breathability':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}breathability')
        if sort_form.cleaned_data['sort_by'] == 'surface_texture':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}surface_texture')
        if sort_form.cleaned_data['sort_by'] == 'compression_resistance':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}compression_resistance')
        if sort_form.cleaned_data['sort_by'] == 'color_fastness':
            fabrics = fabrics.order_by(f'{"-" if is_reversed else ""}color_fastness')
    fabrics = fabrics.filter(q_objects)
    context = {'fabrics': fabrics,
               'sort_form': sort_form,
               'form': form}
    return render(request, 'catalog/tables/table_fabric.html', context)


def list_supplier(request):
    suppliers = Supplier.objects.all()
    sort_form = SortBySupplier(request.POST or None)
    form = SupplierFilterForm(request.GET)
    q_objects = Q()
    if form.is_valid():
        contact_person_name_values = form.cleaned_data.get('contact_person_name', [])
        contact_person_surname_values = form.cleaned_data.get('contact_person_surname', [])
        phone_number_values = form.cleaned_data.get('phone_number', [])
        city_values = form.cleaned_data.get('city', [])
        email_values = form.cleaned_data.get('email', [])
        filters = Q()
        if contact_person_name_values:
            filters &= Q(contact_person_name__in=contact_person_name_values)
        if contact_person_surname_values:
            filters &= Q(contact_person_surname__in=contact_person_surname_values)
        if phone_number_values:
            filters &= Q(phone_number__in=phone_number_values)
        if city_values:
            filters &= Q(city__in=city_values)
        if email_values:
            filters &= Q(email__in=email_values)
        q_objects &= filters
    if sort_form.is_valid():
        is_reversed = sort_form.cleaned_data['is_reversed']
        if sort_form.cleaned_data['sort_by'] == 'id_supplier':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}id_supplier')
        if sort_form.cleaned_data['sort_by'] == 'company_name':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}company_name')
        if sort_form.cleaned_data['sort_by'] == 'contact_person_name':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}contact_person_name')
        if sort_form.cleaned_data['sort_by'] == 'contact_person_surname':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}contact_person_surname')
        if sort_form.cleaned_data['sort_by'] == 'phone_number':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}phone_number')
        if sort_form.cleaned_data['sort_by'] == 'city':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}city')
        if sort_form.cleaned_data['sort_by'] == 'email':
            suppliers = suppliers.order_by(f'{"-" if is_reversed else ""}email')
    suppliers = suppliers.filter(q_objects)
    context = {'suppliers': suppliers,
               'sort_form': sort_form,
               'form': form}
    return render(request, 'catalog/tables/table_supplier.html', context)


def list_customer(request):
    customers = Customer.objects.all()
    sort_form = SortByCustomer(request.POST or None)
    form = CustomerFilterForm(request.GET)
    q_objects = Q()
    if form.is_valid():
        customer_name_values = form.cleaned_data.get('customer_name', [])
        customer_surname_values = form.cleaned_data.get('customer_surname', [])
        customer_middle_name_values = form.cleaned_data.get('customer_middle_name', [])
        customer_city_values = form.cleaned_data.get('customer_city', [])
        customer_address_values = form.cleaned_data.get('customer_address', [])
        customer_number_of_house_values = form.cleaned_data.get('customer_number_of_house', [])
        customer_phone_number_values = form.cleaned_data.get('customer_phone_number', [])
        customer_email_values = form.cleaned_data.get('customer_email', [])
        customer_passport_code_values = form.cleaned_data.get('customer_passport_code', [])
        customer_date_of_birth_values = form.cleaned_data.get('customer_date_of_birth', [])
        customer_password_values = form.cleaned_data.get('customer_password', [])
        customer_credit_card_values = form.cleaned_data.get('customer_credit_card', [])
        filters = Q()
        if customer_name_values:
            filters &= Q(customer_name__in=customer_name_values)
        if customer_surname_values:
            filters &= Q(customer_surname__in=customer_surname_values)
        if customer_middle_name_values:
            filters &= Q(customer_middle_name__in=customer_middle_name_values)
        if customer_city_values:
            filters &= Q(customer_city__in=customer_city_values)
        if customer_address_values:
            filters &= Q(customer_address__in=customer_address_values)
        if customer_number_of_house_values:
            filters &= Q(customer_number_of_house__in=customer_number_of_house_values)
        if customer_phone_number_values:
            filters &= Q(customer_phone_number__in=customer_phone_number_values)
        if customer_email_values:
            filters &= Q(customer_email__in=customer_email_values)
        if customer_passport_code_values:
            filters &= Q(customer_passport_code__in=customer_passport_code_values)
        if customer_date_of_birth_values:
            filters &= Q(customer_date_of_birth__in=customer_date_of_birth_values)
        if customer_password_values:
            filters &= Q(customer_password__in=customer_password_values)
        if customer_credit_card_values:
            filters &= Q(customer_credit_card__in=customer_credit_card_values)
        q_objects &= filters
    if sort_form.is_valid():
        is_reversed = sort_form.cleaned_data['is_reversed']
        if sort_form.cleaned_data['sort_by'] == 'id_customer':
            customers = customers.order_by(f'{"-" if is_reversed else ""}id_customer')
        if sort_form.cleaned_data['sort_by'] == 'customer_name':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_name')
        if sort_form.cleaned_data['sort_by'] == 'customer_surname':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_surname')
        if sort_form.cleaned_data['sort_by'] == 'customer_middle_name':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_middle_name')
        if sort_form.cleaned_data['sort_by'] == 'customer_city':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_city')
        if sort_form.cleaned_data['sort_by'] == 'customer_address':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_address')
        if sort_form.cleaned_data['sort_by'] == 'customer_number_of_house':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_number_of_house')
        if sort_form.cleaned_data['sort_by'] == 'customer_phone_number':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_phone_number')
        if sort_form.cleaned_data['sort_by'] == 'customer_email':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_email')
        if sort_form.cleaned_data['sort_by'] == 'customer_passport_code':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_passport_code')
        if sort_form.cleaned_data['sort_by'] == 'customer_date_of_birth':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_date_of_birth')
        if sort_form.cleaned_data['sort_by'] == 'customer_password':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_password')
        if sort_form.cleaned_data['sort_by'] == 'customer_credit_card':
            customers = customers.order_by(f'{"-" if is_reversed else ""}customer_credit_card')
    customers = customers.filter(q_objects)
    context = {'customers': customers,
               'sort_form': sort_form,
               'form': form}
    return render(request, 'catalog/tables/table_customer.html', context)


def list_receipt(request):
    receipts = Receipt.objects.all()
    sort_form = SortByReceipt(request.POST or None)
    form = ReceiptFilterForm(request.GET)
    q_objects = Q()
    if form.is_valid():
        id_item_values = form.cleaned_data.get('id_item', [])
        id_customer_values = form.cleaned_data.get('id_customer', [])
        date_of_purchase_values = form.cleaned_data.get('date_of_purchase', [])
        method_of_delivery_values = form.cleaned_data.get('method_of_delivery', [])
        payment_type_values = form.cleaned_data.get('payment_type', [])
        min_price = form.cleaned_data.get('min_the_item_cost')
        max_price = form.cleaned_data.get('max_the_item_cost')
        filters = Q()
        if id_item_values:
            filters &= Q(id_item__in=id_item_values)
        if id_customer_values:
            filters &= Q(id_customer__in=id_customer_values)
        if date_of_purchase_values:
            filters &= Q(date_of_purchase__in=date_of_purchase_values)
        if min_price is not None:
            filters &= Q(the_item_cost__gte=min_price)
        if max_price is not None:
            filters &= Q(the_item_cost__lte=max_price)
        if method_of_delivery_values:
            filters &= Q(method_of_delivery__in=method_of_delivery_values)
        if payment_type_values:
            filters &= Q(payment_type__in=payment_type_values)
        q_objects &= filters
    if sort_form.is_valid():
        is_reversed = sort_form.cleaned_data['is_reversed']
        if sort_form.cleaned_data['sort_by'] == 'id_receipt':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}id_receipt')
        if sort_form.cleaned_data['sort_by'] == 'id_item':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}id_item')
        if sort_form.cleaned_data['sort_by'] == 'id_customer':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}id_customer')
        if sort_form.cleaned_data['sort_by'] == 'number_of_receipt':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}number_of_receipt')
        if sort_form.cleaned_data['sort_by'] == 'date_of_purchase':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}date_of_purchase')
        if sort_form.cleaned_data['sort_by'] == 'the_item_cost':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}the_item_cost')
        if sort_form.cleaned_data['sort_by'] == 'method_of_delivery':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}method_of_delivery')
        if sort_form.cleaned_data['sort_by'] == 'payment_type':
            receipts = receipts.order_by(f'{"-" if is_reversed else ""}payment_type')
    receipts = receipts.filter(q_objects)
    context = {'receipts': receipts,
               'sort_form': sort_form,
               'form': form}
    return render(request, 'catalog/tables/table_receipt.html', context)


def statistics(request):
    # Середня ціна речей кожного бренду
    average_price_per_brand = Item.objects.values('brand').annotate(average_price=Avg('price'))
    # Кількість речей кожного бренду
    count_per_brand = Item.objects.values('brand').annotate(count=Count('id_item'))
    # Кількість речей за кожним постачальником
    count_per_supplier = Item.objects.values('supplier__company_name').annotate(count=Count('id_item'))
    # Середня ціна речей кожного постачальника
    average_price_per_supplier = Item.objects.values('supplier__company_name').annotate(average_price=Avg('price'))
    # Постачальники, у яких найбільше поставок
    most_deliveries = count_per_supplier.aggregate(Max('count'))['count__max']
    most_deliveries_suppliers = count_per_supplier.filter(count=most_deliveries)
    # Постачальники, у яких найменше поставок
    least_deliveries = count_per_supplier.aggregate(Min('count'))['count__min']
    least_deliveries_suppliers = count_per_supplier.filter(count=least_deliveries)
    # сума кожного чека
    start_of_last_week = datetime.now() - timedelta(days=datetime.now().weekday() + 7)
    end_of_last_week = start_of_last_week + timedelta(days=6)
    receipt_totals = Receipt.objects.filter(date_of_purchase__range=[start_of_last_week, end_of_last_week]).values(
        'number_of_receipt').annotate(total=Sum('the_item_cost'))
    # Найбільший чек
    biggest_receipt =receipt_totals.aggregate(Max('total'))['total__max']
    biggest_receipts = receipt_totals.filter(total=biggest_receipt)
    # Найменший чек
    smallest_receipt = receipt_totals.aggregate(Min('total'))['total__min']
    smallest_receipts = receipt_totals.filter(total=smallest_receipt)
    # Середня вартість товарів кожного типу тканини
    average_price_per_fabric_type = Item.objects.values('fabric__fabric_name').annotate(average_price=Avg('price'))

    context = {'average_price_per_brand': average_price_per_brand,
               'count_per_brand': count_per_brand,
               'count_per_supplier': count_per_supplier,
               'average_price_per_supplier': average_price_per_supplier,
               'most_deliveries_suppliers': most_deliveries_suppliers,
               'least_deliveries_suppliers': least_deliveries_suppliers,
               'biggest_receipts': biggest_receipts,
               'smallest_receipt': smallest_receipt,
               'smallest_receipts': smallest_receipts,
               'average_price_per_fabric_type': average_price_per_fabric_type,
               'receipt_totals': receipt_totals,
               }
    return render(request, 'catalog/Statistics.html', context)

class CreateItemView(CreateView):
    model = Item
    template_name = "catalog/Forms/add_form.html"
    form_class = ItemForm
    success_url = "/items"


class UpdateItemView(UpdateView):
    model = Item
    template_name = "catalog/Forms/editor_form.html"
    form_class = ItemForm2
    success_url = "/items"


class DeleteItemView(DeleteView):
    model = Item
    template_name = "catalog/Forms/delete_form.html"
    success_url = "/items"


class CreateCustomerView(CreateView):
    model = Customer
    template_name = "catalog/Forms/add_form.html"
    form_class = CustomerForm
    success_url = "/customers"


class CreateCustomer2View(CreateView):
    model = Customer
    template_name = "catalog/Forms/add_account.html"
    form_class = CustomerForm

    def get_success_url(self):
        return reverse('home_client', args=[str(self.object.pk)])


class UpdateCustomerView(UpdateView):
    model = Customer
    template_name = "catalog/Forms/editor_form.html"
    form_class = CustomerForm2
    success_url = "/customers"


class UpdateCustomer2View(UpdateView):
    model = Customer
    template_name = "catalog/users_page/edit_info.html"
    form_class = CustomerForm2

    def get_success_url(self):
        return reverse('home_client', args=[str(self.object.pk)])


class DeleteCustomerView(DeleteView):
    model = Customer
    template_name = "catalog/Forms/delete_form.html"
    success_url = "/customers"


class CreateFabricView(CreateView):  # тканина
    model = Fabric
    template_name = "catalog/Forms/add_form.html"
    fields = "__all__"
    success_url = "/fabrics"


class UpdateFabricView(UpdateView):
    model = Fabric
    template_name = "catalog/Forms/editor_form.html"
    fields = "__all__"
    success_url = "/fabrics"


class DeleteFabricView(DeleteView):
    model = Fabric
    template_name = "catalog/Forms/delete_form.html"
    success_url = "/fabrics"


class CreateSupplierView(CreateView):  # постачальник
    model = Supplier
    template_name = "catalog/Forms/add_form.html"
    form_class = SupplierForm
    success_url = "/suppliers"


class UpdateSupplierView(UpdateView):
    model = Supplier
    template_name = "catalog/Forms/editor_form.html"
    form_class = SupplierForm
    success_url = "/suppliers"


class DeleteSupplierView(DeleteView):
    model = Supplier
    template_name = "catalog/Forms/delete_form.html"
    success_url = "/suppliers"


class CreateReceiptView(CreateView):  # Чеки
    model = Receipt
    template_name = "catalog/Forms/add_form.html"
    form_class = ReceiptForm
    success_url = "/receipts"


class UpdateReceiptView(UpdateView):
    model = Receipt
    template_name = "catalog/Forms/editor_form.html"
    form_class = ReceiptForm2
    success_url = "/receipts"


class DeleteReceiptView(DeleteView):
    model = Receipt
    template_name = "catalog/Forms/delete_form.html"
    success_url = "/receipts"
