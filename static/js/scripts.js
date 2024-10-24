const privateCheckbox = document.querySelector('#id_is_private');  // Assuming 'is_private' field's id is 'id_is_private'
    const passwordField = document.querySelector('.password-field');

    privateCheckbox.addEventListener('change', function() {
        if (this.checked) {
            passwordField.style.display = 'block';  // Show password field when checked
        } else {
            passwordField.style.display = 'none';   // Hide password field when unchecked
        }
    });