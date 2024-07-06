tinymce.init({
    selector: '#body',
    height: 300,
    menubar: true,
    advcode_inline: true,
    plugins: [
        'autosave', 'advlist', 'link', 'searchreplace',
        'codesample', 'linkchecker', 'image', 'tinydrive',
        'help', 'table', 'lists', 'charmap', 'emoticons',
        'preview', 'importcss', 'wordcount', 'quickbars',
        'visualblocks', 'autolink', 'code'
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