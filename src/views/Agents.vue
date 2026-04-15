<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router';

const router = useRouter();

// STATE
const agents = ref([])
const models = ref([])
const search = ref("")

const showDelete = ref(false)
const deleteAgentId = ref(null)

const showUpload = ref(false)
const uploadAgentId = ref(null)
const uploadFile = ref(null)

const showCreate = ref(false)
const showEdit = ref(false)

const editingAgent = ref(null)

const newName = ref("")
const newModel = ref("")
const prompt = ref("")

const editModel = ref("")
const editPrompt = ref("")

const isSubmitting = ref(false)
const error = ref(null)

// ✅ NEW STATES
const isLoadingAgents = ref(true)
const isUnauthorized = ref(false)

const editBackupModel = ref("")
const editMemory = ref("temporary")

const newBackupModel = ref("")
const newMemory = ref("temporary")

// COMPUTED
const filteredAgents = computed(() => {
  return agents.value.filter(a =>
    a.name.toLowerCase().includes(search.value.toLowerCase())
  )
})

// METHODS

const openDelete = (id) => {
  deleteAgentId.value = id
  showDelete.value = true
}

const confirmDelete = async () => {
  isSubmitting.value = true

  await fetch("https://flowtai-1.onrender.com/delete-agent?id=" + deleteAgentId.value , {credentials: "include"})

  showDelete.value = false
  await loadAgents()

  isSubmitting.value = false
}

const openUpload = (id) => {
  uploadAgentId.value = id
  uploadFile.value = null
  showUpload.value = true
}

const handleFile = (e) => {
  uploadFile.value = e.target.files[0]
}

const uploadKB = async () => {
  isSubmitting.value = true

  try {
    if (!uploadFile.value) {
      alert("Please select a file")
      return
    }

    const formData = new FormData()
    formData.append("file", uploadFile.value)

    const res = await fetch("https://flowtai-1.onrender.com/agent-kb?agent_id=" + uploadAgentId.value, {
      method: "POST",
      body: formData,
      credentials: "include"
    })

    if (res.status === 200) {
      alert("Knowledge uploaded successfully")
      showUpload.value = false
    } else {
      alert(await res.text())
    }

  } catch (e) {
    console.log(e)
    alert("Upload failed")
  }

  isSubmitting.value = false
}

const copyId = async (id) => {
  try {
    await navigator.clipboard.writeText(id, {credentials: "include"})
    alert("Agent ID copied!")
  } catch (e) {
    console.log("Copy failed", e)
  }
}

const editAgent = (agent) => {
  isSubmitting.value = true

  editingAgent.value = agent
  editModel.value = agent.model_id || ""
  editPrompt.value = agent.prompt || ""
  editBackupModel.value = agent.backup_model_id || ""
  editMemory.value = agent.memory || "temporary"

  showEdit.value = true
  isSubmitting.value = false
}

const createAgent = async () => {
  isSubmitting.value = true
  error.value = null

  try {
    const res = await fetch(
      "https://flowtai-1.onrender.com/create-agent?" +
      "name=" + encodeURIComponent(newName.value) +
      "&model=" + encodeURIComponent(newModel.value) +
      "&backup_model=" + encodeURIComponent(newBackupModel.value) +
      "&memory=" + encodeURIComponent(newMemory.value) +
      "&prompt=" + encodeURIComponent(prompt.value),
      {
        credentials: "include"
      }
    )

    if (res.status === 200) {
      router.push("/agents")
    } else {
      error.value = await res.text()
    }

  } catch (e) {
    error.value = "Network error"
  }

  isSubmitting.value = false
}


const saveEdit = async () => {
  error.value = null
  isSubmitting.value = true

  try {
    const res = await fetch(
      "https://flowtai-1.onrender.com/edit-agent?" +
      "id=" + editingAgent.value.id +
      "&model=" + encodeURIComponent(editModel.value) +
      "&backup_model=" + encodeURIComponent(editBackupModel.value) +
      "&memory=" + encodeURIComponent(editMemory.value) +
      "&prompt=" + encodeURIComponent(editPrompt.value),
      { credentials: "include" }
    )

    if (res.status === 200) {
      showEdit.value = false
      await loadAgents()
    } else {
      error.value = await res.text()
    }

  } catch (e) {
    error.value = "Network error"
  }

  isSubmitting.value = false
}

