<template>
  <div id="app">
    <abchat :title="'sjchat'" :button_title="'good'"></abchat>
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
