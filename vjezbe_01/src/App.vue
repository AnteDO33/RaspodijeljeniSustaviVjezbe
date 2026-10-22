
<script setup>
import { ref, computed, watch } from 'vue'

const STORAGE_KEY = 'taskflow-tasks'

function loadTasks() {
  try {
    const stored = JSON.parse(localStorage.getItem(STORAGE_KEY))
    return Array.isArray(stored) ? stored : []
  } catch {
    return []
  }
}

const tasks = ref(loadTasks())
const newTask = ref('')
const filter = ref('all')
const editingId = ref(null)
const editText = ref('')

watch(
  tasks,
  value => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(value))
  },
  { deep: true }
)

const total = computed(() => tasks.value.length)
const completed = computed(() =>
  tasks.value.filter(task => task.completed).length
)
const remaining = computed(() => total.value - completed.value)
const progress = computed(() =>
  total.value === 0 ? 0 : Math.round(completed.value / total.value * 100)
)

const filteredTasks = computed(() => {
  if (filter.value === 'active') {
    return tasks.value.filter(task => !task.completed)
  }
  if (filter.value === 'completed') {
    return tasks.value.filter(task => task.completed)
  }
  return tasks.value
})

function addTask() {
  const text = newTask.value.trim()
  if (!text) return

  tasks.value.unshift({
    id: crypto.randomUUID(),
    text,
    completed: false,
    createdAt: new Date().toISOString()
  })

  newTask.value = ''
}

function toggleTask(task) {
  task.completed = !task.completed
}

function deleteTask(id) {
  tasks.value = tasks.value.filter(task => task.id !== id)
  if (editingId.value === id) cancelEdit()
}

function startEdit(task) {
  editingId.value = task.id
  editText.value = task.text
}

function saveEdit(id) {
  const text = editText.value.trim()
  if (!text) return

  const task = tasks.value.find(task => task.id === id)
  if (task) task.text = text

  cancelEdit()
}

function cancelEdit() {
  editingId.value = null
  editText.value = ''
}

function clearCompleted() {
  tasks.value = tasks.value.filter(task => !task.completed)
  cancelEdit()
}

