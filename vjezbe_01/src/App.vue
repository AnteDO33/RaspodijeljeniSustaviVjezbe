
<script setup>
import { ref, computed, onMounted } from 'vue'
import { taskApi } from './services/api'

// ===== PODACI =====

const tasks = ref([])
const newTask = ref('')
const filter = ref('all')
const editingId = ref(null)
const editText = ref('')

const loading = ref(true)
const errorMessage = ref('')
const saving = ref(false)

// ===== STATISTIKA =====

const total = computed(() => tasks.value.length)

const completed = computed(() =>
  tasks.value.filter(task => task.completed).length
)

const remaining = computed(() =>
  total.value - completed.value
)

const progress = computed(() =>
  total.value === 0
    ? 0
    : Math.round((completed.value / total.value) * 100)
)

// ===== FILTERI =====

const filters = [
  { id: 'all', label: 'Svi zadaci' },
  { id: 'active', label: 'Aktivni' },
  { id: 'completed', label: 'Dovršeni' }
]

const filteredTasks = computed(() => {
  if (filter.value === 'active') {
    return tasks.value.filter(task => !task.completed)
  }

  if (filter.value === 'completed') {
    return tasks.value.filter(task => task.completed)
  }

  return tasks.value
})

// ===== REST API =====

// GET /api/tasks
async function loadTasks() {
  loading.value = true
  errorMessage.value = ''

  try {
    tasks.value = await taskApi.getAll()
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    loading.value = false
  }
}

onMounted(loadTasks)

// POST /api/tasks
async function addTask() {
  const text = newTask.value.trim()

  if (!text || saving.value) return

  saving.value = true
  errorMessage.value = ''

  try {
    const task = await taskApi.create(text)

    tasks.value.unshift(task)
    newTask.value = ''
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    saving.value = false
  }
}

// PATCH /api/tasks/:id
async function toggleTask(task) {
  if (saving.value) return

  saving.value = true

  try {
    const updated = await taskApi.update(task.id, {
      completed: !task.completed
    })

    Object.assign(task, updated)
    errorMessage.value = ''
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    saving.value = false
  }
}

// DELETE /api/tasks/:id
async function deleteTask(id) {
  if (saving.value) return

  saving.value = true

  try {
    await taskApi.remove(id)

    tasks.value = tasks.value.filter(
      task => task.id !== id
    )

    if (editingId.value === id) {
      cancelEdit()
    }

    errorMessage.value = ''
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    saving.value = false
  }
}

// ===== UREĐIVANJE ZADATKA =====

function startEdit(task) {
  editingId.value = task.id
  editText.value = task.text
}

// PATCH /api/tasks/:id
async function saveEdit(id) {
  const text = editText.value.trim()

  if (!text || saving.value) return

  saving.value = true

  try {
    const updated = await taskApi.update(id, { text })

    const task = tasks.value.find(
      task => task.id === id
    )

    if (task) {
      Object.assign(task, updated)
    }

    cancelEdit()
    errorMessage.value = ''
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    saving.value = false
  }
}

function cancelEdit() {
  editingId.value = null
  editText.value = ''
}

// ===== BRISANJE DOVRŠENIH =====

