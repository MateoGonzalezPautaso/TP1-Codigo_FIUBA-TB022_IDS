/* SE CREAN LAS TABLAS */

CREATE TABLE IF NOT EXISTS usuarios(
    username VARCHAR(30) UNIQUE NOT NULL,
    password VARCHAR(20) NOT NULL,
    PRIMARY KEY(username)
    );

CREATE TABLE IF NOT EXISTS recetas(
    nombre VARCHAR(80),
    ingredientes JSON,
    duenio VARCHAR(30) NOT NULL,
    descripcion TEXT,
    imagen VARCHAR(180),
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(nombre),
    FOREIGN KEY (duenio) REFERENCES usuarios(username)
    );

/* SE INSERTAN VALORES */

INSERT INTO usuarios (username, password) VALUES
    ('main', 'MTIzNA=='),  -- 1234
    ('carlosperez23', 'cGFzc3dvcmQ='), -- password
    ('damian_chef', 'cXdlcnR5'), -- qwerty
    ('laura_m', 'cmF0YXRvdWlsbGU='), -- ratatouille
    ('paula_cocina', 'cGF1NWVzdHJlbGxhcw=='); -- pau5estrellas

INSERT INTO recetas (nombre, ingredientes, duenio, descripcion, imagen) VALUES
    (
        'Spaghetti con salsa de tomate', 
        '{"spaghetti": "200g", "tomate": "2", "ajo": "2 dientes", "aceite de oliva": "30ml", "sal": "10mg"}', 
        'main', 
        'Fideos con salsa de tomate fresca con aceite de oliva y ajo.',
        'https://imag.bonviveur.com/espaguetis-rojos-con-tomate.jpg'
    ),

    (
        'Sopa de Tomate', 
        '{"tomates": "4", "caldo de pollo": "500ml", "cebolla": "1", "ajo": "2 dientes", "aceite de oliva": "30ml", "sal": "5g", "pimienta": "2g", "crema": "100ml"}', 
        'main', 
        'Sopa caliente de tomates frescos con cebolla, ajo, caldo de pollo y un toque de crema.',
        'https://assets.tmecosys.com/image/upload/t_web767x639/img/recipe/ras/Assets/7D232720-0F91-41E1-99D7-9DAC5F413404/Derivates/360431A8-187D-4325-B46F-060CC1F6EDE4.jpg'
    ),

    (
        'Hamburguesa', 
        '{"pan de hamburguesa": "1", "carne de res": "200g", "queso cheddar": "1 rebanada", "lechuga": "1 hoja", "tomate": "2 rodajas", "cebolla": "1 rodaja"}', 
        'main', 
        'Hamburguesa con carne de res, queso cheddar, lechuga, tomate y cebolla.',
        'https://img.freepik.com/fotos-premium/hamburguesa-lechuga-tomate-cebolla-morada-queso-base-madera-tejido-cuadros-rojos-fondo-negro-espacio-texto_442783-27.jpg'
    ),

    (
        'Churrasco', 
        '{"carne de res": "1 kg", "ajo": "3 dientes", "sal": "5g"}', 
        'main', 
        'Churrasco a la plancha con ajo.',
        'https://osolemio.com.co/181/churrasco-a-la-plancha.jpg'
    ),

    (
        'Brownies de Chocolate', 
        '{"chocolate": "200g", "manteca": "100g", "azúcar": "200g", "harina": "100g", "huevos": "3", "esencia de vainilla": "5ml"}', 
        'main', 
        'Brownies de chocolate con una textura suave y húmeda.',
        'https://www.recetasderechupete.com/wp-content/uploads/2019/11/Brownie-1200x828.jpg'
    );