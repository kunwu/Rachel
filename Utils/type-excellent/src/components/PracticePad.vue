<template>
    <v-app style="background-color:lightblue; width: max-content;">
        <v-main class="main-content">
            <v-container style="border: solid 1px yellow;">
                <!-- Typing Panel -->
                <typing-panel :numberOfGroups="numberOfGroups" :numberOfLettersPerGroup="numberOfLettersPerGroup"
                    :level="level" :regenerateCount="regenerateCount" :showFinger="showFinger" :enableSound="enableSound"
                    @typingComplete="handleTypingComplete" style="border: solid 1px gray;"></typing-panel>
                <v-container>
                    <v-row>
                        <v-col cols="12">
                            <v-expansion-panels multiple v-model="configPanel">
                                <v-expansion-panel>
                                    <v-expansion-panel-title>Configuration</v-expansion-panel-title>
                                    <v-expansion-panel-text>
                                        <v-row>
                                            <v-col cols="3">
                                                <v-select v-model="level" color="primary" :items="[0, 1, 2, 3, 4]"
                                                    label="Level"></v-select>
                                            </v-col>
                                            <v-col cols="3">
                                                <v-select v-model="numberOfGroups" color="primary"
                                                    :items="[1, 2, 4, 10, 20]" label="Groups"></v-select>
                                            </v-col>
                                            <v-col cols="3">
                                                <v-switch v-model="showFinger" color="primary" label="Finger"></v-switch>
                                            </v-col>
                                            <v-col cols="3">
                                                <v-switch v-model="enableSound" color="primary" label="Sound"></v-switch>
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
                        <v-dialog v-model="dialogVisible" @open="handleDialogOpen" @close="handleDialogClose"
                            max-width="500px">
                            <v-card>
                                <v-card-text>
                                    {{ dialogContent }}
                                </v-card-text>
                                <v-card-actions>
                                    <v-btn color="primary" @click="dialogVisible = true">Close</v-btn>
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
import { defineComponent, ref, nextTick } from 'vue'
import TypingPanel from './TypingPanel.vue'
import EvaluationPanel from './EvaluationPanel.vue'

export default defineComponent({
    components: {
        TypingPanel,
        EvaluationPanel
    },
    setup() {
        // dialog
        const dialogVisible = ref(false)
        const dialogContent = ref('')
        // params
        const numberOfGroups = ref(1)
        const numberOfLettersPerGroup = ref(4)
        const level = ref(0)
        const showFinger = ref(true)
        const enableSound = ref(true)
        // regenerate control
        const regenerateCount = ref(0)
        // config panel
        const configPanel = ref(null)

        const handleTypingComplete = ({ lettersToType, lettersUserTyped }: { lettersToType: string[], lettersUserTyped: string[] }): void => {
            let countCorrect = 0
            const total = lettersToType.length
            for (let i = 0; i < total; i++) {
                if (lettersToType[i] === lettersUserTyped[i]) {
                    countCorrect++
                }
            }

            let msg = ''
            if (countCorrect === total) {
                msg = 'Awsome! You are a typing master!'
            } else if (countCorrect / total >= 0.8) {
                msg = 'Good job! You are almost there.'
            } else if (countCorrect / total >= 0.6) {
                msg = 'Cool! You are doing well.'
            } else if (countCorrect / total >= 0.4) {
                msg = 'Not bad. Keep going.'
            } else if (countCorrect / total >= 0.2) {
                msg = 'I like your spirit. Keep going.'
            } else {
                msg = 'Good start. Let\'s prace more.'
            }

            dialogContent.value = `You typed ${countCorrect} out of ${total} correctly.` + ' ' + msg
            dialogVisible.value = true
            handleDialogOpen()
        }

        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key === 'Enter' && dialogVisible.value) {
                handleDialogClose()
            }
        }

        const handleDialogOpen = async () => {
            window.addEventListener('keydown', handleKeyDown)
        }

        const handleDialogClose = (): void => {
            dialogVisible.value = false
            regenerateLetterGroups()
            window.removeEventListener('keydown', handleKeyDown)
        }

        const regenerateLetterGroups = (): void => {
            regenerateCount.value++
        }

        return {
            dialogVisible,
            dialogContent,
            numberOfGroups,
            numberOfLettersPerGroup,
            level,
            showFinger,
            enableSound,
            regenerateCount,
            configPanel,
            handleDialogOpen,
            handleDialogClose,
            handleTypingComplete
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
