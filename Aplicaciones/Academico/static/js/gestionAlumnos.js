(function() {
    const btnEliminacion = document.querySelectorAll(".btnEliminacion")

    btnEliminacion.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmation = confirm('¿Estás seguro que quieres eliminar a este alumno?')
            if (!confirmation) {
                e.preventDefault()
            }
        })
    })
})()