// ✅ UPDATED FETCH FUNCTION

const loadAgents = async () => {
  isLoadingAgents.value = true
  isUnauthorized.value = false

  try {
    const res = await fetch("https://flowtai-1.onrender.com/agents", {
      credentials: "include"
    })

    if (res.status === 401) {
      isUnauthorized.value = true
      agents.value = []
      return
    }

    const data = await res.json()
    agents.value = data.agents

  } catch (e) {
    console.log(e)
    agents.value = []
  } finally {
    isLoadingAgents.value = false
  }
}

const loadModels = async () => {
  const res = await fetch("https://flowtai-1.onrender.com/show-models", {
    credentials: "include"
  })
  const data = await res.json()
  models.value = data.models
}

// MOUNT
onMounted(() => {
  loadAgents()
  loadModels()
})
</script>

<template>
  


<div class="min-h-screen bg-zinc-950 text-white mt-16">
  <div class="max-w-7xl mx-auto px-8 py-10">

    <!-- HEADER -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">

        <h1 class="text-2xl font-semibold">Your agents</h1>
        <div class="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
      
          <input
            v-model="search"
            placeholder="search agents..."
            class="bg-zinc-900 px-4 py-2 rounded-lg w-full sm:w-64"
          />
    
          <button
            @click="showCreate = true"
            class="text-black bg-white px-4 py-2 rounded-lg hover:bg-sky-200 whitespace-nowrap"
          >
            New Agent
          </button>
      
        </div>
      </div>

    <!-- EMPTY -->
    <div v-if="isLoadingAgents" class="text-zinc-400 text-left py-6">
      Loading agents...
    </div>

    <!-- UNAUTHORIZED -->
    <div v-else-if="isUnauthorized" class="text-zinc-400 text-left py-6">
      Log In / Sign up to create/view agents
    </div>

    <!-- EMPTY -->
    <div v-else-if="filteredAgents.length === 0" class="text-zinc-400 text-left py-6">
      Your first AI agent awaits you!
    </div>

    <!-- GRID -->
    <div v-else class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">

      <div v-for="agent in filteredAgents" :key="agent.id"
        class="bg-zinc-950 rounded-xl p-6 space-y-4 border border-zinc-800">

        <div>
          <div class="flex items-center gap-2">
            <h2 class="text-lg font-semibold">{{ agent.name }}</h2>
            <span :class="agent.active ? 'text-green-500' : 'text-red-500'" class="text-xs">
              {{ agent.active ? '[Active]' : '[Inactive]' }}
            </span>
          </div>

          <p class="text-sm text-zinc-400 text-left">{{ agent.model }}</p>
          <p class="text-sm text-zinc-400 text-left">Spent: ${{ agent.spend }}</p>
        </div>

        <div class="flex justify-between pt-2">
          <button @click="copyId(agent.id)" class="text-white text-sm">Copy ID</button>
          <button @click="editAgent(agent)" class="text-white text-sm">Edit</button>
          <button @click="openDelete(agent.id)" class="text-red-400 text-sm">Delete</button>
          <button @click="openUpload(agent.id)" class="text-white text-sm">Upload</button>
        </div>

      </div>

    </div>

  </div>

  <!-- UPLOAD MODAL -->
  <div v-if="showUpload"
    class="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
    <div class="bg-zinc-900 rounded-xl p-8 w-full max-w-md space-y-6">

      <h2 class="text-xl font-semibold">Upload Knowledge Base</h2>

      <p class="text-zinc-400 text-sm">
        Uploading new data will delete existing knowledge.
      </p>

      <input type="file" accept=".txt"
        @change="handleFile"
        class="w-full bg-zinc-800 px-4 py-2 rounded-lg" />

      <div class="flex justify-end gap-4">
        <button @click="showUpload=false"
          class="px-4 py-2 bg-zinc-700 rounded-lg">
          Cancel
        </button>

        <button @click="uploadKB"
          :disabled="isSubmitting"
          class="px-4 py-2 bg-blue-600 rounded-lg text-black">
          {{ isSubmitting ? "Processing..." : "Upload" }}
        </button>
      </div>
    </div>
  </div>

  <!-- DELETE MODAL -->
  <div v-if="showDelete"
    class="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
    <div class="bg-zinc-900 rounded-xl p-8 w-full max-w-md space-y-6">

      <h2 class="text-xl text-red-400 font-semibold">Delete Agent</h2>

      <p class="text-zinc-400 text-sm">
        This action cannot be undone.
      </p>

      <div class="flex justify-end gap-4">
        <button @click="showDelete=false"
          class="px-4 py-2 bg-zinc-700 rounded-lg">
          Cancel
        </button>

        <button @click="confirmDelete"
          :disabled="isSubmitting"
          class="px-4 py-2 bg-red-600 rounded-lg">
          {{ isSubmitting ? "Deleting..." : "Delete" }}
        </button>
      </div>
    </div>
  </div>

  <!-- CREATE MODAL -->
  <div v-if="showCreate"
    class="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
    <div class="bg-zinc-900 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6 sm:p-8 space-y-6 border border-zinc-800">

      <h2 class="text-xl font-semibold">Agent info</h2>

      <div v-if="error" class="text-red-400 text-sm">
        {{ error }}
      </div>

      <input v-model="newName"
        placeholder="Agent name"
        class="w-full bg-zinc-800 px-4 py-2 rounded-lg" />

      <textarea v-model="prompt"
        placeholder="Provide context"
        class="w-full bg-zinc-800 px-4 py-2 rounded-lg h-28"></textarea>

      
      <select v-model="newModel"
        class="w-full bg-zinc-800 px-4 py-2 rounded-lg">
        <option disabled value="">Select primary model</option>

        <option v-for="model in models"
          :key="model.id"
          :value="model.id">
          {{ model.name }}
        </option>
      </select>

      <!-- BACKUP MODEL -->
        <div>
          <label class="text-sm text-zinc-400">Backup Model is used upon unavailability of primary model.</label>
          <select v-model="newBackupModel"
            class="w-full mt-1 bg-zinc-800 px-4 py-2 rounded-lg">
            <option disabled value="">Select backup model</option>
            <option v-for="model in models"
              :key="model.id"
              :value="model.id">
              {{ model.name }}
            </option>
          </select>
        </div>
        
        <!-- MEMORY -->
        <div>
          <label class="text-sm text-zinc-400">Memory</label>
        
          <div class="flex justify-center gap-6 mt-2">
            <label class="flex items-center gap-2">
              <input type="radio" value="persistent" v-model="newMemory" />
              <span>Persistent</span>
            </label>
        
            <label class="flex items-center gap-2">
              <input type="radio" value="temporary" v-model="newMemory" />
              <span>Temporary</span>
            </label>
          </div>
          <p class="text-sm text-zinc-400 mt-2 leading-relaxed">
            Persistent memory stores all conversations made by your agent.<br>
            Temporary memory functions no different while interaction, but chats are not stored long term and cannot be viewed.
          </p>
        </div>

      <div class="flex justify-end gap-4">
        <button @click="showCreate=false"
          class="px-4 py-2 bg-zinc-700 rounded-lg">
          Cancel
        </button>

        <button @click="createAgent"
          :disabled="isSubmitting || !prompt.trim() || !newName.trim() || !newModel"
          class="px-4 py-2 bg-blue-600 rounded-lg">
          {{ isSubmitting ? "Processing..." : "Confirm" }}
        </button>
      </div>
    </div>
  </div>

  <!-- EDIT MODAL -->
  <!-- EDIT MODAL -->
