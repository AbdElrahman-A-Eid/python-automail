function convert_to_blob() {
    const content = tinymce.get("body").getContent();
    if (body !== '') {
        const doc = `
            <!DOCTYPE html>
            <html>
                <head>
                <meta charset="UTF-8">
                <title>${document.getElementById("subject").value}</title>
                </head>
                <body>
                ${content}
                </body>
            </html>`;
        var a = document.createElement('a');
        var blob = new Blob([doc], { type: 'text/html' });
        var url = window.URL.createObjectURL(blob);
        var filename = 'template.html';
        a.href = url;
        a.download = filename;
        return [blob, a];
    } else {
        alert("Email body cannot be empty!")
    }
}

document.getElementById('save-template').addEventListener('click', function () {
    const [blob, a] = convert_to_blob()
    a.click()
});

document.getElementById('load-template').addEventListener('change', function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            tinymce.get("body").setContent(e.target.result);
        };
        document.getElementById("body_ifr").focus()
        reader.readAsText(file);
    }
});

async function submit_form() {
    const form = document.getElementById("form")

    const [blob, a] = convert_to_blob();
    const data = new FormData(form)
    data.append("body_file", blob, "template_mail.html")
    
    await $.ajax({
        url: "/",
        type: "POST",
        data: data,
        contentType: false,
        cache: false,
        processData: false,
        success: function (response) {
            generateAlert(response)
        },
        error: function (response) {
            generateAlert(response.responseJSON)
        }
    });
}