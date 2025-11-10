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

getTasks();