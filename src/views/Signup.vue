<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
import { ref } from 'vue'

const username = ref('')
const email = ref('')
const password = ref('')

const error = ref(null)

// OTP state
const otpSent = ref(false)
const otp = ref('')
const otpVerified = ref(false)
const otpMessage = ref('')
const isSendingOtp = ref(false)
const isVerifyingOtp = ref(false)
const processing = ref(false)

// 🔹 Send OTP
const sendOtp = async () => {
  if (!email.value) return

  isSendingOtp.value = true
  otpMessage.value = ''

  try {
    // TODO: replace endpoint later
    const res = await fetch(`https://flowtai-1.onrender.com/send-otp?email=${encodeURIComponent(email.value)}`, {
      credentials: 'include'
    })

    if (res.status === 200) {
      otpSent.value = true
      otpMessage.value = 'OTP sent successfully'
    } else {
      otpMessage.value = await res.text()
    }
  } catch (e) {
    otpMessage.value = 'Failed to send OTP'
  }

  isSendingOtp.value = false
}

// 🔹 Verify OTP (auto on input)
const verifyOtp = async () => {
  if (otp.value.length < 6) return

  isVerifyingOtp.value = true
  otpMessage.value = ''

  try {
    // TODO: replace endpoint later
    const res = await fetch(
      `https://flowtai-1.onrender.com/confirm-otp?email=${encodeURIComponent(email.value)}&otp=${otp.value}`, {
        credentials: 'include'
      }
    )

    if (res.status === 200) {
      otpVerified.value = true
      otpMessage.value = 'OTP verified'
    } else {
      otpVerified.value = false
      otpMessage.value = await res.text()
    }
  } catch (e) {
    otpVerified.value = false
    otpMessage.value = 'Verification failed'
  }

  isVerifyingOtp.value = false
}

// 🔹 Signup
const login = async () => {
  if (!otpVerified.value) {
    error.value = "Please verify OTP first"
    return
  }

  try {
    processing.value = true
    const res = await fetch(
      `https://flowtai-1.onrender.com/signup?username=${username.value}&email=${email.value}&password=${password.value}`,
      {
        method: "GET", // (you should switch to POST later)
        credentials: "include"
      }
    )

    const text = await res.text()

    if (!res.ok) {
      error.value = text || "Signup failed"
      processing.value = false
      return
    }

    // success
    error.value = ""
    router.push("/agents")

  } catch (err) {
    error.value = "Server error. Try again."
    processing.value = false
    console.error(err)
  }
}
</script>

<template>
    <div class="min-h-[92vh] w-full flex flex-col lg:flex-row text-white mt-12">

  <!-- LEFT SECTION -->
        <div class="w-full lg:w-1/2 bg-zinc-950 flex items-center justify-center px-8 mt-24 sm:mt-0">

            <div class="w-full max-w-md">

            <!-- Logo -->
            <div class="mb-3">
                <div class="w-20 h-12 rounded-lg  flex items-center text-white font-bold text-2xl" style="font-family:'Shadows Into Light Two';">
                flowt.ai
                </div>
            </div>

            <!-- Heading -->
            <h2 class="text-2xl font-semibold mb-4 flex" style="font-family:'Space Grotesk';">
                Good to see you.
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
                    <label>Email</label>
                </div>

                <div class="flex gap-2">
                    <input
                    v-model="email"
                    type="email"
                    required
                    class="flex-1 text-black rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-300 outline-none"
                    >

                    <button
                    type="button"
                    @click="sendOtp"
                    :disabled="!email || isSendingOtp"
                    class="px-3 py-2 rounded-lg text-sm bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50"
                    >
                    {{ isSendingOtp ? 'Sending...' : 'Send OTP' }}
                    </button>
                </div>
                </div>

                <!-- OTP FIELD -->
                <div v-if="otpSent">
                <div class="flex justify-between text-sm mb-1">
                    <label>Enter OTP</label>
                </div>

                <input
                    v-model="otp"
                    @input="verifyOtp"
                    type="text"
                    placeholder="Enter OTP"
                    class="w-full text-black rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-300 outline-none"
                >

                <p class="text-sm mt-2"
                    :class="otpVerified ? 'text-green-400' : 'text-red-400'">
                    {{ otpMessage }}
                </p>
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
                <span v-else>Sign Up</span>
                </button>

            </form>
            <p class="text-sm text-gray-500 mt-6">
                Don't have an account?
                <a href="/login" class="text-white font-medium hover:underline">
                Login
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
