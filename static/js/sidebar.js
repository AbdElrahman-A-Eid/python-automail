document.addEventListener('DOMContentLoaded', function () {
    const floatingButton = document.getElementById('floating-button');
    const sidebar = document.getElementById('sidebar');
    const closeSidebar = document.getElementById('close-sidebar');
    const dimmedBackground = document.getElementById('dimmed-background');
    const sbDimmedBackground = document.getElementById('sb-dimmed-background');
    const sbLoadingSpinner = document.getElementById('sb-loading-spinner');
    const customModelName = document.getElementById('custom_model_name');
    const modelSelection = document.getElementById('model_selection');
    const sbContextVariablesContainer = document.getElementById('sb-context-variables-container');
    const sbContextVariablesInput = document.getElementById('sb_context_variables_input');

    const enterEvent = new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter'});

    function toggleSidebar() {
        sidebar.classList.toggle('open');
        document.body.classList.toggle('open-sidebar');
        floatingButton.classList.toggle('hidden');
        dimmedBackground.classList.toggle('show');
    }

    floatingButton.addEventListener('click', function () {
        toggleSidebar();
        document.querySelectorAll("input[name^=context_name]").forEach((ctx, idx)  => {
            sbContextVariablesInput.value = ctx.value;
            sbContextVariablesInput.focus()
            sbContextVariablesInput.dispatchEvent(enterEvent)
        })
        // Remove Duplicates
        removeDuplicateSbContextVariables();
    });

    closeSidebar.addEventListener('click', function () {
        toggleSidebar();
    });

    modelSelection.addEventListener('change', function () {
        if (modelSelection.value === 'custom') {
            customModelName.classList.remove('hidden');
        } else {
            customModelName.classList.add('hidden');
        }
    });

    document.addEventListener('click', function (event) {
        if (!sidebar.contains(event.target) && !floatingButton.contains(event.target) && sidebar.classList.contains('open') && !event.target.classList.contains("remove-variable")) {
            toggleSidebar();
        }
    });

    sbContextVariablesInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' || event.key === ',') {
            event.preventDefault();
            const value = sbContextVariablesInput.value.trim();
            if (value) {
                addContextVariable(value);
                sbContextVariablesInput.value = '';
            }
            removeDuplicateSbContextVariables()
        }
    });

    function addContextVariable(value) {
        const variableBox = document.createElement('div');
        variableBox.className = 'sb-context-variable';
        variableBox.innerHTML = `
            <span>${value}</span>
            <button type="button" class="remove-variable">&times;</button>
        `;
        sbContextVariablesContainer.insertBefore(variableBox, sbContextVariablesInput);

        variableBox.querySelector('.remove-variable').addEventListener('click', function () {
            sbContextVariablesContainer.removeChild(variableBox);
        });
    }

    document.getElementById('template-form').addEventListener('submit', function (e) {
        e.preventDefault();
        sbDimmedBackground.classList.toggle('show');
        sbLoadingSpinner.classList.add('show');

        const sbContextVariables = [];
        document.querySelectorAll('.sb-context-variable span').forEach(span => {
            sbContextVariables.push(span.textContent);
        });

        const formData = {
            model: modelSelection.value === 'custom' ? customModelName.value : modelSelection.value,
            system_prompt: document.getElementById('system_prompt').value,
            user_prompt: document.getElementById('user_prompt').value,
            temperature: parseFloat(document.getElementById('temperature').value),
            max_output_length: parseInt(document.getElementById('max_output_length').value),
            top_p: parseFloat(document.getElementById('top_p').value),
            frequency_penalty: parseFloat(document.getElementById('frequency_penalty').value),
            context_variables: sbContextVariables
        };

        console.log('Form Data:', formData);

        $.ajax({
            url: "/generate",
            type: "POST",
            data: JSON.stringify(formData),
            contentType: "application/json",
            cache: false,
            success: function (response) {
                sbDimmedBackground.classList.toggle('show');
                sbLoadingSpinner.classList.remove('show');
                toggleSidebar()
                document.getElementById('subject').scrollIntoView({ behavior: 'smooth'});
                document.getElementById('subject').setAttribute('value', response.template.subject);
                tinymce.get("body").setContent(response.template.body);
                document.getElementById("body_ifr").focus()
                generateAlert(response, `Mail Template was generated successfully!`);
            },
            error: function (response) {
                sbDimmedBackground.classList.toggle('show');
                sbLoadingSpinner.classList.remove('show');
                toggleSidebar()
                generateAlert(response.responseJSON, `Mail Template cannot be generated!`);
            }
        });
    });

    $(function() {
        var $sidebar = $('#sidebar');
        $sidebar.bind('scroll', function() {
            if ($sidebar.scrollLeft() !== 0) {
                $sidebar.scrollLeft(0);
            }
        });
    }); 
});

function removeDuplicateSbContextVariables() {
    const children = document.querySelectorAll(".sb-context-variable");
    var tmpCtx = [];
    for (const c of children) {
        if (tmpCtx.includes(c.innerText)) {
            c.parentNode.removeChild(c);
        } else {
            tmpCtx.push(c.innerText);
        }
    }
}

