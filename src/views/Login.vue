<script setup>

import { useRouter } from 'vue-router'

const router = useRouter()

import { ref } from 'vue'

const username = ref('')
const password = ref('')
const error = ref(null)
const processing = ref(false)

const login = async () => {
  processing.value = true
  error.value = null

  try{

    const params = new URLSearchParams({
    username: username.value,
    password: password.value
    })

    const res = await fetch(`https://flowtai-1.onrender.com/login?${params.toString()}`, {
      credentials: 'include'
    })

    if(res.ok){
      router.push("/agents")
    }else{
      const txt = await res.text()
      error.value = txt || "Login failed"
    }

  }catch(e){
    error.value = "Network error"
  }
  processing.value = false

}

</script>

<template>
  
    <div class="min-h-[92vh] w-full flex flex-col lg:flex-row text-white mt-12">

  <!-- LEFT SECTION -->
        <div class="w-full lg:w-1/2 bg-zinc-950 flex items-center justify-center px-8 ">

            <div class="w-full max-w-md">

            <!-- Logo -->
            <div class="mb-3">
                <div class="w-20 h-12 rounded-lg  flex items-center text-white font-bold text-2xl" style="font-family:'Shadows Into Light Two';">
                flowt.ai
                </div>
            </div>

            <!-- Heading -->
            <h2 class="text-2xl font-semibold mb-4 flex" style="font-family:'Space Grotesk';">
                Welcome Back.
            </h2>


            <div v-if="error" class="text-red-500 text-sm mb-4">
                {{error}}
            </div>

            <!-- FORM -->
            <form @submit.prevent="login" class="space-y-5">

                <div>
                <div class="flex justify-between text-sm mb-1">
                    <label>Username</label>
                
                </div>

                <input
                    v-model="username"
                    type="text"
                    required
                    class="w-full text-black rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-300 outline-none"
                >
                </div>


                <div>
                <div class="flex justify-between text-sm mb-1">
                    <label>Password</label>
                
                </div>

                <input
                    v-model="password"
                    type="password"
                    required
                    class="w-full text-black rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-300 outline-none"
                >
                </div>

                <button
                type="submit"
                :disabled="processing"
                class="w-full py-2 rounded-lg text-white bg-gradient-to-r from-indigo-900 to-indigo-600 transition"
                :class="processing ? 'opacity-70 cursor-not-allowed' : 'hover:opacity-90'"
                >
                <span v-if="processing">Please wait...</span>
                <span v-else>Sign In</span>
                </button>

            </form>
            <p class="text-sm text-gray-500 mt-6">
                Don't have an account?
                <a href="/signup-page" class="text-white font-medium hover:underline">
                Sign up
                </a>
            </p>
            </div>

        </div>


        <!-- RIGHT SECTION -->
        <div class="hidden lg:flex w-1/2 p-6 bg-zinc-950 py-20" >
        <div class="relative w-full max-w-xl rounded-xl overflow-hidden text-white flex items-center px-20">
            <!-- Sharp Gradient Background -->
            <div class="absolute inset-0 bg-gradient-to-br from-[#191919] via-[#3b2a6d] to-[#191919]"></div>

            <!-- Glow Effect -->
             <div class="absolute w-[700px] h-[700px] bg-purple-400/20 blur-[140px] rounded-full top-[-150px] right-[-150px]"></div>
            <div class="absolute w-[500px] h-[500px] bg-indigo-500/10 blur-[120px] rounded-full bottom-[-100px] left-[-100px]"></div>

            <!-- Content -->
            <div class="relative max-w-xl">

            <h1 class="text-5xl font-normal leading-tight mb-6 text-right" style="font-family:'Space Grotesk';">
                Turn Your Data into an AI Chatbot
            </h1>

            <p class="text-violet-100 text-lg text-left" style="font-family:'Space Grotesk';">
                Select a model, upload your data, and launch a chatbot in minutes.
        Handle customer support, answer questions, or power intelligent assistants—all without complex setup.
                <br><br>
                Scale customer communication without increasing
                support teams.
            </p>

            </div>

        </div>
        </div>

        </div>
</template>
