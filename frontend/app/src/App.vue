<template>
  
  <div id="app">
    <router-view />
  </div>
</template>

<script>
import { store } from './store/store.js';

export default {
  data() {
    return { store };
  },
};
</script>

