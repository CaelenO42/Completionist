function addStatusListeners() {
  const OPTION_HEIGHT = 46;
  const QUICK_SET_VALUE = "complete";

  const updateButtonIcon = (value, options, iconUseElement) => {
    const selectedOption = Array.from(options).find((opt) => opt.getAttribute("data-value") === value);
    if (selectedOption) {
      const newIconId = selectedOption.getAttribute("data-icon-id");
      iconUseElement.setAttribute("href", `#${newIconId}`);
    }
  };

  const setListShift = (value, button, options, optionsList) => {
    const buttonRect = button.getBoundingClientRect();
    let selectedIndex = 0;

    options.forEach((option, index) => {
      if (option.getAttribute("data-value") === value) {
        selectedIndex = index;
      }
    });

    const requiredSpaceAbove = selectedIndex * OPTION_HEIGHT;
    let shiftAmount = -requiredSpaceAbove;

    if (buttonRect.top - requiredSpaceAbove < 10) {
      shiftAmount = 0;
    }

    optionsList.style.setProperty("--shift-amount", `${shiftAmount}px`);
  };

  const openContextMenu = (container, selectedValue, localSetShift) => {
    localSetShift(selectedValue);

    document.querySelectorAll(".task-status-container.active").forEach((activeContainer) => {
      if (activeContainer !== container) {
        activeContainer.classList.remove("active");
      }
    });

    container.classList.toggle("active");
  };

  document.querySelectorAll(".task-status-container").forEach((container) => {
    const button = container.querySelector(".status-button");
    const optionsList = container.querySelector(".status-options-list");
    const options = optionsList.querySelectorAll(".custom-option");
    const iconUseElement = container.querySelector(".selected-status-icon use");
    const hiddenSelect = container.querySelector(".hidden-native-select");

    let selectedValue = container.getAttribute("data-status");

    const localUpdateIcon = (value) => updateButtonIcon(value, options, iconUseElement);
    const localSetShift = (value) => setListShift(value, button, options, optionsList);

    localUpdateIcon(selectedValue);
    localSetShift(selectedValue);

    button.addEventListener("click", (event) => {
      event.stopPropagation();
      
      const isChildOfNewTask = container.closest('.new-task');

      if (isChildOfNewTask) openContextMenu(container, selectedValue, localSetShift);
      else {
        let newValue = "incomplete";
        if (selectedValue == "incomplete" || selectedValue == "inprogress") newValue = QUICK_SET_VALUE;

        selectedValue = newValue;
        container.setAttribute("data-status", newValue);
        localUpdateIcon(newValue);
        hiddenSelect.value = newValue;

        localSetShift(newValue);

        container.classList.remove("active");
      }
    });

    button.addEventListener("contextmenu", (event) => {
      event.preventDefault();
      event.stopPropagation();

      openContextMenu(container, selectedValue, localSetShift);
    });

    options.forEach((option) => {
      option.addEventListener("click", (event) => {
        event.stopPropagation();

        const newValue = option.getAttribute("data-value");

        selectedValue = newValue;
        container.setAttribute("data-status", newValue);
        localUpdateIcon(newValue);
        hiddenSelect.value = newValue;

        container.classList.remove("active");
        localSetShift(newValue);
        button.focus();
      });
    });
  });

  document.addEventListener("click", () => {
    document.querySelectorAll(".task-status-container.active").forEach((activeContainer) => {
      activeContainer.classList.remove("active");
    });
  });
}