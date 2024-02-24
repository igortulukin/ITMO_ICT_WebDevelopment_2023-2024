# EditingProgram.vue
**Описание**:Пример компонента, в котором производятся все CRUD операции

**Листинг кода**:
``` vue title="EditingProgram.vue"
<script setup lang="ts">
import {onMounted, ref, Ref} from "vue";
import TimePicker from "../TimePicker.vue";
import More from "../../assets/more.svg"
import Actions from "../Actions.vue";
import router from "../../router";
import LeftArrow from "../../assets/left-arrow.svg";
import Edit from "../../assets/edit.svg";
import Grid from "../Grid.vue";
import {StainerStore} from "../../store/StainerStore.ts";
import client from "../../utils/client.ts";
import {components} from "../../types/schema";
import {Cell} from "../../types/types.ts";
import TestKeyboard from "../Test/TestKeyboard.vue";

type Step = components["schemas"]["ProgramStep"];

const stainer = StainerStore();

const props = defineProps<{
  id: number
}>()

onMounted(async () => {
  fetchProgram()
})

async function fetchProgram() {
  let {data, error, response} = await client.GET(`/api/programs/programs/{id}/`, {
    params: {
      path: {
        id: props.id
      }
    }
  })
  if (error) {
    if (response.status == 401) {
      router.push('/login')
    }
    editProgram.value = program.value
    return
  }
  if (!data) return
  program.value = data
  editProgram.value = data
  if (data.steps.length < 1) {
    addStep()
  }
}

const showGrid = ref(false);
let selectedStep: Step;
let copiedStep: components["schemas"]["ProgramStepRequest"];

const program: Ref<components["schemas"]["ProgramDetail"] | undefined> = ref(undefined)
const editProgram: Ref<components["schemas"]["ProgramDetail"] | undefined> = ref()

async function editReagent(cell: Cell) {
  let body: components["schemas"]["PatchedProgramStepRequest"] = {
    step_type: 'reagent',
    cell_x: (cell.id - 1) % 8,
    cell_y: Math.trunc((cell.id - 1) / 8),
    reagent: null,
    seconds: selectedStep.seconds,
    stirring: selectedStep.stirring,
    precision: selectedStep.precision,
    order: selectedStep.order
  }
  switch (cell.object) {
    case 'washer':
      body.step_type = 'washing'
      break
    case 'heater':
      body.step_type = 'drying'
      break
    default:
      if (cell.data) {
        body.step_type = 'reagent'
        body.reagent = cell.data.reagent
        break
      } else return
  }
  if (typeof cell.data?.cell_x !== 'undefined' && typeof cell.data?.cell_y !== 'undefined') {
    body.cell_x = cell.data?.cell_x
    body.cell_y = cell.data?.cell_y
  }
  let {error, response} = await client.PATCH(`/api/programs/steps/{id}/`, {
    params: {
      path: {
        id: selectedStep.id
      }
    },
    body: body
  })
  if (error) {
    if (response.status == 401) {
      router.push('/login')
    }
  }
  await fetchProgram()
}

function processStep(step: Step) {
  if (step.step_type === 'drying')
    return 'Сушка'
  if (step.step_type === 'washing')
    return 'Промывка'
  return getReagent(step.reagent)
}

function processStation(step: Step) {
  const lttrs = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
  return lttrs[step.cell_x] + (step.cell_y + 1)
}

async function deleteStep(step: Step) {
  let {error, response} = await client.DELETE(`/api/programs/steps/{id}/`, {
    params: {
      path: {
        id: step.id
      }
    }
  })
  if (error) {
    if (response.status == 401) {
      router.push('/login')
    }
  }
  await fetchProgram()
}

async function addStep(step?: Step) {
  if (!stainer.currentConfiguration) return
  let newStep: components["schemas"]["ProgramStepRequest"] = {
    "program": props.id,
    "step_type": "reagent",
    "cell_x": stainer.currentConfiguration.stations[0].cell_x,
    "cell_y": stainer.currentConfiguration.stations[0].cell_y,
    "reagent": stainer.currentConfiguration.stations[0].reagent,
    "seconds": 5,
    "stirring": "off",
    "precision": "exact",
    "order": step ? step.order + 1 : 1
  }
  let {error, response} = await client.POST(`/api/programs/steps/`, {
    body: newStep
  })
  if (error) {
    if (response.status == 401) {
      router.push('/login')
    }
  }
  await fetchProgram()
}

async function pasteStep(step: Step) {
  if (!copiedStep) return
  copiedStep.order = step.order + 1;
  copiedStep.program = props.id
  let {error, response} = await client.POST(`/api/programs/steps/`, {
    body: copiedStep
  })
  if (error) {
    if (response.status == 401) {
      router.push('/login')
    }
  }
  await fetchProgram()
}

async function updateStep(step: Step) {
  let {error, response} = await client.PATCH(`/api/programs/steps/{id}/`, {
    params: {
      path: {
        id: step.id
      }
    },
    body: step
  })
  if (error) {
    if (response.status == 401) {
      router.push('/login')
    }
  }
  await fetchProgram()
}

async function updateName() {
  if (!editProgram.value?.name) return
  let {error, response} = await client.PATCH(`/api/programs/programs/{id}/`, {
    params: {
      path: {
        id: props.id
      }
    },
    body: {name: editProgram.value.name}
  })
  if (error) {
    if (response.status == 401) {
      router.push('/login')
    }
  }
  await fetchProgram()
  await stainer.fetchCurrentConfiguration()
}

function getTime(sec: number){
    const hours = ('0' + Math.floor(sec / 3600)).slice(-2)
    const minutes = ('0' + Math.floor((sec % 3600) / 60)).slice(-2)
    const seconds = ('0' + sec % 60).slice(-2)
    return `${hours}:${minutes}:${seconds}`
}

const input = ref()
const showKeyboard = ref(false)
const showTimePicker: Ref<number | undefined> = ref();
const showActions = ref()

function getReagent(reagentId: number | null | undefined) {
  if (!reagentId) return
  let fetchedReagent = stainer.reagents.filter(reagent => reagent.id === reagentId)[0];
  if (!fetchedReagent) return
  if (fetchedReagent.short_name) return fetchedReagent.short_name;
  else return fetchedReagent.long_name;
}
</script>

<template>
  <div v-if="program && editProgram" class="w-5/6 h-2/3">
    <div v-if="showGrid" class="absolute w-full bg-white border-black border rounded-xl z-50 -mt-2 p-4">
      <Grid @selected-cell="cell => {editReagent(cell); showGrid=false}"/>
    </div>
    <div class="grid mx-12 grid-cols-[1fr_14fr] mb-4 w-full h-12">
      <div></div>
      <div class="login-border relative">
        <input @click="showKeyboard = true" type="text" v-model="editProgram.name" class="w-full h-full rounded-lg p-2"
               placeholder="Введите название программы "/>
        <Edit class="absolute right-0 top-0 m-3"/>
      </div>
    </div>
    <div v-show="showKeyboard" class="absolute z-50 w-4/5 left-0 right-0 my-0 mx-auto flex justify-center">
      <TestKeyboard @hide='() => {showKeyboard= false; updateName()}' @show="showKeyboard=true"/>
    </div>
    <div class="grid mx-12 w-full z-0 col-span-7 bg-white auto-rows-[70px] grid-cols-[1fr_1fr_2fr_4fr_2fr_3fr_2fr]">
      <div class=""></div>
      <div class="border-grey-3 border-[1px] sticky flex items-center p-2">Шаг</div>
      <div class="border-grey-3 border-[1px] sticky flex items-center p-2">№ станции</div>
      <div class="border-grey-3 border-[1px] sticky flex items-center p-2">Реагент</div>
      <div class="border-grey-3 border-[1px] sticky flex items-center p-2">Время</div>
      <div class="border-grey-3 border-[1px] sticky flex items-center p-2">Перемешивание</div>
      <div class="border-grey-3 border-[1px] sticky flex items-center p-2">Задержка</div>
    </div>
    <div
        class="w-full mx-12 h-3/4 max-h-[15rem] hide-scrollbar overflow-y-auto inline-grid auto-rows-[70px] grid-cols-[1fr_1fr_2fr_4fr_2fr_3fr_2fr]">
      <template v-for="(step) in program.steps">
        <div class="flex justify-center items-center">
          <div>
            <More @click="showActions=step.id" class="overflow-visible"/>
            <Actions v-if="showActions === step.id" @delete="deleteStep(step)" @add="addStep(step)"
                     @copy="copiedStep = Object.assign({program: props.id}, step)" @paste="pasteStep(step)" @hide="showActions=''"
                     class="z-50 absolute bottom-36 left-14"/>
            <div @click.exact="showActions=''" v-if="showActions === step.id"
                 class="absolute z-10 modal w-full h-full top-0 left-0">
            </div>
          </div>
        </div>
        <div class="border-grey-3 border-[1px] flex items-center p-2">
          {{ step.order }}
        </div>
        <div class="border-grey-3 border-[1px] flex items-center p-2">{{ processStation(step) }}</div>
        <div @click="showGrid = true; selectedStep = step" class=" border-grey-3 border-[1px] flex items-center p-2">
          {{ processStep(step) }}
        </div>
        <div @click="showTimePicker = step.id"
             class="overflow-visible border-grey-3 border-[1px] w-full flex items-center p-2">
          <span>{{ getTime(step.seconds) }}</span>
        </div>
        <div v-if="showTimePicker === step.id" @click.exact="showTimePicker= undefined"
             class="absolute top-0 left-0 w-screen h-screen flex justify-center items-center">
          <TimePicker @click.stop @time="time => {step.seconds = time; updateStep(step)}"
                      :given-time="step.seconds" v-model:show="showTimePicker"/>
        </div>
        <div class="border-grey-3 border-[1px] flex items-center p-2">
          <select @change="updateStep(step)" v-model="step.stirring" class="bg-white">
            <option value="off" :selected="'off' === step.stirring">ВЫКЛ</option>
            <option value="fast" :selected="'fast' === step.stirring">Быстро</option>
            <option value="slow" :selected="'slow' === step.stirring">Медленно</option>
          </select>
        </div>
        <div class="border-grey-3 border-[1px] flex items-center p-2">
          <select @change="updateStep(step)" v-model="step.precision" class="bg-white">
            <option value="exact" :selected="'exact' === step.precision">точно</option>
            <option value="percent_20" :selected="'percent_20' === step.precision">+20%</option>
            <option value="percent_50" :selected="'percent_50' === step.precision">+50%</option>
            <option value="unlimited" :selected="'unlimited' === step.precision">неогр.</option>
          </select>
        </div>
      </template>
    </div>
  </div>
  <div class="absolute bottom-0 mb-8 flex justify-between w-full px-12">
    <button @click="showGrid ? showGrid=false : router.go(-1)"
            class="main-button flex items-center justify-center gap-2 w-1/6">
      <LeftArrow/>
      Назад
    </button>
    <button @click="router.push('/edit-program')" class="main-button w-1/4">Сохранить</button>
  </div>
  <div class="footer"></div>
</template>

<style>
.bg-black {
  background-color: black;
}

.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  scrollbar-width: none;  /* Firefox */
  -ms-overflow-style: none;  /* IE and Edge */
}
</style>
```