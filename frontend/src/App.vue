<template>
  <div class="container-fluid">
    <div class="row">
      <Sidebar id="sidebar">
        <div class="float-end">
          <OverviewButton v-if="showOverviewButton" @click="selectNone" />
          <FocusButton v-if="showOverviewButton" @click="focus" />
          <RefreshButton @click="refresh" />
        </div>
        <ImageInfo v-if="selectedImageId" :id="selectedImageId" />
        <ContainerInfo
          v-else-if="selectedContainerId"
          :id="selectedContainerId"
        />
        <OverviewInfo
          v-else
          @select-container="(id) => selectContainer(id)"
          @select-image="(id) => selectImage(id)"
          @focus-node="(id) => (focussedNode = id)"
        />
      </Sidebar>
      <div id="graph-container" class="col">
        <GraphView
          :focussed-node="focussedNode"
          @select-container="(id) => selectContainer(id)"
          @select-image="(id) => selectImage(id)"
          @focused="focussedNode = null"
        />
      </div>
    </div>
  </div>
</template>

<script>
import {
  GET_IMAGES,
  GET_CONTAINERS,
  GET_IMAGE,
  GET_CONTAINER,
} from './store/actions';
import OverviewInfo from './components/OverviewInfo.vue';
import Sidebar from './components/SidebarContainer.vue';
import ImageInfo from './components/ImageInfo.vue';
import ContainerInfo from './components/ContainerInfo.vue';
import RefreshButton from './components/RefreshButton.vue';
import OverviewButton from './components/OverviewButton.vue';
import GraphView from './components/GraphView.vue';
import FocusButton from './components/FocusButton.vue';

export default {
  name: 'App',
  components: {
    OverviewInfo,
    Sidebar,
    ImageInfo,
    ContainerInfo,
    RefreshButton,
    OverviewButton,
    GraphView,
    FocusButton,
  },
  data() {
    return {
      selectedContainerId: null,
      selectedImageId: null,
      focussedNode: null,
    };
  },
  computed: {
    showOverviewButton() {
      return this.selectedImageId || this.selectedContainerId;
    },
    isLoading() {
      return this.$store.getters.isLoading;
    },
  },
  created() {
    this.updateStore();
  },
  methods: {
    selectContainer(id) {
      this.selectedContainerId = id;
      this.selectedImageId = null;
    },
    selectImage(id) {
      this.selectedImageId = id;
      this.selectedContainerId = null;
    },
    selectNone() {
      this.selectedImageId = null;
      this.selectedContainerId = null;
    },
    focus() {
      this.focussedNode = this.selectedContainerId || this.selectedImageId;
    },
    updateStore() {
      if (this.selectedContainerId)
        this.$store.dispatch(GET_CONTAINER, this.selectedContainerId);
      if (this.selectedImageId)
        this.$store.dispatch(GET_IMAGE, this.selectedImageId);
      this.$store.dispatch(GET_IMAGES);
      this.$store.dispatch(GET_CONTAINERS);
    },
    refresh() {
      if (!this.isLoading) {
        this.updateStore();
      }
    },
  },
};
</script>

<style lang="scss">
body {
  margin: 0;
  padding: 0;
}

#graph-container {
  order: 2;
  height: 100vh;
  width: 100%;
  padding-left: 0;
  padding-right: 1px;
  @media (max-width: 728px) {
    height: 80vh;
  }
}

#sidebar {
  height: 100vh;
  overflow-y: scroll;
  overflow-x: hidden;
  width: 354px;
  order: 1;
  @media (max-width: 728px) {
    width: 100%;
    min-height: 100vh;
    height: auto;
    overflow-y: auto;
    order: 3;
  }
}
</style>
