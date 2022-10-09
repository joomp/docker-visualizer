import api from '../../services/backend';
import {
  finishLoading,
  startLoading,
  clearError,
  setData,
  setError,
} from './common/mutations';

/**
 * @property {Array} data list of images
 * @property {boolean} isLoading whether the data is loading
 * @property {boolean} isError whether an error occurred during the last update
 * @property {string|null} errorMsg Error message, if error occurred else null
 */
const state = {
  data: [],
  isLoading: false,
  errorMsg: null,
  isError: false,
};

const actions = {
  /**
   * Update state.data by fetching images from the backend
   *
   * @param {*} context context
   */
  get: async ({ commit }) => {
    commit('startLoading');
    commit('setData', { data: [] });
    commit('clearError');

    try {
      const images = await api.getImages();
      images.sort((a, b) => !a.tags[0] || a.tags[0] > b.tags[0]);
      commit('setData', { data: images });
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
