// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// Lazy-loaded pages (IMPORTANT for performance)
const Home = () => import(/* webpackPrefetch: true */ '../views/Homme.vue')
const Login = () => import(/* webpackPrefetch: true */ '../views/Login.vue')
const Signup = () => import(/* webpackPrefetch: true */ '../views/Signup.vue')
const Models = () => import (/* webpackPrefetch: true */ '../views/Models.vue')
const Agents = () => import (/* webpackPrefetch: true */ '../views/Agents.vue')
const Docs = () => import (/* webpackPrefetch: true */ '../views/Docs.vue')
const Billing = () => import (/* webpackPrefetch: true */ '../views/Billing.vue')

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
