<script setup>
import { reactive, ref, computed, watch, defineEmits, defineProps } from 'vue';
import * as vNG from 'v-network-graph';
import { useStore } from 'vuex';
import dagre from 'dagre/dist/dagre.min.js';

const store = useStore();
const emit = defineEmits(['selectContainer', 'selectImage', 'focused']);
const props = defineProps({
  focussedNode: {
    // Id of the focussed node or null
    type: String,
    default: null,
  },
});
const zoomLevel = ref(1.5);
const maxZoomLevel = 3;
const minZoomLevel = 0.05;
const graph = ref(vNG);
const nodes = computed(() => store.getters.nodes);
const edges = computed(() => store.getters.edges);
const layout = reactive({
  nodes: {},
});
const nodeSize = 12; // Used for node size and spacing

watch([nodes, edges], ([newNodes, newEdges]) => {
  updateLayout({ nodes: newNodes, edges: newEdges });
});

watch(
  () => props.focussedNode,
  (newval) => {
    focus(newval);
  }
);

const getColor = (node) => {
  switch (node.type) {
    case 'CONTAINER':
      return 'red';
    case 'CONTAINER_RUNNING':
      return 'green';
    case 'IMAGE':
      return '#4a6de5';
    case 'LAYER':
      return 'gray';
  }
};

const getShape = (node) => {
  if (node.type === 'CONTAINER' || node.type === 'CONTAINER_RUNNING')
    return 'rect';
  return 'circle';
};

const configs = reactive(
  vNG.defineConfigs({
    view: {
      scalingObjects: true,
      minZoomLevel,
      maxZoomLevel,
    },
    node: {
      selectable: false,
      normal: {
        color: (n) => getColor(n),
        type: (n) => getShape(n),
        width: nodeSize * 2,
        height: nodeSize * 1,
        radius: (n) => (n.type === 'IMAGE' ? nodeSize / 2 : nodeSize / 3),
      },
      label: {
        fontFamily: 'monospace',
        background: {
          visible: true,
          color: '#ffffff99',
          padding: {
            vertical: 1,
            horizontal: 4,
          },
          borderRadius: 2,
        },
      },
    },
    edge: {
      selectable: false,
      marker: {
        target: {
          type: 'arrow',
          width: 3,
          height: 3,
        },
      },
      normal: {
        color: '#222',
        width: 2,
      },
      hover: {
        color: '#222',
      },
    },
  })
);

const updateLayout = (data) => {
  if (
    Object.keys(data.nodes).length <= 1 ||
    Object.keys(data.edges).length == 0
  ) {
    return;
  }

  const g = new dagre.graphlib.Graph();
  g.setGraph({
    nodesep: nodeSize * 4,
    edgesep: nodeSize * 12,
    ranksep: nodeSize * 4,
    ranker: 'longest-path', // Makes nicest looking graphs
  });

  g.setDefaultEdgeLabel(() => ({}));

  // Add nodes to the layout.
  Object.entries(data.nodes).forEach(([nodeId, node]) => {
    g.setNode(nodeId, { label: node.name, width: nodeSize, height: nodeSize });
  });

  // Add edges to the layout.
  Object.values(data.edges).forEach((edge) => {
    g.setEdge(edge.source, edge.target);
  });

  dagre.layout(g);

  const box = {};
  g.nodes().forEach((nodeId) => {
    // update node position
    const x = g.node(nodeId).x;
    const y = g.node(nodeId).y;
    layout.nodes[nodeId] = { x, y };

    // calculate bounding box size
    box.top = box.top ? Math.min(box.top, y) : y;
    box.bottom = box.bottom ? Math.max(box.bottom, y) : y;
    box.left = box.left ? Math.min(box.left, x) : x;
    box.right = box.right ? Math.max(box.right, x) : x;
  });

  const graphMargin = nodeSize * 2;
  const viewBox = {
    top: (box.top ?? 0) - graphMargin,
    bottom: (box.bottom ?? 0) + graphMargin,
    left: (box.left ?? 0) - graphMargin,
    right: (box.right ?? 0) + graphMargin,
  };
  graph.value?.setViewBox(viewBox);
};

const eventHandlers = {
  'node:click': ({ node }) => {
    const type = nodes.value[node].type;
    if (type === 'CONTAINER' || type === 'CONTAINER_RUNNING') {
      return emit('selectContainer', node);
    }
    if (type === 'IMAGE') {
      return emit('selectImage', node);
    }
  },
  'node:mouseover': ({ event }) => {
    console.log(event.x, event.y);
  },
};

const focus = (nodeid) => {
  if (!nodeid) return;

  let { x, y } = layout.nodes[nodeid];
  // I can't figure out how panTo works, hence setViewBox
  const width = nodeSize * 30;
  const height = nodeSize * 30;
  graph.value?.setViewBox({
    top: y - height / 2,
    bottom: y + height / 2,
    left: x - width / 2,
    right: x + width / 2,
  });
  emit('focused');
};
</script>

<template>
  <div id="graph-wrapper">
    <div id="control-panel" class="container-fluid my-1">
      <div class="row flex-nowrap align-items-center text-nowrap">
        <div
          class="col-auto btn-group btn-group-sm"
          role="group"
          aria-label="Control panel"
        >
          <button
            type="button"
            class="btn btn-primary"
            @click="graph?.panToCenter"
          >
            To center
          </button>
          <button class="btn btn-primary" @click="graph?.fitToContents">
            Fit
          </button>
        </div>
        <div class="col">
          <input
            id="range"
            v-model.number="zoomLevel"
            type="range"
            class="form-range"
            step="0.05"
            :min="minZoomLevel"
            :max="maxZoomLevel"
          />
        </div>
      </div>
    </div>
    <v-network-graph
      ref="graph"
      v-model:zoom-level="zoomLevel"
      v-model:layouts="layout"
      :event-handlers="eventHandlers"
      :nodes="nodes"
      :edges="edges"
      :configs="configs"
      class="graph"
    >
    </v-network-graph>
  </div>
</template>

<style lang="scss" scoped>
#graph {
  height: 100%;
  width: 100%;
}
#graph-wrapper {
  position: relative;
  height: 100%;
  width: 100%;
}
#control-panel {
  position: absolute;
  z-index: 100;
}
</style>
