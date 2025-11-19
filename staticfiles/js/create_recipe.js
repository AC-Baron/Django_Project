document.addEventListener("DOMContentLoaded", function () {
  const addBtn = document.getElementById("add-ingredient");
  const formContainer = document.getElementById("ingredient-forms");
  const totalForms = document.querySelector('[name$="-TOTAL_FORMS"]'); // more robust

  addBtn.addEventListener("click", function () {
    const formCount = parseInt(totalForms.value);
    const newForm = formContainer.children[0].cloneNode(true);

    // Clear inputs and update names/IDs
    newForm.querySelectorAll("input").forEach((input) => {
      input.value = "";
      input.name = input.name.replace(/-(\d+)-/, `-${formCount}-`);
      input.id = "id_" + input.name;
    });

    formContainer.appendChild(newForm);
    totalForms.value = formCount + 1;
  });

  // Remove ingredient form
  formContainer.addEventListener("click", function (e) {
    if (e.target.classList.contains("remove-ingredient")) {
      const formCount = parseInt(totalForms.value);
      if (formCount > 1) {
        e.target.closest(".ingredient-form").remove();
        totalForms.value = formCount - 1;
      }
    }
  });
});
