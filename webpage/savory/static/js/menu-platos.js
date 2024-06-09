// Obtengo el JSON del html
function obtenerJson() {
    const container = document.getElementById('contenedor-platos');
    const platosCadena = container.textContent;  // tipo string

    // cuando obtengo el JSON borro el contenido del container
    container.textContent = '';

    // reemplazo las comillas y casteo a JSON
    const platosJson = JSON.parse(platosCadena.replaceAll("'", '"'));
    return platosJson
}

// Declaro la funcion que muestra los platos
function mostrarPlatos(platos) {
    const container = document.getElementById('contenedor-platos');

    // Itero sobre el JSON
    platos.forEach(plato => {
        // Creo un <div>
        const platoDiv = document.createElement('div');
        platoDiv.classList.add('col-lg-4', 'col-md-4', 'col-sm-6');

        // Creo un <h2>
        const platoNombre = document.createElement('h2');
        platoNombre.classList.add("fh5co-text");
        // Le agrego el nombre del plato como contenido
        platoNombre.textContent = plato.nombre;

        // Creo un <p>
        const platoDescripcion = document.createElement('p');
        platoDescripcion.classList.add("fh5co-text");
        // Le agrego la descripcion del plato como contenido
        platoDescripcion.textContent = plato.descripcion;

        // Agrego el <h2> y el <p> dentro del <div>
        platoDiv.appendChild(platoNombre);
        platoDiv.appendChild(platoDescripcion);

        // Agrego todo al contenedor principal (representa un plato)
        container.appendChild(platoDiv);
    });
}

// Llamo a las funciones
const platosJson = obtenerJson();
mostrarPlatos(platosJson);
