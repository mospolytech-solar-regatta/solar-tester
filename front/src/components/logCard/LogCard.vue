<template>

  <va-card>
    <va-card-title><h2 style="color: #2c3e50;">{{ message }}</h2></va-card-title>
    <va-card-content>
      <va-scroll-container vertical style="max-height: 300px;">
        <va-list>
          <va-list-item v-for="l in logs" :key="l">
            {{ l }}
          </va-list-item>
        </va-list>
      </va-scroll-container>
    </va-card-content>
    <va-card-actions align="center">
      <va-button-group class="mb-4" size="medium">
        <va-button @click="startLog">Start</va-button>
        <va-button @click="removeLog(logId)">Remove</va-button>
        <va-button @click="stopLog">Stop</va-button>
      </va-button-group>
    </va-card-actions>
  </va-card>
</template>

<script setup lang="ts">
import {ref} from "@vue/reactivity";

const isLoading = ref(true);
const logs = ref(Array<string>());
const ws = ref();
const props = defineProps(["message", 'removeLog', 'logId']);

// onMounted(() => {
//   for (let i = 0; i < 50; i++) {
//     logs.value.push(i.toString());
//   }
// });

function startLog() {
  let host = import.meta.env.VITE_BACKEND_HOST
  if (host == "") {
    host = location.host
  }
  var endpoint = "ws://" + host + "/listen/" + props.message;
  ws.value = new WebSocket(endpoint);
  ws.value.onmessage = onMessage;
}

function onMessage(event: any) {
  let content = document.createTextNode(event.data)
  console.log(event.data);
  if (event.data instanceof Blob) {
    let reader = new FileReader();

    reader.onload = () => {
      console.log("Result: " + reader.result);
      let res: string = <string>reader.result;
      logs.value.push(res);
    };

    reader.readAsText(event.data);
  } else {
    logs.value.push(event.data);
  }
}

function stopLog() {
  ws.value.close();
}

</script>

<style scoped>

</style>
