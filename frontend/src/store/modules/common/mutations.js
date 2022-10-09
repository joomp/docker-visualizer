/**
 * Set state.data state
 *
 * @param {*} state state
 * @param {*} payload payload
 * @param {*} payload.data new state.data value
 */
export const setData = (state, payload) => {
  state.data = payload.data;
};

/**
 * Set state.isLoading to true
 *
 * @param {*} state state
 */
export const startLoading = (state) => {
  state.isLoading = true;
};

/**
 * Set state.isLoading to true
 *
 * @param {*} state state
 */
export const finishLoading = (state) => {
  state.isLoading = false;
};

/**
 * Set state.errorMessage. Set state.isError to true
 *
 * @param {*} state state
 * @param {*} payload payload
 * @param {string|null} payload.message new state.errorMessage value
 */
export const setError = (state, { message }) => {
  state.errorMsg = message;
  state.isError = true;
};

/**
 * Clear state.errorMsg and state.isError
 *
 * @param {*} state state
 */
export const clearError = (state) => {
  state.errorMsg = null;
  state.isError = false;
};
