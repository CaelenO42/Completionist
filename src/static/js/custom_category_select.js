function addCategoryListeners() {
  const updateButton = (value, options, buttonInner) => {
    const selectedOption = Array.from(options).find((opt) => opt.getAttribute("data-value") === value);
    if (selectedOption) {
      const newButtonContents = selectedOption.innerHTML
      buttonInner.innerHTML = newButtonContents
      buttonInner.parentElement.setAttribute("style", `--category_color: #${selectedOption.getAttribute("data-color")}`)
    }
  };
  
  const openContextMenu = (container) => {
    document.querySelectorAll(".task-category-container.active").forEach((activeContainer) => {
      if (activeContainer !== container) {
        activeContainer.classList.remove("active");
      }
    });

    container.classList.toggle("active");
  };

  document.querySelectorAll(".task-category-container").forEach((container) => {
    const button = container.querySelector(".category-button");
    const buttonInner = button.querySelector(".inner");
    const optionsList = container.querySelector(".category-options-list");
    const options = optionsList.querySelectorAll(".custom-option");
    const hiddenSelect = container.querySelector(".hidden-native-select");

    let selectedValue = container.getAttribute("data-category");

    const localUpdateButton = (value) => updateButton(value, options, buttonInner);

    localUpdateButton(selectedValue);

    button.addEventListener("click", (event) => {
      event.stopPropagation();
      
      openContextMenu(container);
    });

    button.addEventListener("contextmenu", (event) => {
      event.preventDefault();
      event.stopPropagation();
      
      openContextMenu(container);
    });

    options.forEach((option) => {
      option.addEventListener("click", (event) => {
        event.stopPropagation();

        const newValue = option.getAttribute("data-value");

        selectedValue = newValue;
        container.setAttribute("data-category", newValue);
        localUpdateButton(newValue);
        hiddenSelect.value = newValue;

        container.classList.remove("active");
        button.focus();
      });
    });
  });

  document.addEventListener("click", () => {
    document.querySelectorAll(".task-category-container.active").forEach((activeContainer) => {
      activeContainer.classList.remove("active");
    });
  });
}