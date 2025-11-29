const tasks = [];
const categories = [];
const filters = {
  category: [],
  date: "",
  status: []
}

function contentFromTask(task) {
  return `
  <div class="task-container" data-uuid="${task.uuid}" data-position="${task.position}">
    ${createStatusDropdown(task.status)}
    <input name="title" type="text" class="title" value="${task.title}">
    <span class="created-date">${new Date().getFullYear() == new Date(task.created_at).getFullYear() ? new Date(task.created_at).toLocaleString("en-US", {month: 'short', day: "numeric"}) : new Date(task.created_at).toLocaleString("en-US", {month: 'numeric', 'day': "numeric", year: 'numeric'})}</span>
    <div class="due-date-container">
      <input name="due-date" type="date" class="due-date hidden" value="${!task.due_date ? "" : new Date(task.due_date).toLocaleString("en-CA", {year: 'numeric', month: '2-digit', 'day': '2-digit', timeZone: 'UTC'})}">
      <button onclick="dueDateToggle(event)" class="due-date-pretty">${!task.due_date ? "None" : new Date().getFullYear() == new Date(task.due_date).getUTCFullYear() ? new Date(task.due_date).toLocaleString("en-US", {month: 'short', day: "numeric", timeZone: 'UTC'}) : new Date(task.due_date).toLocaleString("en-US", {month: 'numeric', 'day': "numeric", year: 'numeric', timeZone: 'UTC'})}</button>
    </div>
    ${createCategoryDropdown(task.category_id)}
    <button class="delete glass error" onclick="deleteTask('${task.uuid}')"><i class="fa-regular fa-trash-can"></i></button>
  </div>`;
}

function createStatusDropdown(currentStatus) {
  return `
    <div class="task-status-container" data-status="${currentStatus}">
      <button class="status-button" tabindex="0">
          <svg class="selected-status-icon" width="32" height="32" viewBox="0 0 32 32"">
              <use href="#icon-${currentStatus}"></use> 
          </svg>
      </button>

      <div class="status-options-list">
          <div class="custom-option" data-value="planned" data-icon-id="icon-planned">
              <svg class="option-icon" width="32" height="32" viewBox="0 0 32 32"><use href="#icon-planned"></use></svg>
              Planned
          </div>
          <div class="custom-option" data-value="incomplete" data-icon-id="icon-incomplete">
              <svg class="option-icon" width="32" height="32" viewBox="0 0 32 32"><use href="#icon-incomplete"></use></svg>
              Incomplete
          </div>
          <div class="custom-option" data-value="inprogress" data-icon-id="icon-inprogress">
              <svg class="option-icon" width="32" height="32" viewBox="0 0 32 32"><use href="#icon-inprogress"></use></svg>
              In Progress
          </div>
          <div class="custom-option" data-value="complete" data-icon-id="icon-complete">
              <svg class="option-icon" width="32" height="32" viewBox="0 0 32 32"><use href="#icon-complete"></use></svg>
              Complete
          </div>
          <div class="custom-option" data-value="dropped" data-icon-id="icon-dropped">
              <svg class="option-icon" width="32" height="32" viewBox="0 0 32 32"><use href="#icon-dropped"></use></svg>
              Dropped
          </div>
      </div>

      <select class="hidden-native-select" name="task-status" aria-hidden="true">
          <option value="planned" ${currentStatus == "planned" ? "selected": ""}>Planned</option>
          <option value="incomplete" ${currentStatus == "incomplete" ? "selected": ""}>Incomplete</option>
          <option value="inprogress" ${currentStatus == "inprogress" ? "selected": ""}>In Progress</option>
          <option value="complete" ${currentStatus == "complete" ? "selected": ""}>Complete</option>
          <option value="dropped" ${currentStatus == "dropped" ? "selected": ""}>Dropped</option>
      </select>
    </div>`;
}

function createCategoryDropdown(currentCategoryID = "none") {
  let currentCategory = categories.find(category => category.uuid === currentCategoryID);
  let categoryString = `
  <div class="task-category-container" data-category="${currentCategory ? currentCategory.uuid : "none"}">
    <button class="category-button" tabindex="0" style="--category_color: #${currentCategory ? currentCategory.color : "555"};">
      <div class="inner">
        ${currentCategory ? currentCategory.name : "None"}
      </div>
      <i class="fa-solid fa-angle-down"></i>
    </button>
    <div class="category-options-list">
      <div class="custom-option" data-value="none" data-color="555" style="--category_color: #555;">
        <span class="color-swatch"></span>
        None
      </div>`;

  categories.forEach(category => {
    categoryString += `
      <div class="custom-option" data-value="${category.uuid}" data-color="${category.color}" style="--category_color: #${category.color};">
        <span class="color-swatch"></span>
        ${category.name}
      </div>`;
  })

  categoryString += `
      <button class="create-button" onclick="newCategoryModal()">
        <i class="fa-solid fa-plus"></i> Create New
      </button>
    </div>
    <select class="hidden-native-select" name="task-category" aria-hidden="true">
      <option value="none">None</option>`;

  categories.forEach(category => {
      categoryString += `<option value="${category.uuid}">${category.name}</option>`;
  })

  categoryString += `
    </select>
  </div>`;

  return categoryString;
}

