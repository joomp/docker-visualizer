<template>
  <h1 class="mb-1">Image</h1>
  <h5 class="id mb-3">{{ id }}</h5>

  <SpinnerLoader v-if="isLoading" />
  <p v-else-if="isError">Error: {{ errorMsg }}</p>
  <div v-else class="my-5">
    <table class="table table-sm">
      <thead>
        <tr>
          <th>General</th>
          <th colspan="2"></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Tags:</td>
          <td colspan="2">{{ image.tags.join(', ') || 'Untagged' }}</td>
        </tr>
        <tr>
          <td>Created:</td>
          <td colspan="2">{{ dateToString(image.created) }}</td>
        </tr>
        <tr>
          <td>Author:</td>
          <td colspan="2">{{ image.author || 'Not defined' }}</td>
        </tr>
        <tr>
          <td>
            <TooltipWrap tooltip="How many containers use this image.">
              Containers:
            </TooltipWrap>
          </td>
          <td colspan="2">{{ image.containers }}</td>
        </tr>
      </tbody>
    </table>

    <table class="table table-sm">
      <thead>
        <tr>
          <th colspan="3">Target Platform</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Operating system:</td>
          <td colspan="2">{{ capitalize(image.os) }}</td>
        </tr>
        <tr>
          <td>Architecture:</td>
          <td colspan="2">{{ image.architecture }}</td>
        </tr>
      </tbody>
    </table>

    <table class="table table-sm">
      <thead>
        <tr>
          <th colspan="3">Size</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            <TooltipWrap
              tooltip="The virtual size of the image. This is the sum of the shared size and the unique size."
            >
              Total size:
            </TooltipWrap>
          </td>
          <td colspan="2">{{ sizeToString(image.size) }}</td>
        </tr>
        <tr>
          <td>
            <TooltipWrap
              tooltip="The amount of space that this image shares with another one."
            >
              Shared size:
            </TooltipWrap>
          </td>
          <td colspan="2">{{ sizeToString(image.shared_size) }}</td>
        </tr>
        <tr>
          <td>
            <TooltipWrap
              tooltip="The amount of space that is only used by this image."
            >
              Unique size:
            </TooltipWrap>
          </td>
          <td colspan="2">
            {{ sizeToString(image.size - image.shared_size) }}
          </td>
        </tr>
      </tbody>
    </table>

    <table class="table table-sm">
      <thead>
        <tr>
          <th>
            <TooltipWrap
              tooltip="Empty history items do not create an actual layer, and are not visible in the graph. Empty layers do not modify the filesystem, and only modify the metadata in the image config file."
            >
              History ({{ image.history.length }})
            </TooltipWrap>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(history, index) in image.history" :key="index">
          <td>
            <table class="table table-sm table-borderless">
              <thead class="table-light">
                <tr>
                  <th>Layer</th>
                  <th colspan="2"></th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Created:</td>
                  <td colspan="2">
                    {{ dateToString(history.created) || 'No date' }}
                  </td>
                </tr>
                <tr>
                  <td>Size:</td>
                  <td colspan="2">
                    {{ sizeToString(history.size) }}
                  </td>
                </tr>
                <tr>
                  <td>
                    <TooltipWrap
                      tooltip="The command which created this layer."
                    >
                      Created by:
                    </TooltipWrap>
                  </td>
                  <td colspan="2">
                    {{ history.created_by }}
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import store from '@/store';
import SpinnerLoader from './SpinnerLoader.vue';
import { GET_IMAGE } from '@/store/actions';
import { capitalize, dateToString } from '../utils';
import prettyBytes from 'pretty-bytes';
import TooltipWrap from './TooltipWrap.vue';

export default {
  components: { SpinnerLoader, TooltipWrap },
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  computed: {
    isLoading: () => store.state.image.isLoading,
    isError: () => store.state.image.isError,
    errorMsg: () => store.state.image.errorMsg,
    image: () => store.state.image.data,
  },
  watch: {
    id: {
      handler(newId) {
        this.$store.dispatch(GET_IMAGE, newId);
      },
      immediate: true,
    },
  },
  methods: {
    capitalize,
    dateToString,
    sizeToString(bytes) {
      // Uses SI byte prefix
      return prettyBytes(bytes, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@import 'bootstrap';
.id {
  @extend .font-monospace, .text-muted;
  overflow-wrap: anywhere;
}

th {
  @extend .mx-2;
}

td {
  @extend .text-center, .align-middle;
}

table {
  table-layout: fixed;
  width: 100%;
  overflow-wrap: break-word;
  word-break: break-word;
}
</style>
