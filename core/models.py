from django.db import models


class Cliente(models.Model):
    cedula_ruc = models.CharField(primary_key=True, max_length=13)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    correo = models.EmailField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.cedula_ruc} - {self.nombre}"


class Proveedor(models.Model):
    nif = models.CharField(primary_key=True, max_length=15)
    nombre = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
    presentacion = models.CharField(max_length=50)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha = models.DateField(auto_now_add=True)
    iva = models.DecimalField(max_digits=5, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"Venta {self.id_venta}"



class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('venta', 'producto')


class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    fecha_pago = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    observacion = models.CharField(max_length=100, blank=True)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
