
const express = require('express')
const cors = require('cors')
const { randomUUID } = require('node:crypto')

const app = express()
const PORT = process.env.PORT || 3000

app.use(cors())
app.use(express.json({ limit: '20kb' }))

let tasks = [
  { id: randomUUID(), text: 'Naučiti Express.js', completed: false },
  { id: randomUUID(), text: 'Deployati API na Render', completed: false },
  { id: randomUUID(), text: 'Povezati Vue i REST API', completed: false }
]

// Provjera stanja API-ja
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    message: 'TaskFlow API radi!'
  })
})

// Dohvati sve zadatke
app.get('/api/tasks', (req, res) => {
  res.json(tasks)
})

// Dodaj novi zadatak
app.post('/api/tasks', (req, res) => {
  const text = req.body?.text

  if (typeof text !== 'string' || !text.trim() || text.length > 200) {
    return res.status(400).json({
      error: 'Tekst zadatka mora imati između 1 i 200 znakova.'
    })
  }

  const task = {
    id: randomUUID(),
    text: text.trim(),
    completed: false
  }

  tasks.unshift(task)
  res.status(201).json(task)
})

// Uredi zadatak ili njegov status
app.patch('/api/tasks/:id', (req, res) => {
  const task = tasks.find(t => t.id === req.params.id)
  if (!task) return res.status(404).json({ error: 'Zadatak nije pronađen.' })

  const { text, completed } = req.body || {}

  if (text === undefined && completed === undefined) {
    return res.status(400).json({ error: 'Nema podataka za ažuriranje.' })
  }

  if (text !== undefined) {
    if (typeof text !== 'string' || !text.trim() || text.length > 200) {
      return res.status(400).json({ error: 'Neispravan tekst zadatka.' })
    }
    task.text = text.trim()
  }

  if (completed !== undefined) {
    if (typeof completed !== 'boolean') {
      return res.status(400).json({ error: 'completed mora biti boolean.' })
    }
    task.completed = completed
  }

  res.json(task)
})

// Izbriši zadatak
app.delete('/api/tasks/:id', (req, res) => {
  const index = tasks.findIndex(t => t.id === req.params.id)
  if (index === -1) {
    return res.status(404).json({ error: 'Zadatak nije pronađen.' })
  }

  tasks.splice(index, 1)
  res.status(204).send()
})

// Endpoint nije pronađen
app.use((req, res) => {
  res.status(404).json({ error: 'Endpoint ne postoji.' })
})

app.listen(PORT, '0.0.0.0', () => {
  console.log(`TaskFlow API pokrenut na portu ${PORT}`)
})
