<script setup>
import {ref, computed} from "vue";
import {availableAlignments, selectedAlignment, topKOptions} from "../../alignmentConfigs.js";
import GlobalAlignSettings from "./GlobalAlignSettings.vue";
import NoiseAwareAlignSettings from "./NoiseAwareAlignSettings.vue";
import S4AlignSettings from "./S4AlignSettings.vue";

const alignmentTypeOptions = computed(() => {
// the options are the keys of availableEmbeddings
  return Object.keys(availableAlignments);
});

const topKKeys = computed(() => {
      return Object.keys(topKOptions)
    }
)

const formMax = selectedAlignment.topKType === 'Top % Tokens'?100:null
const step = selectedAlignment.topKType === 'Top % Tokens'?0.01:1

</script>

<template>
  <div>
    <!-- form to configure the settings for an alignment-->
    <form>
      <!-- dropdown to select the alignment object to edit -->
      <label class="d-flex justify-content-start" for="topKSelect">Token Occurrence Filter</label>
      <div class="input-group">
        <select class="form-select" id="topKSelect" v-model="selectedAlignment.topKType">
          <option v-for="type in topKKeys" :value="type">{{ type }}</option>
        </select>
        <input type="number" class="form-control" id="cthresh" min="0" v-bind:max="formMax"
               v-model="topKOptions[selectedAlignment.topKType].value" v-bind:step="step">
      </div>
      <small id="topKLabel"
             class="d-flex justify-content-start text-muted mb-3">{{
          selectedAlignment.topKType === 'Top % Tokens' ? 'A value over 100 will be treated as 100%' : 'A value greater than the shared vocabulary will be treated as max'
        }}</small>


      <label class="d-flex justify-content-start" for="alignmentTypeSelect">Select Alignment Type</label>
      <select class="form-select mb-3" id="alignmentTypeSelect" v-model="selectedAlignment.alignmentType">
        <option v-for="type in alignmentTypeOptions" :value="type">{{ type }}</option>
      </select>

      <!-- form to configure the embedding, changes depending on which embedding type is selected -->
      <div v-if="selectedAlignment.alignmentType!= null">
        <div v-if="selectedAlignment.alignmentType === 'global'">
          <!-- <GlobalAlignSettings/> -->
        </div>
        <div v-if="selectedAlignment.alignmentType === 'noise-aware'">
          <NoiseAwareAlignSettings/>
        </div>
        <div v-if="selectedAlignment.alignmentType === 's4'">
          <S4AlignSettings/>
        </div>

      </div>

    </form>

  </div>
</template>

<style scoped>

</style>
