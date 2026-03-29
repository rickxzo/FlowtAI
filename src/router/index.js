// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// Lazy-loaded pages (IMPORTANT for performance)
const Home = () => import('../views/Homme.vue')
const Login = () => import('../views/Login.vue')
const Signup = () => import('../views/Signup.vue')
const Models = () => import ('../views/Models.vue')
const Agents = () => import ('../views/Agents.vue')
const Docs = () => import ('../views/Docs.vue')
const Billing = () => import ('../views/Billing.vue')

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