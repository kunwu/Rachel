<template>
    <v-container class="whole-pad">
        <span class="letter-group" v-for="group in letterGroups" :key="group.id">
            <span class="letter-column" v-for="letterCell in group.letterCells" :key="letterCell.id">
                <span :class="getFingerClass(letterCell.letter)">{{ keyboardLayout[letterCell.letter]['finger'] }}</span>
                <span :class="getLetterClass(letterCell.id)">{{ letterCell.letter }}</span>
                <span class="incorrect-indicator">{{ lettersUserTypedIncorrect[letterCell.id] }}</span>
            </span>
        </span>
    </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { ComputedRef } from 'vue'
import { onMounted, onUnmounted } from 'vue';
import { keyboardLayout, generateLetterArray, generateLetterArrayByFeedback } from './GobleConfig.vue';
import typingSound from '@/assets/sounds/typing.mp3'
import warningSound from '@/assets/sounds/warning.mp3'

interface letterCell {
    id: number
    letter: string
}

interface LetterGroup {
    id: number
    letterCells: letterCell[]
}

const props = defineProps({
    numberOfGroups: {
        type: Number,
        required: true
    },
    numberOfLettersPerGroup: {
        type: Number,
        required: true
    },
    level: {
        type: Number,
        required: true
    },
    levelForFrequency: {
        type: Number,
        required: true
    },
    regenerateCount: {
        type: Number,
        required: true
    },
    enableSound: {
        type: Boolean,
        required: false
    },
    showFinger: {
        type: Boolean,
        required: false
    }
})

const emit = defineEmits(["typingComplete"])

const lettersToType = ref<string[]>([])
const lettersUserTyped = ref<string[]>([])
const lettersUserTypedIncorrect = ref<string[]>([])

const letterGroups: ComputedRef<LetterGroup[]> = computed(() => generateLetterGroups())

const audioPlayerTyping = ref(new Audio(typingSound))
const audioPlayerWarning = ref(new Audio(warningSound))

const handleKeyPress = (event: KeyboardEvent) => {
    const typedLetter = event.key
    // Handle user keyboard typing input
    // Ignore keys that are not normal displayable keys
    if (event.key.length !== 1) {
        return
    }
    if (event.key === ' ') {
        event.preventDefault()
    }

    const totalLetters = props.numberOfGroups * props.numberOfLettersPerGroup
    if (lettersUserTyped.value.length === totalLetters) {
        return
    }

    // Add the typed letter to lettersUserTyped
    lettersUserTyped.value.push(typedLetter)
    let idx = lettersUserTyped.value.length - 1
    // Check if the typed letter is correct
    if (typedLetter !== lettersToType.value[idx]) {
        // Add the typed letter to lettersUserTypedIncorrect
        lettersUserTypedIncorrect.value.push(typedLetter)
        if (props.enableSound && audioPlayerWarning.value) {
            audioPlayerWarning.value.currentTime = 0;
            audioPlayerWarning.value.play();
        }
    } else {
        lettersUserTypedIncorrect.value.push("")
        if (props.enableSound && audioPlayerTyping.value) {
            audioPlayerTyping.value.currentTime = 0;
            audioPlayerTyping.value.play();
        }
    }

    // Check if the count reached the total
    if (lettersUserTyped.value.length === totalLetters) {
        // Notify the parent with the letters to type and the user typed letters
        emit("typingComplete", {
            lettersToType: lettersToType.value.slice(),
            lettersUserTyped: lettersUserTyped.value.slice()
        })
    }
}

const getLetterClass = (id: number) => {
    if (id > lettersUserTypedIncorrect.value.length) {
        return 'not-typed'
    } else if (id == lettersUserTypedIncorrect.value.length && id < lettersToType.value.length) {
        return 'typing'
    }
    const letter = lettersUserTypedIncorrect.value[id]
    if (letter === '') {
        return 'typed-correct'
    } else {
        return 'typed-incorrect'
    }
}

const getFingerClass = (letter: string) => {
    if (!props.showFinger) {
        return 'finger-number finger-hide'
    }
    const hand = keyboardLayout[letter]['hand']
    const shift = keyboardLayout[letter]['shift']
    if (hand === 'L') {
        if (shift === 0) {
            return `finger-number hand-left`
        } else {
            return `finger-number hand-left finger-shift`
        }
    } else {
        if (shift === 0) {
            return `finger-number hand-right`
        } else {
            return `finger-number hand-right finger-shift`
        }
    }
}

onMounted(() => {
    window.addEventListener('keypress', handleKeyPress);
});

onUnmounted(() => {
    window.removeEventListener('keypress', handleKeyPress);
});

const generateLetterGroups = (): LetterGroup[] => {
    // do something to reference props.regenerateCount to enforce invoke of this function
    if (props.regenerateCount < 0) {
        console.log('something unexpected happen')
    }

    // const lettersGenerated = generateLetterArray(props.numberOfGroups, props.numberOfLettersPerGroup, props.level)
    const lettersGenerated = generateLetterArrayByFeedback(props.numberOfGroups * props.numberOfLettersPerGroup, props.levelForFrequency, lettersToType.value, lettersUserTyped.value)
    // reset letterToType and lettersUserTyped
    lettersToType.value = []
    lettersUserTyped.value = []
    lettersUserTypedIncorrect.value = []

    const groups = []
    for (let i = 0; i < props.numberOfGroups; i++) {
        let letterCells: letterCell[] = []
        for (let j = 0; j < props.numberOfLettersPerGroup; j++) {
            let idx = i * props.numberOfLettersPerGroup + j
            const letter = lettersGenerated[idx]
            const letterCell: letterCell = {
                id: idx,
                letter: letter
            }
            letterCells.push(letterCell)
            lettersToType.value.push(letter)
        }
        const group: LetterGroup = {
            id: i,
            letterCells: letterCells
        }
        groups.push(group)
    }
    return groups
}

</script>

<style scoped>
.whole-pad {
    padding: 50px 60px;
    background-color: lightyellow;
    min-width: 600px;
    display: flex;
    gap: 40px 20px;
    flex-flow: row wrap;
    font-family: monospace;
    font-size: 2rem;
    font-weight: lighter;
    justify-content: space-around;
}

.letter-group {
    display: flex;
    flex-flow: row nowrap;
    row-gap: 0;
}

.letter-column {
    display: flex;
    flex-flow: column;
    column-gap: 0;
}

.letter-column span {
    line-height: 1;
}

.finger-hide {
    visibility: hidden;
}

.finger-number {
    margin: 0 1px;
    opacity: 0.3;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 0.8rem;
    font-weight: 100;
}

.hand-left {
    text-align: left;
}

.hand-right {
    text-align: right;
}

.finger-shift {
    border-bottom: double 2px currentColor;
}

.incorrect-indicator {
    height: 1ch;
    text-align: center;
    font-size: 1.8rem;
}

.typing {
    color: gray;
    border-bottom: 2px solid currentColor;
}

.typed-correct {
    color: black;
}

.typed-incorrect {
    color: crimson;
    font-weight: bold;
}

.not-typed {
    color: gray;
}
</style>