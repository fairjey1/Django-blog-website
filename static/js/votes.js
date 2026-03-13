document.addEventListener("DOMContentLoaded", function() {
    const voteButtons = document.querySelectorAll('.vote-btn');
    
    // Leemos el token de seguridad desde la etiqueta meta del base.html
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    voteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            const targetId = this.getAttribute('data-target-id'); 

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken, // Usamos la variable de JS, no la de Django
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById(`like-count-${targetId}`).innerText = data.likes_count;
                document.getElementById(`dislike-count-${targetId}`).innerText = data.dislikes_count;
            })
            .catch(error => console.error('Error:', error));
        });
    });
});