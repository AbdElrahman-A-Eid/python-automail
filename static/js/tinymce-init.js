tinymce.init({
    selector: '#body',
    height: 300,
    menubar: true,
    advcode_inline: true,
    plugins: [
        'casechange', 'autosave', 'advlist', 'link', 'searchreplace',
        'checklist', 'tinymcespellchecker', 'codesample', 'tableofcontents',
        'powerpaste', 'formatpainter', 'permanentpen', 'advtable', 'export',
        'linkchecker', 'a11ychecker', 'mediaembed',
        'advcode', 'editimage', 'image', 'tinydrive', 'visualblocks', 'autolink',
        'help', 'table', 'lists', 'charmap', 'emoticons', 'code',
        'preview', 'importcss', 'wordcount', 'quickbars', 'pageembed'
    ],
    toolbar: 'undo redo | formatselect | bold italic backcolor | \
            alignleft aligncenter alignright alignjustify | \
            bullist numlist outdent indent | removeformat | restoredraft | codesample code',
    toolbar_mode: 'floating',
    setup: (editor) => {
        editor.on("blur", function (e) {
            tinymce.triggerSave();
        });
    }
});