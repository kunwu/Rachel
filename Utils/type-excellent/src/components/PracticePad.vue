<template>
    <v-app style="background-color:lightblue; width: max-content;">
        <v-main class="main-content">
            <v-container style="border: solid 1px yellow;">
                <!-- Typing Panel -->
                <typing-panel :numberOfGroups="numberOfGroups" :numberOfLettersPerGroup="numberOfLettersPerGroup"
                    :level="level" :levelForFrequency="levelForFrequency" :regenerateCount="regenerateCount"
                    :showFinger="showFinger" :enableSound="enableSound" @typingComplete="handleTypingComplete"
                    style="border: solid 1px gray;"></typing-panel>
                <!-- level for frequency -->
                <v-col cols="12" class="mt-10">
                    <v-slider v-model="levelForFrequency" step="1" thumb-label="always" color="primary"
                        :max="levelGroupsForFrequencyOptions.length - 1" label="LevelbyAI"></v-slider>
                </v-col>
                <!-- level indicator -->
                <!-- <v-col cols="12" class="mt-5">
                    <v-slider v-model="level" step="1" thumb-label="always" color="primary" :max="levelOptions.length - 1"
                        label="Level"></v-slider>
                </v-col> -->
                <!-- Configuration Box -->
                <v-container>
                    <v-row>
                        <v-col cols="12">
                            <v-expansion-panels multiple v-model="configPanel">
                                <v-expansion-panel variant="accordion">
                                    <v-expansion-panel-title>Configuration</v-expansion-panel-title>
                                    <v-expansion-panel-text>
                                        <v-row>
                                            <!-- <v-col cols="3">
                                                <v-select v-model="level" color="primary" :items="levelOptions"
                                                    label="Level"></v-select>
                                            </v-col> -->
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
                                            <!-- regenerate button -->
                                            <v-col cols="3">
                                                <v-btn color="primary" @click="regenerateCount++">Regenerate</v-btn>
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
                        <v-dialog v-model="dialogVisible" :hide-overlay="true" :persistent="true" max-width="30%">
                            <v-card>
                                <v-card-text>
                                    <v-row>
                                        <v-col cols="3">
                                            <v-progress-circular v-if="dialogCountDown >= 0" :size="70" :width="7"
                                                :model-value="dialogCountDown * (100 / (dialogCountDownSeconds * 10))"
                                                color="primary"></v-progress-circular>
                                        </v-col>
                                        <v-col cols="9">
                                            <div v-html="dialogContent"></div>
                                        </v-col>
                                    </v-row>
                                </v-card-text>
                                <v-card-actions>
                                    <v-btn color="primary" @click="dialogVisible = false">Close</v-btn>
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
import { defineComponent, ref, onMounted, watch } from 'vue'
import TypingPanel from './TypingPanel.vue'
import EvaluationPanel from './EvaluationPanel.vue'
import { levelConfig, levelGroupsForFrequency, adjustLevelByFeedback } from './GobleConfig.vue'

export default defineComponent({
    components: {
        TypingPanel,
        EvaluationPanel
    },
    setup() {
        // dialog
        const dialogCountDownSeconds = 4
        const dialogVisible = ref(false)
        const dialogContent = ref('')
        const dialogCountDown = ref(dialogCountDownSeconds * 10)
        // params
        const numberOfGroups = ref(4)
        const numberOfLettersPerGroup = ref(4)
        const level = ref(1)
        const levelForFrequency = ref(0)
        let levelAdjustedTemp = levelForFrequency.value
        const showFinger = ref(true)
        const enableSound = ref(true)
        // regenerate control
        const regenerateCount = ref(0)
        // config panel
        const configPanel = ref(null)
        const levelOptions = ref(Array.from({ length: levelConfig.length }, (_, i) => i));
        const levelGroupsForFrequencyOptions = ref(Array.from({ length: levelGroupsForFrequency.length }, (_, i) => i));

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
                msg = 'Good start. Let\'s practice more.'
            }
            msg = "<p>" + msg + "</p>"

            levelAdjustedTemp = adjustLevelByFeedback(levelForFrequency.value, lettersToType, lettersUserTyped)
            if (levelAdjustedTemp > levelForFrequency.value) {

                msg += '<p><b>BTW: Your level is upgraded!</b></p>'
            }

            dialogContent.value = `You typed ${countCorrect} out of ${total} correctly.` + '<br/>' + msg
            dialogCountDown.value = dialogCountDownSeconds * 10
            dialogVisible.value = true
        }

        const regenerateLetterGroups = (): void => {
            regenerateCount.value++
        }

        const saveToLocalStorage = (): void => {
            localStorage.setItem('numberOfGroups', numberOfGroups.value.toString())
            localStorage.setItem('levelForFrequency', levelForFrequency.value.toString())
        }

        watch(dialogVisible, (newValue) => {
            if (newValue) {
                const intervalId = setInterval(() => {
                    if (dialogCountDown.value > 1) {
                        dialogCountDown.value--
                    } else {
                        dialogVisible.value = false
                        clearInterval(intervalId)
                        if (levelAdjustedTemp > levelForFrequency.value) {
                            levelForFrequency.value = levelAdjustedTemp
                        }
                        regenerateLetterGroups()
                    }
                }, 100);
            }
        });

        watch(numberOfGroups, saveToLocalStorage);
        watch(levelForFrequency, saveToLocalStorage);

        onMounted(() => {
            numberOfGroups.value = localStorage.getItem('numberOfGroups') ? parseInt(localStorage.getItem('numberOfGroups')!) : 4
            levelForFrequency.value = localStorage.getItem('levelForFrequency') ? parseInt(localStorage.getItem('levelForFrequency')!) : 0
            levelAdjustedTemp = levelForFrequency.value
        });

        return {
            dialogVisible,
            dialogContent,
            dialogCountDownSeconds,
            dialogCountDown,
            numberOfGroups,
            numberOfLettersPerGroup,
            level,
            levelForFrequency,
            showFinger,
            enableSound,
            regenerateCount,
            configPanel,
            levelOptions,
            levelGroupsForFrequencyOptions,
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
