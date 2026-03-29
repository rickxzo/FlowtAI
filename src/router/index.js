// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// Lazy-loaded pages (IMPORTANT for performance)
import Home from '../views/Homme.vue'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import Models from '../views/Models.vue'
import Agents from '../views/Agents.vue'
import Docs from '../views/Docs.vue'
import Billing from '../views/Billing.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/signup-page', component: Signup},
  { path: '/models', component: Models},
  { path: '/agents', component: Agents},
  { path: '/docs', component: Docs},
  { path: '/billing', component: Billing}
  
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
