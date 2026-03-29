<script setup>
import Navbar from '../components/Navbar.vue'
import { ref, computed, onMounted } from 'vue'

const models = ref([])
const search = ref('')
const sort = ref('')
const selected = ref(null)

const loadModels = async () => {
  try {
    const res = await fetch('https://flowt-ai-j152.onrender.com/show-models')
    const data = await res.json()
    models.value = data.models
  } catch (err) {
    console.error('Failed to load models', err)
  }
}

const filteredModels = computed(() => {
  let result = models.value.filter(m =>
    m.name.toLowerCase().includes(search.value.toLowerCase())
  )

  if (sort.value === 'input') {
    result.sort((a, b) => a.input - b.input)
  }

  if (sort.value === 'output') {
    result.sort((a, b) => a.output - b.output)
  }

  return result
})

const open = (m) => {
  selected.value = m
}

onMounted(loadModels)
</script>

<template>
  <div class="h-screen flex flex-col bg-zinc-950 text-white pt-20" style="font-family: 'Space Grotesk';">

    <!-- NAVBAR -->
    <Navbar />

    <!-- CONTENT WRAPPER -->
    <div class="flex-1 flex flex-col overflow-hidden">

      <!-- HEADER -->
      <div class="max-w-7xl mx-auto px-8 py-6 w-full flex justify-between items-center">

        <h1 class="text-2xl font-semibold" style="font-family: 'Space Grotesk';">
          Models
        </h1>

        <div class="flex gap-4">

          <input
            v-model="search"
            placeholder="search models..."
            class="bg-zinc-900 border border-zinc-800 px-4 py-2 rounded-lg outline-none"
          />

          <select
            v-model="sort"
            class="bg-zinc-900 border border-zinc-800 px-4 py-2 rounded-lg outline-none"
          >
            <option value="">Sort</option>
            <option value="input">Input Cost</option>
            <option value="output">Output Cost</option>
          </select>

        </div>

      </div>

      <!-- SCROLL AREA -->
      <div class="flex-1 overflow-y-auto">
        <div class="max-w-7xl mx-auto px-8 pb-10">

          <div class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">

            <div
              v-for="model in filteredModels"
              :key="model.id"
              @click="open(model)"
              class="bg-zinc-900 border border-zinc-800 rounded-xl overflow-hidden cursor-pointer hover:border-zinc-600 hover:scale-[1.02] transition"
            >

              <div class="h-48 bg-zinc-800 flex items-center justify-center">
                <img v-if="model.logo" :src="model.logo" class="object-cover w-full h-full" />
                <div v-else class="text-4xl font-semibold text-zinc-400">AI</div>
              </div>

              <div class="p-5 space-y-3">
                <div class="text-sm text-zinc-400 text-left">
                  {{ model.name.split('/')[0] }} /
                  <span class="text-white">{{ model.name.split('/')[1] }}</span>
                </div>

                <p class="text-zinc-300 text-sm line-clamp-2 text-left">
                  {{ model.description }}
                </p>

                <div class="flex justify-between text-xs text-zinc-400 pt-3">
                  <span>Input: ${{ model.input }}</span>
                  <span>Output: ${{ model.output }}</span>
                </div>
              </div>

            </div>

          </div>

        </div>
      </div>

    </div>

    <!-- MODAL -->
    <div v-if="selected" class="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
      <div class="bg-zinc-900 max-w-xl w-full rounded-xl p-8 border border-zinc-700">

        <h2 class="text-xl font-semibold mb-3">{{ selected.name }}</h2>

        <p class="text-zinc-300 mb-6">{{ selected.description }}</p>

        <div class="space-y-2 text-sm">
          <div><b>Input Cost:</b> ${{ selected.input }}</div>
          <div><b>Output Cost:</b> ${{ selected.output }}</div>
          <div>
            <b>Link:</b>
            <a :href="selected.link" target="_blank" class="text-blue-400 hover:underline">
              Open Model
            </a>
          </div>
        </div>

        <button
          @click="selected = null"
          class="mt-6 bg-zinc-800 px-4 py-2 rounded-lg hover:bg-zinc-700 transition"
        >
          Close
        </button>

      </div>
    </div>

  </div>
</template>