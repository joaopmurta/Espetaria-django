(() => {
    const counters = {
        'Em espera': document.getElementById('hud-count-espera'),
        'Em Preparo': document.getElementById('hud-count-preparo'),
        Pronto: document.getElementById('hud-count-pronto'),
    };

    if (Object.values(counters).some((counter) => !counter)) return;

    const scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const socket = new WebSocket(`${scheme}://${window.location.host}/ws/hud/`);

    socket.onmessage = (event) => {
        const payload = JSON.parse(event.data);
        const counts = payload.count_by_status || payload.data?.count_by_status || payload.data;

        if (!counts) return;

        Object.entries(counters).forEach(([status, counter]) => {
            counter.textContent = counts[status] ?? '0';
        });
    };

    socket.onclose = () => {
        console.error('WebSocket do HUD foi desconectado.');
    };
})();
