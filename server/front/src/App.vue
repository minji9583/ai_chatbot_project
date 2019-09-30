<template>
  <div id="app">
    <abchat :base_url="'http://localhost:8000'"></abchat>
  </div>
</template>

<script>
import abchat from '@/components/vue-abchat.vue'

export default {
  name: 'app',
  components: {
    abchat
  }
}
</script>

<style>
</style>
