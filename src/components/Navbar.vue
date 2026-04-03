<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoggedIn = ref(false)
const isOpen = ref(false)

const checkUser = async () => {
  try {
    const res = await fetch('https://flowtai-1.onrender.com/logged-in', { credentials: 'include' })
    const data = await res.json()
    isLoggedIn.value = data.logged_in
  } catch (err) {
    console.error(err)
  }
}

const handleAuth = async () => {
  if (isLoggedIn.value) {
    await fetch('https://flowtai-1.onrender.com/logout', { method: 'POST', credentials: 'include' })
    isLoggedIn.value = false
    router.push('/')
  } else {
    router.push('/login')
  }
}

onMounted(checkUser)
</script>

<template>
  <div class="fixed top-4 left-0 w-full flex justify-center z-50 px-3 sm:px-0" style="font-family: 'Space Grotesk';">
    
    <div
      class="w-full sm:w-[90%] md:w-[70%] lg:w-[50%] max-w-5xl
             flex items-center justify-between px-4 sm:px-6 py-3
             bg-black/20 backdrop-blur-md text-white
             rounded-full shadow-lg border border-white/10"
    >
      
      <!-- Logo -->
      <div class="font-semibold text-lg tracking-wide" style="font-family: 'Shadows Into Light Two';">
        <router-link to="/">flowt.ai</router-link>
      </div>

      <!-- Desktop Links -->
      <div class="hidden md:flex gap-6 text-sm text-gray-300">
        <router-link to="/agents" class="hover:text-white transition">Agents</router-link>
        <router-link to="/models" class="hover:text-white transition">Models</router-link>
        <router-link to="/billing" class="hover:text-white transition">Billing</router-link>
        <router-link to="/docs" class="hover:text-white transition">Docs</router-link>
      </div>

      <!-- Desktop Auth -->
      <button
        @click="handleAuth"
        class="hidden md:block px-4 py-1.5 rounded-full bg-white text-black text-sm font-medium hover:scale-105 transition"
      >
        {{ isLoggedIn ? 'Logout' : 'Login' }}
      </button>

      <!-- Mobile Hamburger -->
      <button
        class="md:hidden text-white text-xl"
        @click="isOpen = !isOpen"
      >
        ☰
      </button>
    </div>

    <!-- Mobile Menu -->
    <div
      v-if="isOpen"
      class="absolute top-20 w-[90%] bg-black/90 backdrop-blur-md text-white
             rounded-2xl border border-white/10 p-6 flex flex-col gap-4 md:hidden"
    >
      <router-link to="/agents" @click="isOpen = false">Agents</router-link>
      <router-link to="/models" @click="isOpen = false">Models</router-link>
      <router-link to="/billing" @click="isOpen = false">Billing</router-link>
      <router-link to="/docs" @click="isOpen = false">Docs</router-link>

      <button
        @click="handleAuth"
        class="mt-2 px-4 py-2 rounded-full bg-white text-black text-sm font-medium"
      >
        {{ isLoggedIn ? 'Logout' : 'Login' }}
      </button>
    </div>

  </div>
</template>
