
const express = require('express')
const cors = require('cors')
const { randomUUID } = require('node:crypto')

// ===== POSTAVKE POSLUŽITELJA =====

const app = express()
const PORT = process.env.PORT || 3000

// Middleware
app.use(cors())
app.use(express.json({ limit: '20kb' }))

// ===== PODACI =====

// Privremena pohrana zadataka u memoriji
let tasks = [
  {
    id: randomUUID(),
    text: 'Naučiti Express.js',
    completed: false
  },
  {
    id: randomUUID(),
    text: 'Deployati API na Render',
    completed: false
  },
  {
    id: randomUUID(),
    text: 'Povezati Vue i REST API',
    completed: false
  }
]

// ===== POČETNA STRANICA =====

// GET /
app.get('/', (req, res) => {
  res.status(200).json({
    name: 'TaskFlow REST API',
    version: '1.0.0',
    status: 'online',
    message: 'Dobrodošli na TaskFlow REST API!',
    framework: 'Express.js',
    endpoints: {
      home: 'GET /',
      health: 'GET /api/health',
      getTasks: 'GET /api/tasks',
      createTask: 'POST /api/tasks',
      updateTask: 'PATCH /api/tasks/:id',
      deleteTask: 'DELETE /api/tasks/:id'
    }
  })
})

// ===== PROVJERA STANJA API-JA =====

// GET /api/health
app.get('/api/health', (req, res) => {
  res.status(200).json({
    status: 'ok',
    message: 'TaskFlow API radi!'
  })
})

// ===== DOHVATI SVE ZADATKE =====

// GET /api/tasks
app.get('/api/tasks', (req, res) => {
  res.status(200).json(tasks)
})

// ===== DODAJ NOVI ZADATAK =====

// POST /api/tasks
app.post('/api/tasks', (req, res) => {
  const text = req.body?.text

  // Provjera unesenih podataka
  if (
    typeof text !== 'string' ||
    !text.trim() ||
    text.length > 200
  ) {
    return res.status(400).json({
      error: 'Tekst zadatka mora imati između 1 i 200 znakova.'
    })
  }

  // Kreiranje novog zadatka
  const task = {
    id: randomUUID(),
    text: text.trim(),
    completed: false
  }

  // Dodavanje na početak popisa
  tasks.unshift(task)

  // Uspješno kreiranje
  res.status(201).json(task)
})

// ===== UREDI ZADATAK =====

// PATCH /api/tasks/:id
app.patch('/api/tasks/:id', (req, res) => {
  const task = tasks.find(
    t => t.id === req.params.id
  )

  // Zadatak ne postoji
  if (!task) {
    return res.status(404).json({
      error: 'Zadatak nije pronađen.'
    })
  }

  const { text, completed } = req.body || {}

  // Provjera jesu li poslani podaci
  if (
    text === undefined &&
    completed === undefined
  ) {
    return res.status(400).json({
      error: 'Nema podataka za ažuriranje.'
    })
  }

  // Ažuriranje teksta
  if (text !== undefined) {
    if (
      typeof text !== 'string' ||
      !text.trim() ||
      text.length > 200
    ) {
      return res.status(400).json({
        error: 'Neispravan tekst zadatka.'
      })
    }

    task.text = text.trim()
  }

  // Ažuriranje statusa zadatka
  if (completed !== undefined) {
    if (typeof completed !== 'boolean') {
      return res.status(400).json({
        error: 'completed mora biti boolean.'
      })
    }

    task.completed = completed
  }

  res.status(200).json(task)
})

// ===== IZBRIŠI ZADATAK =====

// DELETE /api/tasks/:id
app.delete('/api/tasks/:id', (req, res) => {
  const index = tasks.findIndex(
    t => t.id === req.params.id
  )

  // Zadatak ne postoji
  if (index === -1) {
    return res.status(404).json({
      error: 'Zadatak nije pronađen.'
    })
  }

  // Brisanje zadatka
  tasks.splice(index, 1)

  // Uspješno brisanje bez sadržaja
  res.status(204).send()
})

// ===== NEPOSTOJEĆI ENDPOINT =====

app.use((req, res) => {
  res.status(404).json({
    error: 'Endpoint ne postoji.',
    path: req.originalUrl
  })
})

// ===== OBRADA GREŠAKA =====

app.use((err, req, res, next) => {
  // Neispravan JSON iz Postmana ili curl-a
  if (
    err.status === 400 &&
    err.type === 'entity.parse.failed'
  ) {
    return res.status(400).json({
      error: 'Neispravan JSON format.',
      message: 'Provjeri navodnike, zagrade i JSON sadržaj.'
    })
  }

  // Prevelik zahtjev
  if (err.status === 413) {
    return res.status(413).json({
      error: 'Poslani podaci su preveliki.'
    })
  }

  // Ostale greške
  console.error('Greška poslužitelja:', err)

  res.status(500).json({
    error: 'Interna greška poslužitelja.'
  })
})

// ===== POKRETANJE POSLUŽITELJA =====

app.listen(PORT, '0.0.0.0', () => {
  console.log('================================')
  console.log('TaskFlow REST API')
  console.log(`Port: ${PORT}`)
  console.log('Status: Online')
  console.log('================================')
})
