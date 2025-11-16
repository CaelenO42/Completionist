async function getTasks() {
  try {
    const response = await protectedApiFetch(`${API_BASE}/task/get`, {
      method: 'POST'
    });

    const data = await response.json();

    if (response.ok) console.log("Success");
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

async function newTask() {
  try {
    const response = await protectedApiFetch(`${API_BASE}/task/new`, {
      method: 'POST',
      body: JSON.stringify({
        title: $('input#taskTitle').val(),
        status: $('select').val(),
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

getTasks();