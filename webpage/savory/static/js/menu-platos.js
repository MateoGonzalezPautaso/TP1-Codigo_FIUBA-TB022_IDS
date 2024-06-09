// Platos hardcodeados
const platosJson = [
    {
        "nombre": "Sopa",
        "descripcion": "Vor  wieder euch wiederholt widerklang selbst ich tränen, mich wie lebt ihr gut blick gestalten. Und freundschaft gut die."
    },
    {
        "nombre": "Pizza",
        "descripcion": "De el quedo sus los y el se para, la deja bajo algodón el mudas."
    },
    {
        "nombre": "Churrasco",
        "descripcion": "Door but bird ungainly ungainly lenore for ember grave. Yore door stood days back and now nevermore, the as if."
    },
    {
        "nombre": "Spaguetti",
        "descripcion": "Halallal uos leg en scemem hol keguggethuk yg num. Wirud uos fyomnok ezes ezes kyul."
    }
];

// Declaro la funcion
function mostrarPlatos(platos) {
    // Obtengo el contenedor de platos
    const container = document.getElementById('contenedor-platos');

    // Itero sobre el JSON
    platos.forEach(plato => {
        // Creo un <div>
        const platoDiv = document.createElement('div');
        platoDiv.classList.add('col-lg-4', 'col-md-4', 'col-sm-6');

        // Creo un <h2>
        const platoNombre = document.createElement('h2');
        platoNombre.classList.add("fh5co-text")
        // Le agrego el nombre del plato como contenido
        platoNombre.textContent = plato.nombre;

        // Creo un <p>
        const platoDescripcion = document.createElement('p');
        platoDescripcion.classList.add("fh5co-text")
        // Le agrego la descripcion del plato como contenido
        platoDescripcion.textContent = plato.descripcion;

        // Agrego el <h2> y el <p> dentro del <div>
        platoDiv.appendChild(platoNombre);
        platoDiv.appendChild(platoDescripcion);

        // Agrego todo al contenedor principal (representa un plato)
        container.appendChild(platoDiv);
    });
}

// Llamo a la función 
mostrarPlatos(platosJson);
