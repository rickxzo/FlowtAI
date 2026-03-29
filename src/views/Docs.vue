<script setup>
import Navbar from '../components/Navbar.vue'
</script>


<template>
  <Navbar />
  <div class="min-h-screen bg-zinc-950 text-white text-left mt-12" style="font-family:'Space Grotesk';">
    <div class="max-w-5xl mx-auto px-8 py-12 space-y-12">

      <!-- HEADER -->
      <div>
        <h1 class="text-4xl font-semibold mb-2" style="font-family:'Space Grotesk';">Documentation</h1>
        <p class="text-zinc-400">
          Learn how to create, manage, and use AI agents on Flowt.ai
        </p>
      </div>

      <!-- CREATE AGENT -->
      <div class="border border-zinc-800 rounded-xl p-8 space-y-6">
        <h2 class="text-2xl font-semibold" style="font-family:'Space Grotesk';">Create New Agent</h2>

        <div>
          <h3 class="text-lg font-medium text-zinc-200">Agent Name</h3>
          <p class="text-zinc-400 mt-1">
            The agent name is just a placeholder and is not revealed to the agent.<br>
            Feel free to name according to convenience.
          </p>
        </div>

        <div>
          <h3 class="text-lg font-medium text-zinc-200">Context</h3>
          <p class="text-zinc-400 mt-1">
            Context is always available to your agent while conversing with clients, unlike uploaded data.<br>
            An appropriate context enhances performance significantly.
          </p>
        </div>

        <div>
          <h3 class="text-lg font-medium text-zinc-200">Model Dropdown</h3>
          <p class="text-zinc-400 mt-1">
            The 'mind' of the agent. Choose appropriately based on performance and budget.
          </p>
        </div>
      </div>

      <!-- UPLOAD DATA -->
      <div class="border border-zinc-800 rounded-xl p-8 space-y-4">
        <h2 class="text-2xl font-semibold" style="font-family:'Space Grotesk';">Upload Data</h2>
        <p class="text-zinc-400">
          Data is to be uploaded as plain text via a txt file.<br>
          Uploaded data will erase all previous data permanently.
        </p>
      </div>

      <!-- USE AGENT -->
      <div class="border border-zinc-800 rounded-xl p-8 space-y-4">
        <h2 class="text-2xl font-semibold" style="font-family:'Space Grotesk';">Use Agent</h2>
        <p class="text-zinc-400">
          Copy agent ID and send requests via:<br><br>
          <i class="text-indigo-400">https://{domain-name}/respond?agent_id={agent-id}&input={your-input}</i>
        </p>
      </div>

      <!-- EDIT AGENT -->
      <div class="border border-zinc-800 rounded-xl p-8 space-y-6">
        <h2 class="text-2xl font-semibold" style="font-family:'Space Grotesk';">Edit Agent</h2>

        <div>
          <h3 class="text-lg font-medium text-zinc-200">Context</h3>
          <p class="text-zinc-400 mt-1">
            Modify agent instructions here.
          </p>
        </div>

        <div>
          <h3 class="text-lg font-medium text-zinc-200">Model</h3>
          <p class="text-zinc-400 mt-1">
            Change the model used by the agent.
          </p>
        </div>
      </div>

      <!-- DELETE AGENT -->
      <div class="border border-zinc-800 rounded-xl p-8 space-y-4">
        <h2 class="text-2xl font-semibold" style="font-family:'Space Grotesk';">Delete Agent</h2>
        <p class="text-red-400">
          Agent once deleted cannot be recovered.
        </p>
      </div>

    </div>
  </div>
</template>