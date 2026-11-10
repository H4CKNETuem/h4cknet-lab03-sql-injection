const form = document.getElementById('busqueda');
const target = document.getElementById('resultados');
if (form && target) {
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    target.innerHTML = '<p class="notice">Buscando…</p>';
    try {
      const response = await fetch(form.action, {
        method: 'POST',
        body: new URLSearchParams(new FormData(form)),
        credentials: 'same-origin',
      });
      const html = await response.text();
      target.innerHTML = response.ok ? html : '<p class="notice error">No se pudo completar la búsqueda.</p>';
    } catch (_) {
      target.innerHTML = '<p class="notice error">Error de conexión. Inténtalo de nuevo.</p>';
    }
  });
}
