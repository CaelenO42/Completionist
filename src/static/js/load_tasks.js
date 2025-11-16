function contentFromTask(task) {
  return `
  <div class="task-container" data-uuid="${task.uuid}" data-position="${task.position}">
    ${createStatusDropdown(task.status)}
    <input type="text" class="title" value="${task.title}">
    <span class="createdDate">${new Date(task.created_at).toLocaleString().split(",")[0].replaceAll("/", "-").trim()}</span>
    <button class="delete" onclick="deleteTask('${task.uuid}')">Delete</button>
  </div>`;
}

function createStatusDropdown(currentStatus) {
  return `<select name="status" id="status">
    <option value="planned" ${currentStatus == "planned" ? "selected": ""}>Planned</option>
    <option value="completed" ${currentStatus == "completed" ? "selected": ""}>Completed</option>
    <option value="inprogress" ${currentStatus == "inprogress"? "selected": ""}>In Progress</option>
    <option value="dropped" ${currentStatus == "dropped" ? "selected": ""}>Dropped</option>
  </select>`
}

function generateLayout(tasks) {
  console.log(tasks);
  list = document.querySelector('div.taskList');
  list.innerHTML = "";
  tasks.sort((a, b) => a.position - b.position);
  tasks.forEach(task => list.innerHTML += contentFromTask(task))
  document.querySelectorAll(".task-container").forEach(container => container.addEventListener("focusout", (e) => inputChanged(e)));
}


async function getTasks() {
  try {
    const response = await protectedApiFetch(`${API_BASE}/task/get`, {
      method: 'POST'
    });

    const data = await response.json();

    if (response.ok) generateLayout(data);
    else console.log(`Proctected access failed: ${data.msg}`);
  } catch (err) {
    console.error(`Operation Failed: ${err.message}`);
  }
}

async function testSet() {
  try {
    const response = await protectedApiFetch(`${API_BASE}/task/set/b98991ab-1c2e-42cb-a8c0-fb5308a15e05`, {
      method: 'POST',
      body: JSON.stringify({
        title: "This is the new title",
        status: "complete",
        position: 3
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();

    if (response.ok) console.log("Protected access successful");
    else console.log(`Proctected access failed: ${data.msg}`);
  } catch (err) {
    console.error(`Operation Failed: ${err.message}`);
  }
}

async function setTask(taskId, status, title) {
  try {
    const response = await protectedApiFetch(`${API_BASE}/task/set/${taskId}`, {
      method: 'POST',
      body: JSON.stringify({
        title: title,
        status: status,
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();

    if (response.ok) {
      console.log(`Updated task ${taskId}`);
      getTasks();
    }
    else console.log(`Proctected access failed: ${data.msg}`);
  } catch (err) {
    console.error(`Operation Failed: ${err.message}`);
  }
}

async function newTask() {
  try {
    const response = await protectedApiFetch(`${API_BASE}/task/new`, {
      method: 'POST',
      body: JSON.stringify({
        title: $('input#taskTitle').val(),
        status: $('select#status').val(),
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();

    if (response.ok) console.log("Protected access successful");
    else console.log(`Proctected access failed: ${data.msg}`);

    getTasks();
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
      getTasks();
    }
    else console.log(`Proctected access failed: ${data.msg}`);
  } catch (err) {
    console.error(`Operation Failed: ${err.message}`);
  }
}

getTasks();

function inputChanged(e) {
  console.log(e);
  let container = e.target.parentElement;
  let taskId = container.getAttribute("data-uuid");
  let status = container.querySelector("select").value;
  let title = container.querySelector("input.title").value;
  console.log(taskId, status, title);
  setTask(taskId, status, title);
}

