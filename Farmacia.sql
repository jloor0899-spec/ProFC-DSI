CREATE TABLE cliente (
    cedula_ruc VARCHAR(13) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    direccion VARCHAR(100),
    telefono VARCHAR(15),
    correo VARCHAR(50)
);

CREATE TABLE venta (
    id_venta SERIAL PRIMARY KEY,
    fecha_venta DATE NOT NULL,
    desc_venta VARCHAR(100),
    iva NUMERIC(5,2),
    subtotal NUMERIC(10,2),
    cliente_cedula_ruc VARCHAR(13),
    CONSTRAINT fk_cliente
        FOREIGN KEY (cliente_cedula_ruc)
        REFERENCES cliente(cedula_ruc)
);

CREATE TABLE proveedor (
    nif VARCHAR(15) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    ciudad VARCHAR(50),
    telefono VARCHAR(15),
    direccion VARCHAR(100)
);

CREATE TABLE producto (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    categoria VARCHAR(50),
    presentacion VARCHAR(50),
    fecha_vencimiento DATE,
    precio NUMERIC(10,2),
    stock INT,
    proveedor_nif VARCHAR(15),
    CONSTRAINT fk_proveedor
        FOREIGN KEY (proveedor_nif)
        REFERENCES proveedor(nif)
);

CREATE TABLE detalle_venta (
    id_venta INT,
    id_producto INT,
    cantidad INT NOT NULL,
    pvp NUMERIC(10,2),
    PRIMARY KEY (id_venta, id_producto),
    CONSTRAINT fk_venta
        FOREIGN KEY (id_venta)
        REFERENCES venta(id_venta),
    CONSTRAINT fk_producto
        FOREIGN KEY (id_producto)
        REFERENCES producto(id_producto)
);

CREATE TABLE pago (
    id_pago SERIAL PRIMARY KEY,
    fecha_pago DATE NOT NULL,
    valor NUMERIC(10,2),
    observacion VARCHAR(100),
    id_venta INT,
    CONSTRAINT fk_venta_pago
        FOREIGN KEY (id_venta)
        REFERENCES venta(id_venta)
);
