
const API_URL = (
  import.meta.env.VITE_API_URL || 'http://localhost:3000'
).replace(/\/$/, '')

async function request(path, options = {}) {
  let response

  try {
    response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    })
  } catch {
    throw new Error('Nije moguće povezati se s API poslužiteljem.')
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.error || `HTTP greška: ${response.status}`)
  }

  return response.status === 204 ? null : response.json()
}

export const taskApi = {
  getAll: () => request('/api/tasks'),

  create: text =>
    request('/api/tasks', {
      method: 'POST',
      body: JSON.stringify({ text })
    }),

  update: (id, data) =>
    request(`/api/tasks/${encodeURIComponent(id)}`, {
      method: 'PATCH',
      body: JSON.stringify(data)
    }),

  remove: id =>
    request(`/api/tasks/${encodeURIComponent(id)}`, {
      method: 'DELETE'
    })
}
