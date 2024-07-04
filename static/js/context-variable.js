$(document).on('click', '.delete-btn', function () {
    $(this).parent('.context-variable').remove();
});

document.getElementById('add-context-variable').addEventListener('click', function () {
    const contextVariablesDiv = document.getElementById('context-variables');
    const randomIndex = Math.floor(Math.random() * 999999999) + 1;
    const newContextVariableDiv = document.createElement('div');
    newContextVariableDiv.className = 'context-variable mb-2 context-row';
    newContextVariableDiv.dataset.index = randomIndex;
    newContextVariableDiv.innerHTML = `
        <input type="text" name="context_name_${randomIndex}" class="form-input context-name mr-2 mb-0" placeholder="Context Name" required>
        <select name="context_type_${randomIndex}" class="form-input context-type mr-2 mb-0" required>
            <option value="string" selected>String</option>
            <option value="datetime">DateTime</option>
            <option value="url">URL</option>
            <option value="email">Email</option>
            <option value="number">Numeric</option>
        </select>
        <input type="text" name="context_value_${randomIndex}" class="form-input context-value mr-2 mb-0" placeholder="Value" required>
        <button type="button" class="remove-context-variable ml-2 text-red-500 delete-btn"><i class="fas fa-trash-alt"></i></button>
    `;
    contextVariablesDiv.appendChild(newContextVariableDiv);
    updateContextVariables()
});

document.getElementById('context-variables').addEventListener('click', function (e) {
    if (e.target.classList.contains('delete-btn') || e.target.parentNode.classList.contains('delete-btn')) {
        const contextVariableDiv = e.target.closest('.context-variable');
        contextVariableDiv.remove();
    }
});

function updateContextVariables () {
    document.querySelectorAll('.context-type').forEach(select => {
        select.addEventListener('change', function () {
            const input = this.parentElement.querySelector('.context-value');
            if (this.value === 'datetime') {
                input.type = 'datetime-local';
            } else if (this.value === 'string') {
                input.type = 'text';
            } else if (this.value === 'url') {
                input.type = 'url';
            } else if (this.value === 'email') {
                input.type = 'email';
            }  else if (this.value === 'number') {
                input.type = 'number';
                input.step = 'any';
            }
        });
    });
}
