from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from decimal import Decimal

from .models import Cliente, Producto, Proveedor, Venta, DetalleVenta
from .forms import ClienteForm, ProductoForm, ProveedorForm


# ===== INICIO =====
def inicio(request):
    return render(request, 'core/inicio.html')


# ===== CLIENTES =====
def clientes(request):
    clientes_list = Cliente.objects.all()
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente registrado')
            return redirect('clientes')
    else:
        form = ClienteForm()

    return render(request, 'core/clientes.html', {
        'form': form,
        'clientes': clientes_list
    })


def editar_cliente(request, cedula):
    cliente = get_object_or_404(Cliente, cedula_ruc=cedula)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado')
            return redirect('clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'core/editar_cliente.html', {'form': form})


def eliminar_cliente(request, cedula):
    cliente = get_object_or_404(Cliente, cedula_ruc=cedula)

    if Venta.objects.filter(cliente=cliente).exists():
        messages.error(request, 'No se puede eliminar un cliente con facturas')
    else:
        cliente.delete()
        messages.success(request, 'Cliente eliminado')

    return redirect('clientes')


# ===== PRODUCTOS =====
def productos(request):
    productos_list = Producto.objects.all()
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto registrado')
            return redirect('productos')
    else:
        form = ProductoForm()

    return render(request, 'core/productos.html', {
        'form': form,
        'productos': productos_list
    })


def editar_producto(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado')
            return redirect('productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'core/editar_producto.html', {'form': form})


def eliminar_producto(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)

    if DetalleVenta.objects.filter(producto=producto).exists():
        messages.error(request, 'No se puede eliminar un producto vendido')
    else:
        producto.delete()
        messages.success(request, 'Producto eliminado')

    return redirect('productos')


# ===== PROVEEDORES =====
def proveedores(request):
    proveedores_list = Proveedor.objects.all()
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor registrado')
            return redirect('proveedores')
    else:
        form = ProveedorForm()

    return render(request, 'core/proveedores.html', {
        'form': form,
        'proveedores': proveedores_list
    })


def editar_proveedor(request, nif):
    proveedor = get_object_or_404(Proveedor, nif=nif)

    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado')
            return redirect('proveedores')
    else:
        form = ProveedorForm(instance=proveedor)

    return render(request, 'core/editar_proveedor.html', {'form': form})


def eliminar_proveedor(request, nif):
    proveedor = get_object_or_404(Proveedor, nif=nif)

    if Producto.objects.filter(proveedor=proveedor).exists():
        messages.error(request, 'No se puede eliminar proveedor con productos')
    else:
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado')

    return redirect('proveedores')


# ===== FACTURACIÓN =====
@transaction.atomic
def facturacion(request):
    carrito = request.session.get('carrito', [])
    cliente = None
    cedula = request.POST.get('cedula') or request.session.get('cedula')

    if request.method == 'POST' and 'buscar_cliente' in request.POST:
        try:
            cliente = Cliente.objects.get(cedula_ruc=cedula)
            request.session['cedula'] = cedula
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente no encontrado')

    if request.method == 'POST' and 'agregar_producto' in request.POST:
        producto = Producto.objects.get(id_producto=request.POST['producto'])
        cantidad = int(request.POST['cantidad'])

        cantidad_carrito = sum(
            i['cantidad'] for i in carrito if i['producto_id'] == producto.id_producto
        )

        if cantidad + cantidad_carrito > producto.stock:
            messages.error(request, f'Stock insuficiente ({producto.stock})')
            return redirect('facturacion')

        for item in carrito:
            if item['producto_id'] == producto.id_producto:
                item['cantidad'] += cantidad
                break
        else:
            carrito.append({
                'producto_id': producto.id_producto,
                'nombre': producto.nombre,
                'precio': float(producto.precio),
                'cantidad': cantidad
            })

        request.session['carrito'] = carrito
        return redirect('facturacion')

    if request.method == 'POST' and 'eliminar_producto' in request.POST:
        carrito = [i for i in carrito if i['producto_id'] != int(request.POST['producto_id'])]
        request.session['carrito'] = carrito
        return redirect('facturacion')

    if request.method == 'POST' and 'guardar_venta' in request.POST:
        if not cedula or not carrito:
            messages.error(request, 'Datos incompletos')
            return redirect('facturacion')

        cliente = Cliente.objects.get(cedula_ruc=cedula)
        venta = Venta.objects.create(
            fecha=timezone.now().date(),
            cliente=cliente,
            subtotal=0,
            iva=0
        )

        subtotal = Decimal('0.00')

        for item in carrito:
            producto = Producto.objects.get(id_producto=item['producto_id'])
            if item['cantidad'] > producto.stock:
                messages.error(request, 'Stock insuficiente')
                return redirect('facturacion')

            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=item['cantidad'],
                precio=item['precio']
            )

            producto.stock -= item['cantidad']
            producto.save()

            subtotal += Decimal(item['precio']) * item['cantidad']

        venta.subtotal = subtotal
        venta.iva = subtotal * Decimal('0.15')
        venta.save()

        request.session['carrito'] = []
        request.session.pop('cedula', None)

        messages.success(request, 'Factura guardada')
        return redirect('facturacion')

    subtotal = sum(Decimal(i['precio']) * i['cantidad'] for i in carrito)

    return render(request, 'core/facturacion.html', {
        'clientes': Cliente.objects.all(),
        'productos': Producto.objects.all(),
        'carrito': carrito,
        'cliente': cliente,
        'cedula': cedula,
        'subtotal': subtotal,
        'iva': subtotal * Decimal('0.15'),
        'total': subtotal * Decimal('1.15')
    })


# ===== FACTURAS =====
def facturas(request):
    ventas = Venta.objects.select_related('cliente').order_by('-id_venta')
    return render(request, 'core/facturas.html', {'ventas': ventas})


def factura_detalle(request, id_venta):
    venta = get_object_or_404(Venta, id_venta=id_venta)
    detalles = DetalleVenta.objects.filter(venta=venta)
    total = venta.subtotal + venta.iva

    return render(request, 'core/factura_detalle.html', {
        'venta': venta,
        'detalles': detalles,
        'total': total
    })
