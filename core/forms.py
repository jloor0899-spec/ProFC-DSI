from django import forms
from .models import Cliente, Producto, Proveedor, Venta, DetalleVenta

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cedula_ruc', 'nombre', 'direccion', 'telefono', 'correo']

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'presentacion', 'fecha_vencimiento', 'precio', 'stock', 'proveedor']

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nif', 'nombre', 'ciudad', 'telefono', 'direccion']

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad']
