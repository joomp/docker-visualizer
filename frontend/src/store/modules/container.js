import api from '../../services/backend';
import {
  finishLoading,
  startLoading,
  clearError,
  setData,
  setError,
} from './common/mutations';

/**
 * @property {Array} data container object
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
   * Update state.data by fetching container data from the backend
   *
   * @param {*} context context
   * @param {string} id target container id
   */
  get: async ({ commit }, id) => {
    commit('startLoading');
    commit('clearError');
    commit('setData', { data: null });

    try {
      const container = await api.getContainer(id);
      commit('setData', { data: container });
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
