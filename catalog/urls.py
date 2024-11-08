from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_admin, name='home'),
   
    path('edit_request', views.edit_request, name='edit_request'),

    path('statistics',  views.statistics, name='statistics'),
    path('sales',  views.sales_of_item, name='sales'),
    
    path('items', views.list_item, name='lists_item'),
    path('fabrics', views.list_fabric, name='lists_fabric'),
    path('suppliers', views.list_supplier, name='lists_supplier'),
    path('customers', views.list_customer, name='lists_customer'),
    path('receipts', views.list_receipt, name='lists_receipt'),

    path('items/new', views.CreateItemView.as_view(), name='new_lists'),
    path('edit_item/<int:pk>/', views.UpdateItemView.as_view(), name='edit_item'),
    path('delete_item/<int:pk>/', views.DeleteItemView.as_view(), name='delete_item'),

    path('customer/new', views.CreateCustomerView.as_view(), name='new_customer'),
    path('customer/new_account', views.CreateCustomer2View.as_view(), name='new_customer_account'),
    path('edit_customer/<int:pk>/', views.UpdateCustomerView.as_view(), name='edit_customer'),
    path('edit_my_profile/<int:pk>/', views.UpdateCustomer2View.as_view(), name='edit_my_profile'),
    path('delete_customer/<int:pk>/', views.DeleteCustomerView.as_view(), name='delete_customer'),

    path('fabric/new', views.CreateFabricView.as_view(), name='new_fabric'),
    path('edit_fabric/<int:pk>/', views.UpdateFabricView.as_view(), name='edit_fabric'),
    path('delete_fabric/<int:pk>/', views.DeleteFabricView.as_view(), name='delete_fabric'),

    path('supplier/new', views.CreateSupplierView.as_view(), name='new_supplier'),
    path('edit_supplier/<int:pk>/', views.UpdateSupplierView.as_view(), name='edit_supplier'),
    path('delete_supplier/<int:pk>/', views.DeleteSupplierView.as_view(), name='delete_supplier'),

    path('receipt/new', views.CreateReceiptView.as_view(), name='new_receipt'),
    path('edit_receipt/<int:pk>/', views.UpdateReceiptView.as_view(), name='edit_receipt'),
    path('delete_receipt/<int:pk>/', views.DeleteReceiptView.as_view(), name='delete_receipt'),

]
