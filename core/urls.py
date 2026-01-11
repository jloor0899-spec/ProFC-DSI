from django.urls import path
from . import views

urlpatterns = [
    # INICIO
    path('', views.inicio, name='inicio'),

    # CLIENTES
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/editar/<str:cedula>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<str:cedula>/', views.eliminar_cliente, name='eliminar_cliente'),

    # PROVEEDORES
    path('proveedores/', views.proveedores, name='proveedores'),
    path('proveedores/editar/<str:nif>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<str:nif>/', views.eliminar_proveedor, name='eliminar_proveedor'),

    # PRODUCTOS
    path('productos/', views.productos, name='productos'),
# PRODUCTOS
    path('productos/editar/<int:id_producto>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id_producto>/', views.eliminar_producto, name='eliminar_producto'),


    # FACTURACIÓN
    path('facturacion/', views.facturacion, name='facturacion'),
    path('facturas/', views.facturas, name='facturas'),
    path('factura/<int:id_venta>/', views.factura_detalle, name='factura_detalle'),
]