async function clearCompleted() {
  if (saving.value) return

  saving.value = true

  const completedTasks = tasks.value.filter(
    task => task.completed
  )

  try {
    const results = await Promise.allSettled(
      completedTasks.map(task =>
        taskApi.remove(task.id)
      )
    )

    const deletedIds = completedTasks
      .filter((_, index) =>
        results[index].status === 'fulfilled'
      )
      .map(task => task.id)

    tasks.value = tasks.value.filter(
      task => !deletedIds.includes(task.id)
    )

    cancelEdit()

    errorMessage.value = results.some(
      result => result.status === 'rejected'
    )
      ? 'Neke zadatke nije moguće izbrisati.'
      : ''
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="app-shell">

    <!-- ===== SIDEBAR ===== -->

    <aside class="sidebar">

      <div class="brand">
        <span class="brand-symbol">✦</span>
        <span>
          taskflow<span class="brand-dot">.</span>
        </span>
      </div>

      <div class="sidebar-section">
        <span class="sidebar-label">
          RADNI PROSTOR
        </span>

        <button class="nav-item active">
          <span>▦</span>
          Moji zadaci
        </button>
      </div>

      <div class="sidebar-bottom">
        <div class="tip-card">
          <div class="tip-icon">✧</div>

          <strong>Ostani fokusiran.</strong>

          <p>
            Veliki ciljevi počinju malim koracima.
          </p>
        </div>

        <div class="sidebar-footer">
          TaskFlow © 2026
        </div>
      </div>

    </aside>

    <!-- ===== GLAVNI SADRŽAJ ===== -->

    <main class="main-content">

      <header class="topbar">
        <span class="breadcrumb">
          Radni prostor
          <span>/</span>
          Moji zadaci
        </span>

        <span class="today-label">
          {{
            new Date().toLocaleDateString('hr-HR', {
              day: 'numeric',
              month: 'long',
              year: 'numeric'
            })
          }}
        </span>
      </header>

      <div class="content">

        <!-- ===== NASLOV ===== -->

        <div class="welcome">

          <div>
            <div class="eyebrow">
              TVOJ OSOBNI PROSTOR
            </div>

            <h1>
              Moji zadaci
              <span class="title-star">✳</span>
            </h1>

            <p>
              Organiziraj svoj dan,
              jedan zadatak po jedan.
            </p>
          </div>

          <div class="welcome-icon">✦</div>

        </div>

        <!-- ===== STATISTIKA ===== -->

        <section class="stats-grid">

          <div class="stat-card">
            <span class="stat-label">
              Ukupno zadataka
            </span>

            <strong>{{ total }}</strong>

            <span class="stat-bottom">
              Svi tvoji zadaci
            </span>
          </div>

          <div class="stat-card">
            <span class="stat-label">
              Za napraviti
            </span>

            <strong>{{ remaining }}</strong>

            <span class="stat-bottom">
              Još malo truda!
            </span>
          </div>

          <div class="stat-card">
            <span class="stat-label">
              Dovršeno
            </span>

            <strong>{{ completed }}</strong>

            <span class="stat-bottom">
              Odličan napredak!
            </span>
          </div>

        </section>

        <!-- ===== PROGRESS BAR ===== -->

        <section class="progress-card">

          <div class="progress-heading">

            <div>
              <h3>Tvoj napredak</h3>

              <p>
                {{ completed }} od {{ total }}
                zadataka dovršeno
              </p>
            </div>

            <strong>{{ progress }}%</strong>

          </div>

          <div
            class="progress-track"
            role="progressbar"
            :aria-valuenow="progress"
            aria-valuemin="0"
            aria-valuemax="100"
            aria-label="Napredak zadataka"
          >
            <div
              class="progress-fill"
              :style="{ width: progress + '%' }"
            ></div>
          </div>

        </section>

        <!-- ===== NOVO: API STATUS ===== -->

        <div
          v-if="loading"
          class="api-message"
          role="status"
        >
          Učitavanje zadataka s REST API-ja...
        </div>

        <div
          v-if="errorMessage"
          class="api-error"
          role="alert"
        >
          <span>{{ errorMessage }}</span>

          <button @click="loadTasks">
            Pokušaj ponovno
          </button>
        </div>

        <!-- ===== POPIS ZADATAKA ===== -->

        <section class="tasks-section">

          <div class="section-heading">

            <div>
              <h2>Popis zadataka</h2>

              <p>
                Što danas želiš napraviti?
              </p>
            </div>

            <span class="task-count">
              {{ total }} zadataka
            </span>

          </div>

          <!-- ===== DODAVANJE ===== -->

          <form
            class="add-form"
            @submit.prevent="addTask"
          >

            <span class="add-plus">＋</span>

            <input
              v-model="newTask"
              type="text"
              maxlength="200"
              placeholder="Dodaj novi zadatak..."
              aria-label="Novi zadatak"
            />

            <button
              class="primary-btn"
              type="submit"
              :disabled="!newTask.trim() || saving || loading"
            >
              {{ saving ? 'Spremanje...' : '+ Dodaj zadatak' }}
            </button>

          </form>

          <!-- ===== FILTERI ===== -->

          <div class="task-toolbar">

            <div class="filters">

              <button
                v-for="item in filters"
                :key="item.id"
                :class="[
                  'filter-btn',
                  { selected: filter === item.id }
                ]"
                @click="filter = item.id"
              >
                {{ item.label }}
              </button>

            </div>

            <button
              v-if="completed > 0"
              class="clear-btn"
              :disabled="saving || loading"
              @click="clearCompleted"
            >
              Očisti dovršene
            </button>

          </div>

          <!-- ===== PRAZNA LISTA ===== -->

          <div
            v-if="!loading && !errorMessage && filteredTasks.length === 0"
            class="empty-state"
          >

            <div class="empty-icon">✳</div>

            <h3>Nema zadataka</h3>

            <p v-if="filter === 'all'">
              Dodaj svoj prvi zadatak i započni
              produktivan dan.
            </p>

            <p v-else>
              Trenutno nema zadataka
              u ovoj kategoriji.
            </p>

          </div>

          <!-- ===== PRIKAZ ZADATAKA ===== -->

          <div
            v-else-if="!loading"
            class="task-list"
          >

            <div
              v-for="task in filteredTasks"
              :key="task.id"
              :class="[
                'task-item',
                { done: task.completed }
              ]"
            >

              <!-- UREĐIVANJE -->

              <template v-if="editingId === task.id">

                <form
                  class="edit-form"
                  @submit.prevent="saveEdit(task.id)"
                >

                  <input
                    v-model="editText"
                    maxlength="200"
                    aria-label="Uredi zadatak"
                    @keyup.esc="cancelEdit"
                  />

                  <button
                    type="submit"
                    class="save-btn"
                    :disabled="saving || !editText.trim()"
                  >
                    Spremi
                  </button>

                  <button
                    type="button"
                    class="cancel-btn"
                    @click="cancelEdit"
                  >
                    Odustani
                  </button>

                </form>

              </template>

              <!-- NORMALNI PRIKAZ -->

              <template v-else>

                <input
                  class="task-checkbox"
                  type="checkbox"
                  :checked="task.completed"
                  :disabled="saving"
                  :aria-label="'Označi zadatak: ' + task.text"
                  @change="toggleTask(task)"
                />

                <span class="task-text">
                  {{ task.text }}
                </span>

                <div class="task-actions">

                  <button
                    class="icon-btn"
                    :disabled="saving"
                    :aria-label="'Uredi ' + task.text"
                    title="Uredi zadatak"
                    @click="startEdit(task)"
                  >
                    ✎
                  </button>

                  <button
                    class="icon-btn delete-btn"
                    :disabled="saving"
                    :aria-label="'Izbriši ' + task.text"
                    title="Izbriši zadatak"
                    @click="deleteTask(task.id)"
                  >
                    ✕
                  </button>

                </div>

              </template>

            </div>

          </div>

        </section>

        <!-- ===== FOOTER ===== -->

        <footer class="main-footer">
          Napravljeno s Vue 3 + Vite ·
          Povezano s Express.js REST API-jem
        </footer>

      </div>

    </main>

  </div>
</template>
