<template>
  <h1 class="mb-3">Overview</h1>

  <a
    data-bs-toggle="collapse"
    href="#containers"
    aria-expanded="true"
    aria-controls="containers"
    class="collapse-toggle"
  >
    <h4 class="my-3">
      Containers ({{ containers.length }})
      <i class="bi bi-chevron-down float-end"></i>
    </h4>
  </a>
  <div id="containers" class="collapse show">
    <SpinnerLoader v-if="isContainersLoading" />
    <p v-else-if="isContainersError">Error: {{ containersErrorMsg }}</p>
    <div v-else>
      <div v-for="(container, index) in containers" :key="index">
        <div class="card p-1 m-1">
          <div class="card-body">
            <h5 class="card-title">{{ container.name }}</h5>
            <h6 class="card-subtitle mb-2 id">{{ container.id }}</h6>
            <div class="card-text">Status: {{ container.status }}</div>
            <div class="card-text">
              Image: {{ container.image_tags[0] || 'Untagged' }}
            </div>
            <a
              class="card-link"
              href="#"
              @click.stop.prevent="() => selectContainer(container.id)"
              >Inspect</a
            >
            <a
              href="#"
              class="card-link"
              @click.stop.prevent="() => focusNode(container.id)"
              >Focus</a
            >
          </div>
        </div>
      </div>
    </div>
  </div>

  <a
    data-bs-toggle="collapse"
    href="#images"
    aria-expanded="true"
    aria-controls="images"
    class="collapse-toggle"
  >
    <h4 class="my-3">
      Images({{ images.length }})
      <i class="bi bi-chevron-down float-end"></i>
    </h4>
  </a>
  <div id="images" class="collapse show">
    <SpinnerLoader v-if="isImagesLoading" />
    <p v-else-if="isImagesError">Error: {{ imagesErrorMsg }}</p>
    <div v-else>
      <div v-for="(image, index) in images" :key="index">
        <div class="card m-1">
          <div class="card-body">
            <h5 class="card-title">{{ image.tags[0] || 'Untagged' }}</h5>
            <h6 class="card-subtitle mb-2 id">{{ image.id }}</h6>
            <a
              href="#"
              class="card-link"
              @click.stop.prevent="() => selectImage(image.id)"
              >Inspect</a
            >
            <a
              href="#"
              class="card-link"
              @click.stop.prevent="() => focusNode(image.id)"
              >Focus</a
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import store from '@/store';
import SpinnerLoader from './SpinnerLoader.vue';
export default {
  components: {
    SpinnerLoader,
  },
  emits: ['selectContainer', 'selectImage', 'focusNode'],
  computed: {
    isContainersLoading: () => store.state.containers.isLoading,
    containers: () => store.state.containers.data,
    isContainersError: () => store.state.containers.isError,
    containersErrorMsg: () => store.state.containers.errorMsg,

    isImagesLoading: () => store.state.images.isLoading,
    images: () => store.state.images.data,
    isImagesError: () => store.state.images.isError,
    imagesErrorMsg: () => store.state.images.errorMsg,
  },
  methods: {
    selectContainer(id) {
      this.$emit('selectContainer', id);
    },
    selectImage(id) {
      this.$emit('selectImage', id);
    },
    focusNode(id) {
      this.$emit('focusNode', id);
    },
  },
};
</script>

<style lang="scss" scoped>
@import 'bootstrap';
.id {
  @extend .font-monospace, .text-muted;
  overflow-wrap: normal;
  text-overflow: ellipsis;
  overflow: hidden;
}

.collapse-toggle h4 .bi {
  transition: 0.24s transform ease-in-out;
}
.collapse-toggle.collapsed h4 .bi {
  transform: rotate(90deg);
}
.collapse-toggle {
  all: unset;
  cursor: pointer;
}
</style>
