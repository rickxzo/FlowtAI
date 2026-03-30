<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoggedIn = ref(false)

const checkUser = async () => {
  try {
    const res = await fetch('https://flowt-ai-j152.onrender.com/logged-in', { credentials: 'include' })
    const data = await res.json()
    isLoggedIn.value = data.logged_in
    console.log(data)
  } catch (err) {
    console.error(err)
  }
}

const handleAuth = async () => {
  if (isLoggedIn.value) {
    await fetch('https://flowt-ai-j152.onrender.com/logout', { method: 'POST', credentials: 'include' })
    isLoggedIn.value = false
    router.push('/')
  } else {
    router.push('/login')
  }
}

onMounted(() => {
  checkUser()
})
</script>

<template>
  <div class="fixed top-4 left-0 w-full flex justify-center z-50" style="font-family: 'Space Grotesk';">
    <div
      class="flex items-center justify-between gap-8 px-6 py-3
             bg-black/20 backdrop-blur-md text-white
             rounded-full shadow-lg border border-white/10
             w-[50%] max-w-5xl"
    >
      <!-- Left: Logo -->
      <div class="font-semibold text-lg tracking-wide" style="font-family: 'Shadows Into Light Two';">
        <router-link to="/" class="hover:text-white transition">flowt.ai</router-link>
      </div>

      <!-- Middle: Links -->
      <div class="hidden md:flex gap-6 text-sm text-gray-300">
        <router-link to="/agents" class="hover:text-white transition">Agents</router-link>
        <router-link to="/models" class="hover:text-white transition">Models</router-link>
        <router-link to="/billing" class="hover:text-white transition">Billing</router-link>
        <router-link to="/docs" class="hover:text-white transition">Docs</router-link>
      </div>

      <!-- Right: Auth -->
      <button
        @click="handleAuth"
        class="px-4 py-1.5 rounded-full bg-white text-black text-sm font-medium hover:scale-105 transition"
      >
        {{ isLoggedIn ? 'Logout' : 'Login' }}
      </button>
    </div>
  </div>
</template>
