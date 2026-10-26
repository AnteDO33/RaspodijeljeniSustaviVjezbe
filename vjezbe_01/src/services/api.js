
/* ==========================================
   TASKFLOW - REST API SERVICE
   Vue 3 + Express.js + Render.com
========================================== */

// ===== API ADRESA =====

const API_URL = (
  import.meta.env.VITE_API_URL ||
  'https://raspodijeljenisustavivjezb.onrender.com'
).replace(/\/+$/, '')

// ===== HTTP REQUEST FUNKCIJA =====

async function request(path, options = {}) {
  let response

  try {
    response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: {
        ...(options.body !== undefined
          ? { 'Content-Type': 'application/json' }
          : {}),
        ...options.headers
      }
    })
  } catch (error) {
    console.error('Greška povezivanja s REST API-jem:', error)

    throw new Error(
      'Nije moguće povezati se s Render API poslužiteljem.'
    )
  }

  // Provjera HTTP statusa
  if (!response.ok) {
    const error = await response.json().catch(() => ({}))

    throw new Error(
      error.error || `HTTP greška: ${response.status}`
    )
  }

  // DELETE vraća 204 No Content
  if (response.status === 204) {
    return null
  }

  // Vraćanje JSON odgovora
  return response.json()
}

// ===== TASKFLOW REST API ENDPOINTOVI =====

export const taskApi = {

  // GET - Dohvati sve zadatke
  getAll: () => {
    return request('/api/tasks')
  },

  // POST - Dodaj novi zadatak
  create: (text) => {
    return request('/api/tasks', {
      method: 'POST',
      body: JSON.stringify({ text })
    })
  },

  // PATCH - Ažuriraj postojeći zadatak
  update: (id, data) => {
    return request(
      `/api/tasks/${encodeURIComponent(id)}`,
      {
        method: 'PATCH',
        body: JSON.stringify(data)
      }
    )
  },

  // DELETE - Izbriši zadatak
  remove: (id) => {
    return request(
      `/api/tasks/${encodeURIComponent(id)}`,
      {
        method: 'DELETE'
      }
    )
  }
}
