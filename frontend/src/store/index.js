import { createStore } from 'vuex';
import images from './modules/images';
import image from './modules/image';
import containers from './modules/containers';
import container from './modules/container';
import { shortId, shortName } from '@/utils';

const getters = {
  /**
   * Checks if something is loading.
   *
   * @param {*} state Store state
   * @returns {boolean} True if something is loading, else false
   */
  isLoading: (state) => {
    return (
      state.images.isLoading ||
      state.containers.isLoading ||
      state.container.isLoading ||
      state.image.isLoading
    );
  },

  /**
   * Returns all the nodes used in the graph. Returns empty array if containers or images are loading.
   *
   * @param {*} state Store state
   * @typedef {object} Node
   * @property {string} name - Node label
   * @property {('CONTAINER'|'LAYER'|'IMAGE'|'CONTAINER_RUNNING')} type - The type of the node
   * @returns {{string, Node}} object of nodes, where the key is node id.
   */
  nodes: (state) => {
    if (state.containers.isLoading || state.images.isLoading) {
      return [];
    }
    const containers = state.containers.data;
    const images = state.images.data;
    const nodes = {};

    containers.forEach((cont) => {
      nodes[cont.id] = {
        name: `${shortName(cont.name)}\n${shortId(cont.id)}`,
        type: cont.status === 'running' ? 'CONTAINER_RUNNING' : 'CONTAINER',
      };
    });

    images.forEach((img) => {
      nodes[img.id] = {
        name: `
          ${img.tags[0] ? shortName(img.tags[0]) + '\n' : ''}
          ${shortId(img.id)}
        `,
        type: 'IMAGE',
      };
      img.layers.forEach((layer) => {
        nodes[layer] = {
          name: shortId(layer),
          type: 'LAYER',
        };
      });
    });
    return nodes;
  },

  /**
   * Returns all the edges in the graph. Returns empty array if containers or images are loading.
   *
   * @param {*} state Store state
   * @typedef {object} Edge
   * @property {string} source - Source of the edge. Must be a node id.
   * @property {string} target - Target of the edge. Must be a node id.
   * @returns {{string, Edge}} object of edge, where the key is edge id.
   */
  edges: (state) => {
    if (state.containers.isLoading || state.images.isLoading) {
      return [];
    }
    const containers = state.containers.data;
    const images = state.images.data;
    const edges = {};

    containers.forEach((cont) => {
      edges[cont.id + cont.image_id] = {
        source: cont.id,
        target: cont.image_id,
      };
    });

    images.forEach((img) => {
      let prevId = img.id;
      img.layers.reduceRight((_, layer) => {
        edges[prevId + layer] = {
          source: prevId,
          target: layer,
        };
        prevId = layer;
      }, null);
    });
    return edges;
  },
};

/*
 * images contains the data fetched from the API at \images
 * containers contains the data fetched from the API at \containers
 * image contains the data fetched from the API at \images\<id>
 * container contains the data fetched from the API at \containers\<id>
 */
export default createStore({
  getters,
  modules: {
    images,
    image,
    containers,
    container,
  },
});
