<template>
  <div class="dashboard">
    <div class="row row">

      <va-app-bar style="border-radius: 50px; height: 40px">
        <va-button-dropdown label="Create new logCard" class="mr-2 mb-2" style="margin-top: 5px">
          <ul id="example-1">
            <li v-for="item in items" :key="item.message" style="padding-top: 10px">
              <va-button @click="showLogCard(item.message) " :value="item.message">
                {{ item.message }}
              </va-button>
            </li>
          </ul>
        </va-button-dropdown>
      </va-app-bar>


      <div v-for="(item, id) in selectedMessages" class="flex md6 lg4" style="float:bottom;">
        <LogCard :message="item" :logId="id" :removeLog="removeLog"/>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

import {Ref, ref} from "vue";
import {useToast} from "vuestic-ui";
import LogCard from '../../../components/logCard/LogCard.vue'

const value = ref();
const {init} = useToast();

const items = [
  {message: 'serial_config'},
  {message: 'telemetry'},
  {message: 'serial_config_apply'},
  {message: 'connector_logs'},
]

const selectedMessages: Ref<string[]> = ref([]);

function removeLog(id: number) {
  selectedMessages.value.splice(id, 1);
}

function showLogCard(message: string) {
  selectedMessages.value.push(message);
}

function dangerToast(msg: string) {
  init({
    message: msg,
    color: "danger",
    position: "bottom-right"
  });
}

function successToast(msg: string) {
  init({
    message: msg,
    color: "success",
    position: "bottom-right"
  });
}

</script>

<style lang="scss">
.jse-json-node {
  font-size: 19px;
  margin-top: 4px;
}

.row-equal .flex {
  .va-card {
    height: 100%;
  }
}

.dashboard {
  .va-card {
    margin-bottom: 0 !important;

    &__title {
      display: flex;
      justify-content: space-between;
    }
  }
}

</style>
