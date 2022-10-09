import axios from 'axios';
import { BACKEND_URL } from '@/config';

const instance = axios.create({
  baseURL: BACKEND_URL,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json, text/plain, */*',
  },
});

// Get error message from error response
instance.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error.response?.status === 0) {
      error.message += `. Request failed with status code 0. Maybe could not connect to the server, there is a CORS issue, or something else.`;
    } else if (error.response?.data?.message) {
      error.message += `. ${error.response.data.message}`;
    }
    return Promise.reject(error);
  }
);

export default {
  /**
   * Get the list of images from the backend API
   *
   * @returns {Array} Array of overview image objects
   */
  async getImages() {
    const response = await instance.get('/images');
    return response.data;
  },

  /**
   * Get image details from the backend API
   *
   * @param {string} id of the container
   * @returns {object} image object
   */
  async getImage(id) {
    const response = await instance.get(`/images/${id}`);
    return response.data;
  },

  /**
   * Get the list of containers from the backend API
   *
   * @returns {Array} Array of overview container objects
   */
  async getContainers() {
    const response = await instance.get('/containers');
    return response.data;
  },

  /**
   * Get container details from the backend API
   *
   * @param {string} id of the container
   * @returns {object} container object
   */
  async getContainer(id) {
    const response = await instance.get(`/containers/${id}`);
    return response.data;
  },
};
