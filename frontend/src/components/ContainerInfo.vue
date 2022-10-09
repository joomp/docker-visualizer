<template>
  <h1 class="mb-1">Container</h1>
  <h5 class="id mb-3">{{ id }}</h5>

  <SpinnerLoader v-if="isLoading" />
  <p v-else-if="isError">Error: {{ errorMsg }}</p>
  <div v-else class="my-5">
    <table class="table table-sm">
      <thead>
        <tr>
          <th colspan="3">General</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Name:</td>
          <td colspan="2">{{ container.name }}</td>
        </tr>
        <tr>
          <td>Status:</td>
          <td colspan="2">{{ container.status_description }}</td>
        </tr>
        <tr>
          <td>Image:</td>
          <td colspan="2">{{ container.image || 'Undefined' }}</td>
        </tr>
        <tr>
          <td>Command:</td>
          <td colspan="2">{{ container.command || 'Undefined' }}</td>
        </tr>
        <tr>
          <td>Created:</td>
          <td colspan="2">{{ dateToString(container.created) }}</td>
        </tr>
        <tr>
          <td>
            <TooltipWrap
              tooltip="The number of active processes in the container."
              >Processes:
            </TooltipWrap>
          </td>
          <td colspan="2">
            {{ container.processes }}
          </td>
        </tr>
      </tbody>
    </table>

    <table class="table table-sm">
      <thead>
        <tr>
          <th colspan="3">Storage</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Graph driver:</td>
          <td colspan="2">{{ container.graph_driver || 'Undefined' }}</td>
        </tr>
        <tr>
          <td>Root filesystem size:</td>
          <td colspan="2">{{ sizeToString(container.size_rootfs) }}</td>
        </tr>
        <tr>
          <td>
            <TooltipWrap
              tooltip="The size of the container specific RW-layer, or the total size of the files which have been created or changed compared to the container base image."
              >Container layer size:
            </TooltipWrap>
          </td>
          <td colspan="2">
            {{ sizeToString(container.size_rw) }}
          </td>
        </tr>
      </tbody>
    </table>

    <table class="table table-sm">
      <thead>
        <tr>
          <th colspan="3">Memory</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            <TooltipWrap
              tooltip="Virtual memory usage as reported by Docker CLI."
              >Memory usage:
            </TooltipWrap>
          </td>
          <td colspan="2">{{ memoryToString(container.memory_usage) }}</td>
        </tr>
        <tr>
          <td>
            <TooltipWrap
              tooltip="PSS memory metric. The portion of physical memory occupied by the container composed from the unshared memory and proportion of shared memory. The PSS for the container is computed by adding up the PSS of all the processes in the container."
              >Proportional set size:
            </TooltipWrap>
          </td>
          <td colspan="2">
            {{ memoryToString(container.pss) }}
          </td>
        </tr>
      </tbody>
    </table>

    <table class="table table-sm">
      <thead>
        <tr>
          <th>Mapped Ports</th>
        </tr>
        <tr v-if="!container.ports.length">
          <td>No port mappings</td>
        </tr>
      </thead>
      <tbody v-if="container.ports.length">
        <tr v-for="(port, index) in container.ports" :key="index">
          <td>
            <table class="table table-sm table-borderless">
              <thead class="table-light">
                <tr>
                  <th colspan="3">Port</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>IP:</td>
                  <td colspan="2">
                    {{ port.ip || '-' }}
                  </td>
                </tr>
                <tr>
                  <td>Container port:</td>
                  <td colspan="2">
                    {{ port.private_port || '-' }}
                  </td>
                </tr>
                <tr>
                  <td>Host port:</td>
                  <td colspan="2">
                    {{ port.public_port || '-' }}
                  </td>
                </tr>
                <tr>
                  <td>Port type:</td>
                  <td colspan="2">
                    {{ port.type || '-' }}
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>

    <table class="table table-sm">
      <thead>
        <tr>
          <th>Mounts</th>
        </tr>
        <tr v-if="!container.mounts.length">
          <td>No Mounts</td>
        </tr>
      </thead>
      <tbody v-if="container.mounts.length">
        <tr v-for="(mount, index) in container.mounts" :key="index">
          <td>
            <table class="table table-sm table-borderless">
              <thead class="table-light">
                <tr>
                  <th>Mount</th>
                  <th colspan="2"></th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Source:</td>
                  <td colspan="2">
                    {{ mount.source }}
                  </td>
                </tr>
                <tr>
                  <td>Destination:</td>
                  <td colspan="2">
                    {{ mount.destination }}
                  </td>
                </tr>
                <tr>
                  <td>Type:</td>
                  <td colspan="2">
                    {{ mount.type }}
                  </td>
                </tr>
                <tr>
                  <td>Mode:</td>
                  <td colspan="2">
                    {{ mount.mode }}
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
import { GET_CONTAINER } from '@/store/actions';
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
    isLoading: () => store.state.container.isLoading,
    isError: () => store.state.container.isError,
    errorMsg: () => store.state.container.errorMsg,
    container: () => store.state.container.data,
  },
  watch: {
    id: {
      handler(newId) {
        this.$store.dispatch(GET_CONTAINER, newId);
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
    memoryToString(bytes) {
      // Uses binary byte prefix
      return prettyBytes(bytes, {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
        binary: true,
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
