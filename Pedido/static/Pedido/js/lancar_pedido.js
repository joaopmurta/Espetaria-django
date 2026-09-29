(() => {
    const mesaSelect = document.getElementById('id_mesa');
    const mesaButtons = document.querySelectorAll('.mesa-btn');

    const updateMesaSelection = () => {
        mesaButtons.forEach((button) => {
            button.classList.toggle('selecionada', button.dataset.mesa === mesaSelect?.value);
        });
    };

    mesaButtons.forEach((button) => {
        button.addEventListener('click', () => {
            if (!mesaSelect) return;
            mesaSelect.value = button.dataset.mesa;
            mesaSelect.dispatchEvent(new Event('change', { bubbles: true }));
            updateMesaSelection();
        });
    });
    mesaSelect?.addEventListener('change', updateMesaSelection);
    updateMesaSelection();

    const addItemButton = document.getElementById('add-espeto');
    addItemButton?.addEventListener('click', () => {
        const container = document.getElementById('espetos-container');
        const emptyForm = document.getElementById('empty-form');
        const totalForms = document.querySelector('[name$="-TOTAL_FORMS"]');
        if (!container || !emptyForm || !totalForms) return;

        const formIndex = Number.parseInt(totalForms.value, 10);
        const newItem = document.createElement('div');
        newItem.className = 'item-form';
        newItem.innerHTML = emptyForm.innerHTML.replace(/__prefix__/g, formIndex);
        container.appendChild(newItem);
        totalForms.value = formIndex + 1;
    });
})();
