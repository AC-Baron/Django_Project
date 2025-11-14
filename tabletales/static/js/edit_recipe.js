document.addEventListener("DOMContentLoaded", function () {

    console.log("Edit JS loaded");

    const addBtn = document.getElementById("add-ingredient");
    const formContainer = document.getElementById("ingredient-forms");
    const emptyFormDiv = document.getElementById("empty-form");
    const totalForms = document.querySelector('[name$="-TOTAL_FORMS"]');

    if (!addBtn || !formContainer || !emptyFormDiv || !totalForms) {
        console.warn("Edit ingredient JS: required elements missing.");
        return;
    }

    const emptyTemplate = emptyFormDiv.innerHTML;

    // -------------------------------
    // ADD INGREDIENT
    // -------------------------------
    addBtn.addEventListener("click", function () {
        console.log("Add clicked");

        const index = parseInt(totalForms.value);

        const newForm = document.createElement("div");
        newForm.classList.add("ingredient-form");
        newForm.innerHTML = emptyTemplate.replace(/__prefix__/g, index);

        // Hide DELETE checkbox for new forms
        const delBox = newForm.querySelector("input[name$='-DELETE']");
        if (delBox) delBox.style.display = "none";

        const delLabel = newForm.querySelector("label[for='" + delBox?.id + "']");
        if (delLabel) delLabel.style.display = "none";

        formContainer.appendChild(newForm);
        totalForms.value = index + 1;
    });

    // -------------------------------
    // REMOVE INGREDIENT
    // -------------------------------
    formContainer.addEventListener("click", (e) => {
        if (!e.target.classList.contains("remove-ingredient")) return;

        const formDiv = e.target.closest(".ingredient-form");

        // Existing ingredient → tick DELETE instead of removing
        const deleteCheckbox = formDiv.querySelector("input[name$='-DELETE']");
        if (deleteCheckbox) {
            deleteCheckbox.checked = true;
            formDiv.style.display = "none";
            return;
        }

        // New unsaved ingredient → remove fully
        formDiv.remove();
    });

});
