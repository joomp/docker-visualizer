<template>
  <span
    v-tooltip
    class="tool-tipped m-0 p-0"
    data-bs-placement="right"
    :title="tooltip"
  >
    <slot></slot>
  </span>
</template>

<script>
export default {
  props: {
    tooltip: {
      type: String,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
@import 'bootstrap';
.tool-tipped {
  text-decoration-style: dotted;
  text-decoration-line: underline;
}
.tool-tipped:hover {
  @extend .text-primary;
}
</style>