function generateLayout() {
  let list = document.querySelector('div.task-list');
  tasks.sort((a, b) => a.position - b.position);

  const filteredTasks = tasks.filter(task => {
    const isCategoryMatch = filters.category.length == 0 || filters.category.includes(task.category_id);
    const isStatusMatch = filters.status.length == 0 || filters.status.includes(task.status);
    const isDueDateMatch = !filters.date || isInDateRange(task.due_date, filters.date);

    return isCategoryMatch && isStatusMatch && isDueDateMatch;
  })

  let newListContent = '';
  filteredTasks.forEach(task => newListContent += contentFromTask(task));
  list.innerHTML = newListContent;

  document.querySelectorAll(".task-container").forEach(container => container.addEventListener("focusout", (e) => inputChanged(e, container)));
  document.querySelectorAll("input.due-date").forEach(input => input.addEventListener("focusout", (e) => dueDateToggle(e, true)));
}

// Task API Calls
async function getTasks() {
  try {
    const response = await protectedApiFetch(`${API_BASE}/task/get`, {
      method: 'POST'
    });

    const data = await response.json();

    if (response.ok) {
      data.forEach(task => {
        if (!_.find(tasks, task)) tasks.push(task);
      });
      generateLayout();
    }
    else console.log(`Proctected access failed: ${data.msg}`);
  } catch (err) {
    console.error(`Operation Failed: ${err.message}`);
  }
}

async function getNewTask(taskId) {
  try {
    const response = await protectedApiFetch(`${API_BASE}/task/get/${taskId}`, {
      method: 'POST'
    });

    const data = await response.json();

    if (response.ok) {
      tasks.push(data);
      generateLayout();
    }
    else console.log(`Proctected access failed: ${data.msg}`);
  } catch (err) {
    console.error(`Operation Failed: ${err.message}`);
  }
}

