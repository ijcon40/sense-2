<script setup>
import {ref, computed} from "vue";
import {availableAlignments, selectedAlignment, topKOptions} from "../../alignmentConfigs.js";

const topKKeys = computed(() => {
      return Object.keys(topKOptions)
    }
)

const formMax = selectedAlignment.topKType === 'Top % Tokens' ? 100 : null
const step = selectedAlignment.topKType === 'Top % Tokens' ? 0.01 : 1
</script>

<template>
  <div class="card p-3">
    <!-- form to configure the settings for an alignment-->
    <form>
      <!-- true/false checkbox for is_soft -->
      <div class="form-group">
        <label class="d-flex justify-content-start" for="topKSelect">Token Occurrence Filter</label>
        <div class="input-group">
          <select class="form-select" id="topKSelect" v-model="selectedAlignment.topKType">
            <option v-for="type in topKKeys" :value="type">{{ type }}</option>
          </select>
          <input type="number" class="form-control" id="kthresh" min="0" v-bind:max="formMax"
                 v-model="topKOptions[selectedAlignment.topKType].value" v-bind:step="step">
        </div>
        <small id="topKLabel"
               class="d-flex justify-content-start text-muted mb-3">{{
            selectedAlignment.topKType === 'Top % Tokens' ? 'A value over 100 will be treated as 100%' : 'A value greater than the shared vocabulary will be treated as max'
          }}</small>
        <div class="form-check">
          <input class="form-check-input" type="checkbox" value="" v-model="availableAlignments['noise-aware'].is_soft"
                 id="flexCheckDefault">
          <label class="form-check-label" for="flexCheckDefault">
            Use soft expectation maximization instead of hard expectation maximization:
            {{ availableAlignments['noise-aware'].is_soft }}
          </label>
        </div>
      </div>
    </form>
  </div>
</template>

<style scoped>

</style>
