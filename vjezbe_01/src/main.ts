import './assets/main.css'

import { createApp } from 'vue'
import './style.css'
// @ts-expect-error Vue SFC typings are not configured in this project.
import App from './App.vue'

createApp(App).mount('#app')

