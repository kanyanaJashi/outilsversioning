// Example: Client-side form validation (can be enhanced)
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.querySelector('#upload-form'); // Assuming you have an ID on your form

    if (uploadForm) {
        uploadForm.addEventListener('submit', function(event) {
            const fileInput = document.querySelector('#data_file'); // Assuming 'data_file' is the ID of your file input
            if (!fileInput.files.length) {
                alert('Please select a file to upload.');
                event.preventDefault(); // Prevent form submission
            }
        });
    }
});