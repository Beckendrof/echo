document.addEventListener("DOMContentLoaded", () => {
    const addExperienceBtn = document.getElementById("add-experience-btn");
    const experienceList = document.getElementById("experience-list");
    const experienceDisplay = document.getElementById("experience-display");
    const jobTitleInput = document.getElementById("job_title");
    const companyNameInput = document.getElementById("company_name");
    const yearsInput = document.getElementById("years");

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
});
