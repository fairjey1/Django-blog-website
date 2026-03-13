
document.addEventListener("DOMContentLoaded", function() {
    // Elementos clave del DOM
    const formContainer = document.getElementById('form-container');
    const originalLocation = document.getElementById('original-form-location');
    const parentIdField = document.getElementById('parent_id_field');
    const cancelBtn = document.getElementById('cancel-reply');

    // Seleccionamos todos los botones "Responder" de los comentarios
    const replyButtons = document.querySelectorAll('.btn-reply');

    replyButtons.forEach(button => {
        button.addEventListener('click', function() {
            // 1. Obtenemos el ID del comentario al que le dimos clic
            const replyId = this.getAttribute('data-reply-id');
            
            // 2. Asignamos ese ID al campo oculto del formulario
            parentIdField.value = replyId;
            
            // 3. Movemos el formulario físicamente debajo de este botón
            // 'this.parentElement' es el div del comentario específico
            this.parentElement.appendChild(formContainer);
            
            // 4. Mostramos el botón de cancelar y enfocamos la caja de texto
            cancelBtn.style.display = 'inline-block';
            document.querySelector('#reply-form textarea').focus();
        });
    });

    // Lógica para cancelar y volver al hilo principal
    cancelBtn.addEventListener('click', function() {
        // 1. Vaciamos el ID (para que vuelva a ser respuesta al Hilo)
        parentIdField.value = '';
        
        // 2. Devolvemos el formulario a su lugar original arriba/abajo
        originalLocation.appendChild(formContainer);
        
        // 3. Ocultamos el botón de cancelar
        this.style.display = 'none';
    });
});
