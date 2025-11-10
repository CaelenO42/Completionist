const API_BASE = '/api';

function getCookieValue(name) {
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i].trim();
    if (cookie.startsWith(name + '=')) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }
  return null;
}

function applyCsrfHeader(options, isRefreshRequest = false) {
  if (options.method === 'POST') {
    const token = isRefreshRequest ? getCookieValue("csrf_refresh_token") : getCookieValue("csrf_access_token");
    
    if (token) {
      options.headers = {
        ...options.headers,
        'X-CSRF-TOKEN': token
      };
    }
  }
}

async function protectedApiFetch(url, options = {}, isRetry = false) {
  console.log(`Attempting to fetch: ${url} (Retry: ${isRetry ? 'Yes' : 'No'})`);
  options.credentials = 'include';
  applyCsrfHeader(options);

  let response = await fetch(url, options);
  if (response.ok || response.status !== 401) return response;

  console.log("Access Token Expired. Attempting Refresh...");

  if (isRetry) {
    console.log("Refresh attempt failed on retry. Forcing log out.");
    window.location.href = '/account/signout';
    return;
  }

  const refreshUrl = `${API_BASE}/auth/refresh`;
  const refreshOptions = {
    method: 'POST',
    credentials: 'include',
    headers: {}
  }
  applyCsrfHeader(refreshOptions, true);

  console.log(`Calling Refresh Endpoint: ${refreshUrl}`);

  const refreshResponse = await fetch(refreshUrl, refreshOptions);

  if (!refreshResponse.ok) {
    console.log(`Refresh Failed (${refreshResponse.status}). Forcing log out.`);
    window.location.href = '/account/signout';
    return;
  }

  console.log("Refresh successful! Retrying original request...");
  return protectedApiFetch(url, options, true);
}

async function accessSet() {
  try {
    const response = await protectedApiFetch(`${API_BASE}/task/set`, {
      method: 'POST'
    });

    const data = await response.json();

    if (response.ok) console.log("Protected access successful");
    else console.log(`Proctected access failed: ${data.msg}`);
  } catch (err) {
    console.error(`Operation Failed: ${err.message}`);
  }
}