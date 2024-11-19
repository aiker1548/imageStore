export const store = {
  state: {
    isAuthenticated: false,
    userId: null,
  },
  mutations: {
    setUserId(state, userId) {
      state.userId = userId;
    },
    setAuth(state, isAuthenticated) {
      state.isAuthenticated = isAuthenticated;
    },
  },
};