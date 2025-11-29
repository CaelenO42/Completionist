const OPTION_HEIGHT = 46;
const QUICK_SET_VALUE = "complete";

function updateCategoryButton(value, container) {
  const button = container.querySelector(".category-button");
  const buttonInner = container.querySelector(".inner");
  const options = container.querySelectorAll(".custom-option");

  const selectedOption = Array.from(options).find((opt) => opt.getAttribute("data-value") === value);

  if (selectedOption && button) {
    const newButtonContents = selectedOption.innerHTML;
    const color = selectedOption.getAttribute("data-color");

    buttonInner.innerHTML = newButtonContents;
    button.setAttribute("style", `--category_color: #${color}`);
  }
}

function updateStatusButtonIcon(value, options, iconUseElement) {
  const selectedOption = Array.from(options).find((opt) => opt.getAttribute("data-value") === value);
  if (selectedOption) {
    const newIconId = selectedOption.getAttribute("data-icon-id");
    iconUseElement.setAttribute("href", `#${newIconId}`);
  }
}

function setStatusListShift(value, button, options, optionsList) {
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
}

function openContextMenu(container) {
  document.querySelectorAll(".task-status-container.active").forEach((activeContainer) => {
    if (activeContainer !== container) activeContainer.classList.remove("active");
  });
  document.querySelectorAll(".task-category-container.active").forEach((activeContainer) => {
    if (activeContainer !== container) activeContainer.classList.remove("active");
  });

  container.classList.toggle("active");
}

document.addEventListener("click", function (event) {
  const target = event.target;

  const statusButton = target.closest(".status-button");
  if (statusButton) {
    event.stopPropagation();
    const container = statusButton.closest(".task-status-container");
    const hiddenSelect = container.querySelector(".hidden-native-select");
    const optionsList = container.querySelector(".status-options-list");
    const options = optionsList.querySelectorAll(".custom-option");
    const iconUseElement = container.querySelector(".selected-status-icon use");

    let selectedValue = container.getAttribute("data-status");

    const isChildOfNewTask = container.closest(".new-task");

    if (isChildOfNewTask) {
      openContextMenu(container);
      setStatusListShift(selectedValue, statusButton, options, optionsList);
    } else {
      let newValue = "incomplete";
      if (selectedValue === "incomplete" || selectedValue === "inprogress") newValue = QUICK_SET_VALUE;

      container.setAttribute("data-status", newValue);
      updateStatusButtonIcon(newValue, options, iconUseElement);
      hiddenSelect.value = newValue;
      setStatusListShift(newValue, statusButton, options, optionsList);

      const taskContainer = container.closest(".task-container");
      if (taskContainer) inputChanged({ target: hiddenSelect }, taskContainer);
    }
    return;
  }

  const statusOption = target.closest(".task-status-container .custom-option");
  if (statusOption) {
    event.stopPropagation();

    const container = statusOption.closest(".task-status-container");
    const hiddenSelect = container.querySelector(".hidden-native-select");
    const optionsList = container.querySelector(".status-options-list");
    const options = optionsList.querySelectorAll(".custom-option");
    const iconUseElement = container.querySelector(".selected-status-icon use");

    const newValue = statusOption.getAttribute("data-value");

    container.setAttribute("data-status", newValue);
    updateStatusButtonIcon(newValue, options, iconUseElement);
    hiddenSelect.value = newValue;

    container.classList.remove("active");
    const taskContainer = container.closest(".task-container");
    if (taskContainer) inputChanged({ target: hiddenSelect }, taskContainer);
    return;
  }

  const categoryButton = target.closest(".task-category-container .category-button");
  if (categoryButton) {
    event.stopPropagation();
    const container = categoryButton.closest(".task-category-container");
    openContextMenu(container);
    return;
  }

  const categoryOption = target.closest(".task-category-container .custom-option");
  if (categoryOption) {
    event.stopPropagation();

    const container = categoryOption.closest(".task-category-container");
    const hiddenSelect = container.querySelector(".hidden-native-select");

    const newValue = categoryOption.getAttribute("data-value");

    container.setAttribute("data-category", newValue);
    updateCategoryButton(newValue, container);
    hiddenSelect.value = newValue;

    container.classList.remove("active");
    const taskContainer = container.closest(".task-container");
    if (taskContainer) inputChanged({ target: hiddenSelect }, taskContainer);
    return;
  }

  document.querySelectorAll(".task-status-container.active").forEach((activeContainer) => {
    activeContainer.classList.remove("active");
  });
  document.querySelectorAll(".task-category-container.active").forEach((activeContainer) => {
    activeContainer.classList.remove("active");
  });
});

document.addEventListener("contextmenu", (event) => {
  const target = event.target;
  const statusButton = target.closest(".status-button");
  const categoryButton = target.closest(".task-category-container .category-button");

  if (statusButton) {
    event.preventDefault();
    event.stopPropagation();
    const container = statusButton.closest(".task-status-container");
    const optionsList = container.querySelector(".status-options-list");
    const options = optionsList.querySelectorAll(".custom-option");
    let selectedValue = container.getAttribute("data-status");

    setStatusListShift(selectedValue, statusButton, options, optionsList);
    openContextMenu(container);
  } else if (categoryButton) {
    event.preventDefault();
    event.stopPropagation();
    const container = categoryButton.closest(".task-category-container");
    openContextMenu(container);
  }
});
