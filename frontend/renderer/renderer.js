document.getElementById('send').addEventListener('click', async () => {
    const persona = document.getElementById('persona').value;
    const prompt = document.getElementById('prompt').value;
    if (!prompt.trim()) return;

    // Limpia área de respuesta y muestra indicador
    const resEl = document.getElementById('response');
    resEl.textContent = 'Cargando...';

    try {
        const resp = await fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ persona, prompt })
        });
        const { respuesta } = await resp.json();
        resEl.textContent = respuesta;
    } catch (e) {
        resEl.textContent = 'Error: ' + e.message;
    }
});