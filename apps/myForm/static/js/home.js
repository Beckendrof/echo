document.addEventListener('DOMContentLoaded', function() {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    const matchMessage = document.getElementById('password_match_message');

    function checkPasswordMatch() {
        if (password.value !== confirmPassword.value) {
            matchMessage.classList.remove('hidden');
            confirmPassword.setCustomValidity("Passwords do not match");
        } else {
            matchMessage.classList.add('hidden');
            confirmPassword.setCustomValidity("");
        }
    }

    if (password && confirmPassword) {
        password.addEventListener('change', checkPasswordMatch);
        confirmPassword.addEventListener('keyup', checkPasswordMatch);
    }
});

document.getElementById('user_type').addEventListener('change', function() {
    var creatorFields = document.getElementById('creator_fields');
    var editorFields = document.getElementById('editor_fields');
    if (this.value === 'creator') {
        creatorFields.classList.remove('hidden');
        editorFields.classList.add('hidden');
        creatorFields.querySelectorAll('input').forEach(input => input.required = true);
        editorFields.querySelectorAll('input').forEach(input => input.required = false);
    } else if (this.value === 'editor') {
        creatorFields.classList.add('hidden');
        editorFields.classList.remove('hidden');
        creatorFields.querySelectorAll('input').forEach(input => input.required = false);
        editorFields.querySelectorAll('input').forEach(input => input.required = true);
    } else {
        creatorFields.classList.add('hidden');
        editorFields.classList.add('hidden');
        creatorFields.querySelectorAll('input').forEach(input => input.required = false);
        editorFields.querySelectorAll('input').forEach(input => input.required = false);
    }
});
