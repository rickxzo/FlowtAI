<script setup>
import Aurora from './ColorBends.vue'
</script>

<template>
  <div class="relative text-white bg-black">

    <!-- Fixed Aurora -->
    <div class="fixed inset-0 z-5">
      <Aurora
        :color-stops="['#191919', '#9678DC', '#191919']"
        :amplitude="1.0"
        :blend="1.0"
        :speed="1.0"
        :intensity="1.0"
        class="w-full h-full"
      />
    </div>

    <!-- HERO -->
    <section class="min-h-screen px-6 md:px-16 grid md:grid-cols-2 gap-10 items-center">

      <!-- LEFT SIDE -->
      <div class="max-w-xl text-left">
        <h1 class="text-2xl md:text-4xl font-bold leading-tight" style="font-family: 'Space Grotesk';">
          Sip some coffee,<br> build an AI agent in minutes!
        </h1>

        <p class="mt-6 text-white/60 text-lg">
          Flowt.AI gives you access to an expert designed AI agent<br>
          customizable with your own data, a LLM of your choice and other options.
        </p>
      </div>

      <!-- RIGHT SIDE -->
      <div class="flex flex-col gap-10 py-10 items-end mt-10">

        <!-- TOP -->
        <div class="max-w-sm ml-auto text-right" >
          <h2 class="text-xl font-semibold" style="font-family: 'Space Grotesk';">
            Build an AI agent
          </h2>
          <p class="mt-3 text-white/60">
            Create and deploy in 4 simple steps with flexible customization
            at every stage.
          </p>
        </div>

        <!-- BOTTOM -->
        <div class="max-w-sm ml-auto text-right">
          <h2 class="text-xl font-semibold" style="font-family: 'Space Grotesk';">
            Pay as you go
          </h2>
          <p class="mt-3 text-white/60">
            No subscriptions. Minimal markup. Transparent pricing designed
            for developers and teams.
          </p>
        </div>

        <div class="max-w-sm ml-auto text-right">
          <h2 class="text-xl font-semibold" style="font-family: 'Space Grotesk';">
            Choose from popular LLMs
          </h2>
          <p class="mt-3 text-white/60">
            Your agent's personality is your choice.<br>
            Choose which LLM model you wish for to respond to your customers.
          </p>
        </div>

        <div class="max-w-sm ml-auto text-right mt-15">
          <h2 class="text-lg font-light" style="font-family: 'Space Grotesk';">
            Read our docs for more info!
          </h2>
        </div>


      </div>

    </section>

  </div>
</template>

<style scoped>
  .aurora-container {
    width: 100%;
    height: 500px;
    position: relative;
    overflow: hidden;
  }
</style>