<div v-if="showEdit"
  class="fixed inset-0 bg-black/70 flex items-center justify-center z-50">

  <div class="bg-zinc-900 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6 sm:p-8 space-y-6 border border-zinc-800">

    <!-- HEADER -->
    <div class="flex justify-between items-center">
      <h2 class="text-xl font-semibold">Edit Agent</h2>
      <button @click="showEdit=false" class="text-zinc-400 hover:text-white">✕</button>
    </div>

    <!-- ERROR -->
    <div v-if="error" class="text-red-400 text-sm">
      {{ error }}
    </div>

    <!-- GRID -->
    <div class="grid md:grid-cols-2 gap-6">

      <!-- PRIMARY MODEL -->
      <div>
        <label class="text-sm text-zinc-400">Primary Model</label>
        <select v-model="editModel"
          class="w-full mt-1 bg-zinc-800 px-4 py-2 rounded-lg">
          <option v-for="model in models"
            :key="model.id"
            :value="model.id">
            {{ model.name }}
          </option>
        </select>
      </div>

      <!-- BACKUP MODEL -->
      <div>
        <label class="text-sm text-zinc-400">Backup Model</label>
        <select v-model="editBackupModel"
          class="w-full mt-1 bg-zinc-800 px-4 py-2 rounded-lg">
          <option disabled value="">Select backup model</option>
          <option v-for="model in models"
            :key="model.id"
            :value="model.id">
            {{ model.name }}
          </option>
        </select>
        <p class="text-xs text-zinc-500 mt-1">
          Used when main model is unavailable.
        </p>
      </div>

    </div>

    <!-- MEMORY -->
    <div>
      <label class="text-sm text-zinc-400">Memory</label>

      <div class="flex gap-6 mt-2">
        <label class="flex items-center gap-2 cursor-pointer">
          <input type="radio" value="persistent" v-model="editMemory" />
          <span>Persistent</span>
        </label>

        <label class="flex items-center gap-2 cursor-pointer">
          <input type="radio" value="temporary" v-model="editMemory" />
          <span>Temporary</span>
        </label>
      </div>

      <p class="text-xs text-zinc-500 mt-1">
        Persistent stores conversations. Temporary does not store messages.
      </p>
    </div>

    <!-- PROMPT -->
    <div>
      <label class="text-sm text-zinc-400">System Prompt</label>
      <textarea v-model="editPrompt"
        class="w-full mt-1 bg-zinc-800 px-4 py-2 rounded-lg h-32"></textarea>
    </div>

    <!-- API ENDPOINT -->
    <div>
      <label class="text-sm text-zinc-400">API Endpoint</label>

      <div class="flex mt-1">
        <input
          :value="`https://flowtai-1.onrender.com/respond?agent_id=${editingAgent.id}&input=`"
          readonly
          class="flex-1 bg-zinc-800 px-4 py-2 rounded-l-lg text-sm"
        />
        <button
          @click="copyId(`https://flowtai-1.onrender.com/respond?agent_id=${editingAgent.id}&input=`)"
          class="bg-blue-600 px-4 rounded-r-lg">
          Copy
        </button>
      </div>
    </div>

    <!-- EMBED CODE -->
    <div>
      <label class="text-sm text-zinc-400">HTML Embed Code</label>

      <div class="flex mt-1">
        <input
          :value="`<script src='https://flowtai-1.onrender.com/static/widget.js' data-agent-id=${editingAgent.id}></script>`"
          readonly
          class="flex-1 bg-zinc-800 px-4 py-2 rounded-l-lg text-sm"
        />
        <button
          @click="copyId(`<script src='https://flowtai-1.onrender.com/static/widget.js' data-agent-id=${editingAgent.id}></script>`)"
          class="bg-green-600 px-4 rounded-r-lg">
          Copy
        </button>
      </div>
    </div>

    <!-- ACTIONS -->
    <div class="flex justify-end gap-4 pt-2">
      <button @click="showEdit=false"
        class="px-4 py-2 bg-zinc-700 rounded-lg">
        Cancel
      </button>

      <button @click="saveEdit"
        :disabled="isSubmitting || !editPrompt.trim()"
        class="px-4 py-2 bg-blue-600 rounded-lg">
        {{ isSubmitting ? "Saving..." : "Save Changes" }}
      </button>
    </div>

  </div>
</div>

</div>
</template>
