document.addEventListener("DOMContentLoaded", () => {
    const addExperienceBtn = document.getElementById("add-experience-btn");
    const experienceList = document.getElementById("experience-list");
    const experienceDisplay = document.getElementById("experience-display");
    const jobTitleInput = document.getElementById("job_title");
    const companyNameInput = document.getElementById("company_name");
    const yearsInput = document.getElementById("years");
    const form = document.querySelector('form'); // Adjust selector as needed
    const fileInput = document.querySelector('input[type="file"]'); // Adjust selector as needed

    let experienceCount = 0;

    addExperienceBtn.addEventListener("click", () => {
        const jobTitle = jobTitleInput.value.trim();
        const companyName = companyNameInput.value.trim();
        const years = yearsInput.value.trim();

        if (jobTitle && companyName && years) {
            experienceCount++;
            
            const listItem = document.createElement("li");
            listItem.classList.add("list-group-item");
            listItem.innerHTML = `
                <strong>${jobTitle}</strong> at ${companyName} (${years} years)
                <input type="hidden" name="job_title[]" value="${jobTitle}">
                <input type="hidden" name="company_name[]" value="${companyName}">
                <input type="hidden" name="years[]" value="${years}">
                <button type="button" class="btn btn-danger btn-sm float-end remove-experience-btn">Remove</button>
            `;

            experienceList.appendChild(listItem);
            experienceDisplay.style.display = "block";

            // Clear input fields
            jobTitleInput.value = "";
            companyNameInput.value = "";
            yearsInput.value = "";
        } else {
            alert("Please fill in all experience fields.");
        }
    });

    experienceList.addEventListener("click", (e) => {
        if (e.target.classList.contains("remove-experience-btn")) {
            e.target.closest("li").remove();
            experienceCount--;
            if (experienceCount === 0) {
                experienceDisplay.style.display = "none";
            }
        }
    });
        
    if (form && fileInput) {
        form.addEventListener('submit', function(e) {
            if (fileInput.files.length > 0) {
                e.preventDefault();
                
                // Get file info first
                const file = fileInput.files[0];
                
                // Create FormData from the form
                const formData = new FormData(form);
                
                // Make sure file is included (should be automatic if input is in the form)
                // But let's ensure it's there with the correct field name
                formData.set('resume', file);
                
                // Add file metadata
                formData.append('file_size', file.size);
                formData.append('file_type', file.type);
                formData.append('file_name', file.name);
                
                fetch('/apply/submit/', {
                    method: 'POST',
                    body: formData, // Send FormData directly - don't convert to string
                    headers: {
                        // IMPORTANT: Do NOT set Content-Type when sending files
                        // Let the browser set it automatically with correct boundary
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    },
                    credentials: 'same-origin',
                    redirect: 'follow'
                })
                .then(response => {
                    if (response.ok) {
                        // Handle the redirect from Django
                        window.location.href = response.url;
                    } else {
                        alert('Failed to submit application. Please try again.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                });
            }
        });
    } else {
        console.error('Form or file input not found');
    }    
    
});