async function setTask(taskId, body) {
  try {
    const response = await protectedApiFetch(`${API_BASE}/task/set/${taskId}`, {
      method: 'POST',
      body: JSON.stringify(body),
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();

    if (response.ok) {
      console.log(`Updated task ${taskId}`);
    }
    else console.log(`Proctected access failed: ${data.msg}`);
  } catch (err) {
    console.error(`Operation Failed: ${err.message}`);
  }
}

async function newTask(task_data) {
  try {
    const response = await protectedApiFetch(`${API_BASE}/task/new`, {
      method: 'POST',
      body: JSON.stringify(task_data),
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();

    if (response.ok) getNewTask(data.id);
    else console.log(`Proctected access failed: ${data.msg}`);
  } catch (err) {
    console.error(`Operation Failed: ${err.message}`);
  }
}

async function deleteTask(taskId) {
  try {
    const response = await protectedApiFetch(`${API_BASE}/task/delete/${taskId}`, {
      method: 'POST'
    });

    const data = await response.json();

    if (response.ok) {
      console.log(data.msg);
      tasks.pop(_.findIndex(tasks, {uuid: taskId}))
      document.querySelector(`.task-container[data-uuid='${taskId}']`).remove();
    }
    else console.log(`Proctected access failed: ${data.msg}`);
  } catch (err) {
    console.error(`Operation Failed: ${err.message}`);
  }
}

// Category API Calls
async function getCategories() {
  try {
    const response = await protectedApiFetch(`${API_BASE}/category/get`, {
      method: 'POST'
    });

    const data = await response.json();

    if (response.ok) {
      data.forEach(category => {
        if (!_.find(categories, category)) categories.push(category);
      });
    }
    else console.log(`Proctected access failed: ${data.msg}`);
  } catch (err) {
    console.error(`Operation Failed: ${err.message}`);
  }
}

async function newCategory(category_data) {
  try {
    const response = await protectedApiFetch(`${API_BASE}/category/new`, {
      method: 'POST',
      body: JSON.stringify(category_data),
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();

    if (response.ok) {
      categories.push(data);
      regenerateCategories();
    }
    else console.log(`Proctected access failed: ${data.msg}`);
  } catch (err) {
    console.error(`Operation Failed: ${err.message}`);
  }
}

// Due Date Button to Input Toggle
function dueDateToggle(event, doClose) {
  let input = event.target.parentElement.querySelector("input.due-date");
  let button = event.target.parentElement.querySelector("button.due-date-pretty");
  if (doClose) {
    button.innerHTML = new Date().getFullYear() == new Date(input.value).getUTCFullYear() ? new Date(input.value).toLocaleString("en-US", {month: 'short', day: "numeric", timeZone: 'UTC'}) : new Date(input.value).toLocaleString("en-US", {month: 'numeric', 'day': "numeric", year: 'numeric', timeZone: 'UTC'})
    input.classList.add("hidden");
    button.classList.remove("hidden");
  } else {
    input.classList.remove("hidden");
    button.classList.add("hidden");
  }
}

// New Task Stuff
function taskToggle(doClose) {
  if (doClose) {
    document.querySelector(".new-task button.new").classList.remove("hidden");
    document.querySelector(".new-task .input").classList.add("hidden");
    // Clear fields
    newTaskClear();
  } else {
    document.querySelector(".new-task button.new").classList.add("hidden");
    document.querySelector(".new-task .input").classList.remove("hidden");
  }
}

function newTaskClear() {
  document.querySelector("#new-task-title").value = "";

  generateNewTaskStatus();
  generateNewTaskCategories();
  
  document.querySelector("input#new-due-date").value = new Date().toLocaleString("en-CA", {year: 'numeric', month: '2-digit', 'day': "2-digit"});
}

function addNewTask() {
  let newTaskContainer = document.querySelector(".new-task");

  let data = {
    title: newTaskContainer.querySelector("#new-task-title").value,
    status: newTaskContainer.querySelector("select[name='task-status']").value,
    due_date: newTaskContainer.querySelector("#new-due-date").value,
    category_id: newTaskContainer.querySelector("select[name='task-category']").value == "none" ? null : newTaskContainer.querySelector("select[name='task-category']").value
  }

  taskToggle(true);
  newTask(data);
}

// Task DB Sync
function inputChanged(e, container) {
  let taskId = container.getAttribute("data-uuid");

  let data = {
    title: container.querySelector("input.title").value,
    status: container.querySelector("select[name='task-status']").value,
    due_date: container.querySelector("input.due-date").value,
    category_id: container.querySelector("select[name='task-category']").value == "none" ? null : container.querySelector("select[name='task-category']").value
  }
  if(!_.find(tasks, {uuid: taskId, status: data.status, title: data.title, due_date: new Date(data.due_date).toUTCString(), category_id: data.category_id})) setTask(taskId, data);
}

// Generate New Task Status
function generateNewTaskStatus() {
  let container = document.querySelector(".new-task .task-status-container");

  let newHTMLString = createStatusDropdown("incomplete");
  let parser = new DOMParser();
  let doc = parser.parseFromString(newHTMLString, 'text/html');
  let newElement = doc.body.firstChild;
  container.replaceWith(newElement);
}

// Generate New Task Category Selector
function generateNewTaskCategories() {
  let container = document.querySelector(".new-task .task-category-container");

  let newHTMLString = createCategoryDropdown("none");
  let parser = new DOMParser();
  let doc = parser.parseFromString(newHTMLString, 'text/html');
  let newElement = doc.body.firstChild;
  container.replaceWith(newElement);
}

// Regenerate Category Selectors
function regenerateCategories() {
  const categoryContainers = document.querySelectorAll('.task-category-container');

  categoryContainers.forEach(container => {
    let currentCategory = container.getAttribute("data-category");

    let newHTMLString = createCategoryDropdown(currentCategory);
    let parser = new DOMParser();
    let doc = parser.parseFromString(newHTMLString, 'text/html');
    let newElement = doc.body.firstChild;

    container.replaceWith(newElement);
  })

  generateCategoryFilters();
}

// New Category Modal Stuff
function newCategoryModal() {
  document.querySelector("dialog").showModal();
}

document.querySelector("dialog").addEventListener("close", (e) => {
  let dialog = document.querySelector("dialog");
  let nameField = dialog.querySelector("input#category-name");
  let colorField = document.querySelector("input[type='radio']:checked");

  if (dialog.returnValue === "create" && nameField.value && colorField) {
    data = {
      name: nameField.value,
      color: colorField.value,
    }

    newCategory(data);
  }

  dialog.querySelector("input#category-name").value = "";
  dialog.querySelectorAll("input[type='radio']").forEach(button => button.checked = false);
});

document.querySelector("dialog #confirmBtn").addEventListener("click", (e) => {
  e.preventDefault();
  document.querySelector("dialog").close("create");
});

// Category Filter Stuff
function generateCategoryFilters() {
  let filterContainer = document.querySelector(".category-list.filter-list");

  let filterButtons = `
  <button onclick='filterByCategory(event)' data-value='none'>
    <span class="color-swatch" style="--category_color: #555;"></span>
    None
  </button>`;

  categories.forEach(category => {
    filterButtons += `
    <button onclick='filterByCategory(event)' data-value='${category.uuid}'>
      <span class="color-swatch" style="--category_color: #${category.color};"></span>
      ${category.name}
    </button>`;
  })

  filterContainer.innerHTML = filterButtons;
}

// Filtering Logic
function filterByCategory(event, clear) {
  if (clear) {
    filters.category.length = 0;
    document.querySelectorAll(".category-list.filter-list button").forEach(button => button.classList.remove("active"));
    generateLayout();
    return;
  }

  let button = event.target;
  let filter = button.getAttribute("data-value") == "none" ? null : button.getAttribute("data-value");
  if (!filters.category.includes(filter)) {
    filters.category.push(filter);
    button.classList.add("active");
  } else if (filters.category.includes(filter)) {
    filters.category.splice(filters.category.indexOf(filter), 1)
    button.classList.remove("active");
  }

  generateLayout();
}

function filterByStatus(event, clear) {
  if (clear) {
    filters.status.length = 0;
    document.querySelectorAll(".status-list.filter-list button").forEach(button => button.classList.remove("active"));
    generateLayout();
    return;
  }

  let button = event.target;
  let filter = button.getAttribute("data-value");
  if (!filters.status.includes(filter)) {
    filters.status.push(filter);
    button.classList.add("active");
  } else if (filters.status.includes(filter)) {
    filters.status.splice(filters.status.indexOf(filter), 1)
    button.classList.remove("active");
  }

  generateLayout();
}

function filterByDate(event, clear) {
  if (clear) {
    filters.date = "";
    document.querySelectorAll(".date-list.filter-list button").forEach(button => button.classList.remove("active"));
    generateLayout();
    return;
  }

  let button = event.target;
  let filter = button.getAttribute("data-value");
  document.querySelectorAll(".date-list.filter-list button").forEach(button => button.classList.remove("active"));
  filters.date = filter;
  button.classList.add("active");

  generateLayout();
}

function isInDateRange(taskDueDate, period) {
  if (!taskDueDate) return false;

  const taskDate = new Date(taskDueDate);
  const today = new Date();
  taskDate.setUTCHours(0,0,0,0);
  today.setUTCHours(0,0,0,0);

  const getStartOfWeek = (date) => {
    const d = new Date(date);
    d.setUTCHours(0,0,0,0);
    const day = d.getUTCDay();
    const diff = d.getUTCDate() - day + (day == 0 ? -6 : 1);
    d.setUTCDate(diff);
    return d;
  }

  const getStartOfMonth = (date) => {
    const d = new Date(date);
    d.setUTCHours(0, 0, 0, 0);
    d.setUTCDate(1);
    return d;
  };

  const getStartOfYear = (date) => {
    const d = new Date(date);
    d.setUTCHours(0, 0, 0, 0);
    d.setUTCMonth(0, 1);
    return d;
  };

  console.log(taskDate);
  console.log(today);

  switch (period.toLowerCase()) {
    case 'today':
      return taskDate.getTime() == today.getTime();
      
    case 'week':
      const startOfWeek = getStartOfWeek(today);
      const endOfWeek = new Date(startOfWeek);
      endOfWeek.setUTCDate(startOfWeek.getUTCDate() + 7);
      return taskDate >= startOfWeek && taskDate < endOfWeek;

    case 'month':
      const startOfMonth = getStartOfMonth(today);
      const startOfNextMonth = new Date(startOfMonth);
      startOfNextMonth.setUTCMonth(startOfNextMonth.getUTCMonth() + 1);
      return taskDate >= startOfMonth && taskDate < startOfNextMonth;

    case 'year':
      const startOfYear = getStartOfYear(today);
      const startOfNextYear = new Date(startOfYear);
      startOfNextYear.setUTCFullYear(startOfNextYear.getUTCFullYear() + 1);
      return taskDate >= startOfYear && taskDate < startOfNextYear;

    case 'past':
      return taskDate < today;

    default:
      return false;
  }
}

// File Load stuff
async function main() {
  await getCategories();
  generateCategoryFilters();
  getTasks();
  generateNewTaskStatus();
  generateNewTaskCategories();

  document.querySelector("input#new-due-date").setAttribute("value", new Date().toLocaleString("en-CA", {year: 'numeric', month: '2-digit', 'day': "2-digit"}));
}

main();