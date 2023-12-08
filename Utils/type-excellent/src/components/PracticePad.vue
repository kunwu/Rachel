<template>
    <v-app style="background-color:lightblue; width: max-content;">
        <v-main class="main-content">
            <v-container style="border: solid 1px yellow;">
                <!-- Typing Panel -->
                <typing-panel :numberOfGroups="numberOfGroups" :numberOfLettersPerGroup="numberOfLettersPerGroup"
                    :level="level" style="border: solid 1px gray;"></typing-panel>
                <v-container>
                    <v-row>
                        <v-col cols="12">
                            <v-expansion-panels multiple v-model="configPanel">
                                <v-expansion-panel>
                                    <v-expansion-panel-title>Configuration</v-expansion-panel-title>
                                    <v-expansion-panel-text>
                                        <v-row>
                                            <v-col cols="3">
                                                <v-slider v-model="level" :max="4" :min="0" step="1" thumb-label
                                                    label="Level"></v-slider>
                                            </v-col>
                                        </v-row>
                                    </v-expansion-panel-text>
                                </v-expansion-panel>
                            </v-expansion-panels>
                        </v-col>
                    </v-row>
                </v-container>
                <!-- Evaluation Panel -->
                <evaluation-panel></evaluation-panel>
                <!-- Dialog -->
                <v-row>
                    <v-col cols="12">
                        <v-dialog v-model="dialogVisible" max-width="500px">
                            <v-card>
                                <v-card-title>
                                    Dialog Title
                                </v-card-title>
                                <v-card-text>
                                    Dialog Content
                                </v-card-text>
                                <v-card-actions>
                                    <v-btn @click="dialogVisible = false">Close</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
    </v-app>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import TypingPanel from './TypingPanel.vue'
import EvaluationPanel from './EvaluationPanel.vue'

export default defineComponent({
    components: {
        TypingPanel,
        EvaluationPanel
    },
    setup() {
        const dialogVisible = ref(false)
        const numberOfGroups = ref(40)
        const numberOfLettersPerGroup = ref(4)
        const level = ref(0)
        const configPanel = ref(null)

        return {
            dialogVisible,
            numberOfGroups,
            numberOfLettersPerGroup,
            level,
            configPanel
        }
    }
})
</script>

<style scoped>
.main-content {
    display: flex;
    border: solid 1px green;
}
</style>
