var socket = io();
// Add form initialization
var form = document.getElementById('my_form');
var inputs = form.getElementsByTagName('input');
Array.from(inputs).forEach(input => {
    // FIXME: add form serialization
    input.addEventListener('change', event => {
        const oid = form.dataset.oid;
        const name = input.name;
        const value = input.value;
        const data = {
            oid,
            name,
            value
        };
        socket.emit('change', data);
    });
});

// FIXME: add namespace (rooms?)
socket.on('update', event => {
    const html = event.html;
    const form = document.getElementById('my_form');
    Alpine.morph(form, html);
});
