<template>
    <v-app style="background-color:lightblue; width: max-content;">
        <v-main class="main-content">
            <v-container style="border: solid 1px yellow;">
                <!-- Typing Panel -->
                <typing-panel :numberOfGroups="numberOfGroups" :numberOfLettersPerGroup="numberOfLettersPerGroup"
                    :level="level" style="border: solid 1px gray;"></typing-panel>
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
        const level = ref(1)

        return {
            dialogVisible,
            numberOfGroups,
            numberOfLettersPerGroup,
            level
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
