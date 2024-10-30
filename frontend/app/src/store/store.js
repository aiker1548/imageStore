import { reactive } from 'vue';

export const store = reactive({
  isAuthenticated: false,
  userId: null,
});
