<script setup>
import { ref, onMounted } from 'vue'

const amounts = [150, 300, 500, 1000, 2000, 5000]
const selected = ref(150)

const loggedIn = ref(null) // null = loading, true/false after fetch
const username = ref("")

const balance = ref(null)

const fetchBalance = async () => {
  try {
    const res = await fetch("https://flowtai-1.onrender.com/balance", {
      credentials: "include"
    })
    const data = await res.json()

    balance.value = data.balance
  } catch (err) {
    console.error(err)
    balance.value = 0
  }
}

const checkAuth = async () => {
  try {
    const res = await fetch("https://flowtai-1.onrender.com/logged-in", {
      credentials: "include"
    })
    const data = await res.json()

    loggedIn.value = data.logged_in
    username.value = data.username || ""
  } catch (err) {
    console.error(err)
    loggedIn.value = false
  }
}

onMounted(async () => {
  checkAuth()
  fetchBalance()
})

const pay = () => {
  window.location.href = "https://imjo.in/a4Yg6w"
}

const selectAmount = (amount) => {
  selected.value = amount
}

const formatAmount = (amount) => {
  if (amount === "custom") return "Custom"
  return "₹" + amount.toLocaleString()
}

const cardClass = (amount) => {
  const isSelected = selected.value === amount

  return [
    "border p-10 text-center cursor-pointer transition-all duration-150 text-xl",
    isSelected
      ? "border-white"
      : "border-zinc-800 hover:border-zinc-600 text-gray-300"
  ]
}
</script>
<template>
  <div class="min-h-[90vh] bg-zinc-950 text-white px-6 py-10 mt-16">

    <!-- Loading State -->
    <div v-if="loggedIn === null" class="text-center text-gray-400">
      Checking authentication...
    </div>

    <!-- Not Logged In -->
    <div v-else-if="!loggedIn" class="max-w-4xl mx-auto text-center mt-20">
      <p class="text-xl text-gray-300">
        Billing information is only available if logged in
      </p>
    </div>

    <!-- Logged In -->
    <div v-else>

      <!-- Balance Section -->
      <div class="max-w-4xl mx-auto mb-6">
        <div class="border border-zinc-800 p-6 flex justify-between items-center bg-zinc-900/40">
          
          <div>
            <p class="text-gray-400 text-sm">Current Balance</p>
            <p class="text-2xl font-semibold mt-1">
              {{ balance !== null ? "₹" + balance.toFixed(2) : "Loading..." }}
            </p>
          </div>
      
          <div class="text-right text-sm text-gray-500">
            Available credits
          </div>
      
        </div>
      </div>

      <!-- Header -->
      <div class="max-w-4xl mx-auto mb-8">
        <h1 class="text-3xl font-semibold">
          <span class="text-gray-400 underline cursor-pointer" style="font-family:'Space Grotesk';">
            Billing
          </span>
          <span class="text-gray-500"> / </span>
          <span>Add credit</span>
        </h1>
        <p class="text-gray-500 mt-1">Welcome, {{ username }}</p>
      </div>

      <!-- Credit Section -->
      <div class="max-w-4xl mx-auto">
        <p class="text-gray-300 mb-4 font-medium" style="font-family:'Space Grotesk';">
          Credit amount
        </p>

        <div class="grid grid-cols-3 gap-4">
          <div
            v-for="(amount, index) in amounts"
            :key="index"
            @click="selectAmount(amount)"
            :class="cardClass(amount)"
          >
            {{ formatAmount(amount) }}
          </div>
        </div>
      </div>

      <!-- Footer Buttons -->
      <div class="max-w-4xl mx-auto mt-10 flex gap-4">
        <button class="border border-gray-500 px-6 py-3 text-white hover:bg-white/5 transition">
          Cancel
        </button>

        <button
          class="flex-1 bg-gray-200 text-black px-6 py-3 font-medium hover:bg-white transition"
          :disabled="!selected"
          @click="pay"
        >
          Buy {{ selected ? formatAmount(selected) : "₹0.00" }} in credit
        </button>
      </div>

    </div>
  </div>
</template>
