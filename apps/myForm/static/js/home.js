document.addEventListener('DOMContentLoaded', function() {
    const userTypeField = document.getElementById('id_user_type');
    const creatorFields = ['youtube_channel', 'brand_name'];
    const editorFields = ['display_name', 'expertise_tags'];

    function toggleFields() {
        const userType = userTypeField.value;
        creatorFields.forEach(id => {
            const field = document.getElementById('id_' + id);
            const isCreator = userType === 'creator';
            field.parentElement.classList.toggle('hidden', !isCreator);
            field.classList.toggle('hidden', !isCreator);
            field.required = isCreator;
        });
        editorFields.forEach(id => {
            const field = document.getElementById('id_' + id);
            const isEditor = userType === 'editor';
            field.parentElement.classList.toggle('hidden', !isEditor);
            field.classList.toggle('hidden', !isEditor);
            field.required = isEditor;
        });
    }

    userTypeField.addEventListener('change', toggleFields);
    toggleFields();
});