const filters = [
  { id: 'all', label: 'Svi zadaci' },
  { id: 'active', label: 'Aktivni' },
  { id: 'completed', label: 'Dovršeni' }
]
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand">
        <span class="brand-symbol">✦</span>
        <span>taskflow<span class="brand-dot">.</span></span>
      </div>

      <div class="sidebar-section">
        <span class="sidebar-label">RADNI PROSTOR</span>
        <button class="nav-item active">
          <span>▦</span> Moji zadaci
        </button>
      </div>

      <div class="sidebar-bottom">
        <div class="tip-card">
          <div class="tip-icon">✧</div>
          <strong>Ostani fokusiran.</strong>
          <p>Veliki ciljevi počinju malim koracima.</p>
        </div>
        <div class="sidebar-footer">TaskFlow © 2026</div>
      </div>
    </aside>

    <main class="main-content">
      <header class="topbar">
        <span class="breadcrumb">Radni prostor <span>/</span> Moji zadaci</span>
        <span class="today-label">
          {{ new Date().toLocaleDateString('hr-HR', {
            day: 'numeric', month: 'long', year: 'numeric'
          }) }}
        </span>
      </header>

      <div class="content">
        <div class="welcome">
          <div>
            <div class="eyebrow">TVOJ OSOBNI PROSTOR</div>
            <h1>Moji zadaci <span class="title-star">✳</span></h1>
            <p>Organiziraj svoj dan, jedan zadatak po jedan.</p>
          </div>
          <div class="welcome-icon">✦</div>
        </div>

        <section class="stats-grid">
          <div class="stat-card">
            <span class="stat-label">Ukupno zadataka</span>
            <strong>{{ total }}</strong>
            <span class="stat-bottom">Svi tvoji zadaci</span>
          </div>
          <div class="stat-card">
            <span class="stat-label">Za napraviti</span>
            <strong>{{ remaining }}</strong>
            <span class="stat-bottom">Još malo truda!</span>
          </div>
          <div class="stat-card">
            <span class="stat-label">Dovršeno</span>
            <strong>{{ completed }}</strong>
            <span class="stat-bottom">Odličan napredak!</span>
          </div>
        </section>

        <section class="progress-card">
          <div class="progress-heading">
            <div>
              <h3>Tvoj napredak</h3>
              <p>{{ completed }} od {{ total }} zadataka dovršeno</p>
            </div>
            <strong>{{ progress }}%</strong>
          </div>
          <div
            class="progress-track"
            role="progressbar"
            :aria-valuenow="progress"
            aria-valuemin="0"
            aria-valuemax="100"
            aria-label="Napredak dovršenih zadataka"
          >
            <div class="progress-fill" :style="{ width: progress + '%' }"></div>
          </div>
        </section>

        <section class="tasks-section">
          <div class="section-heading">
            <div>
              <h2>Popis zadataka</h2>
              <p>Što danas želiš napraviti?</p>
            </div>
            <span class="task-count">{{ total }} zadataka</span>
          </div>

          <form class="add-form" @submit.prevent="addTask">
            <span class="add-plus">＋</span>
            <input
              v-model="newTask"
              type="text"
              maxlength="200"
              placeholder="Dodaj novi zadatak..."
              aria-label="Novi zadatak"
            />
            <button class="primary-btn" type="submit" :disabled="!newTask.trim()">
              + Dodaj zadatak
            </button>
          </form>

          <div class="task-toolbar">
            <div class="filters">
              <button
                v-for="item in filters"
                :key="item.id"
                :class="['filter-btn', { selected: filter === item.id }]"
                @click="filter = item.id"
              >
                {{ item.label }}
              </button>
            </div>
            <button
              v-if="completed > 0"
              class="clear-btn"
              @click="clearCompleted"
            >
              Očisti dovršene
            </button>
          </div>

          <div v-if="filteredTasks.length === 0" class="empty-state">
            <div class="empty-icon">✳</div>
            <h3>Nema zadataka</h3>
            <p v-if="filter === 'all'">
              Dodaj svoj prvi zadatak i započni produktivan dan.
            </p>
            <p v-else>Trenutno nema zadataka u ovoj kategoriji.</p>
          </div>

          <div v-else class="task-list">
            <div
              v-for="task in filteredTasks"
              :key="task.id"
              :class="['task-item', { done: task.completed }]"
            >
              <template v-if="editingId === task.id">
                <form class="edit-form" @submit.prevent="saveEdit(task.id)">
                  <input
                    v-model="editText"
                    maxlength="200"
                    aria-label="Uredi zadatak"
                    @keyup.esc="cancelEdit"
                  />
                  <button type="submit" class="save-btn">Spremi</button>
                  <button type="button" class="cancel-btn" @click="cancelEdit">
                    Odustani
                  </button>
                </form>
              </template>

              <template v-else>
                <input
                  class="task-checkbox"
                  type="checkbox"
                  :checked="task.completed"
                  :aria-label="'Označi zadatak: ' + task.text"
                  @change="toggleTask(task)"
                />
                <span class="task-text">{{ task.text }}</span>
                <div class="task-actions">
                  <button
                    class="icon-btn"
                    :aria-label="'Uredi ' + task.text"
                    title="Uredi zadatak"
                    @click="startEdit(task)"
                  >✎</button>
                  <button
                    class="icon-btn delete-btn"
                    :aria-label="'Izbriši ' + task.text"
                    title="Izbriši zadatak"
                    @click="deleteTask(task.id)"
                  >✕</button>
                </div>
              </template>
            </div>
          </div>
        </section>

        <footer class="main-footer">
          Napravljeno s Vue 3 + Vite · Podaci se čuvaju lokalno
        </footer>
      </div>
    </main>
  </div>
</template>
