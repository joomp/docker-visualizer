import api from '../../services/backend';
import {
  finishLoading,
  startLoading,
  clearError,
  setData,
  setError,
} from './common/mutations';

/**
 * @property {Array} data image object
 * @property {boolean} isLoading whether the data is loading
 * @property {boolean} isError whether an error occurred during the last update
 * @property {string|null} errorMsg Error message, if error occurred else null
 */
const state = {
  data: null,
  isLoading: false,
  errorMsg: null,
  isError: false,
};

const actions = {
  /**
   * Update state.data by fetching image data from the backend
   *
   * @param {*} context context
   * @param {string} id target image id
   */
  get: async ({ commit }, id) => {
    commit('startLoading');
    commit('setData', { data: null });
    commit('clearError');

    try {
      const image = await api.getImage(id);
      commit('setData', { data: image });
    } catch (e) {
      commit('setError', { message: e.message });
    }

    commit('finishLoading');
  },
};

const mutations = {
  setData,
  startLoading,
  finishLoading,
  setError,
  clearError,
};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
};
