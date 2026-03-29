<script setup>
import Navbar from './components/Navbar.vue'
</script>

<template>
  <Navbar />
  <Transition name="fade" mode="out-in">
    <router-view :key="$route.fullPath" />
  <Transition />
</template>
