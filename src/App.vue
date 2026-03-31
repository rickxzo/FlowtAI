<script setup>
import Navbar from './components/Navbar.vue'
</script>

<template>
  <Transition name="fade" mode="out-in">
    <router-view :key="$route.fullPath" />
  </Transition>
</template>
