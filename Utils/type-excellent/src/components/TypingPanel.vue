<template>
    <v-container class="whole-pad">
        <span class="letter-group" v-for="group in letterGroups" :key="group.id">
            <span class="letter-pair" v-for="letterCell in group.letterCells" :key="letterCell.id">
                <span class="finger-number">{{ mappingLettersToFingers[letterCell.letter]['finger'] }}</span>
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

interface letterCell {
    id: number
    letter: string
}

interface LetterGroup {
    id: number
    letterCells: letterCell[]
}

interface FingerInfo {
    hand: "L" | "R" | "B";  // left, right, both
    finger: number;
    row: number;
    shift: boolean;
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
    }
})

const emit = defineEmits(["typingComplete"])

const lettersToType = ref<string[]>([])
const lettersUserTyped = ref<string[]>([])
const lettersUserTypedIncorrect = ref<string[]>([])

const letterGroups: ComputedRef<LetterGroup[]> = computed(() => {
    // Create the letter groups
    const groups = []
    for (let i = 0; i < props.numberOfGroups; i++) {
        // letters is array of {letter, idx}
        let letterCells: letterCell[] = []
        for (let j = 0; j < props.numberOfLettersPerGroup; j++) {
            let idx = i * props.numberOfLettersPerGroup + j
            // Generate a random letter
            const letter = String.fromCharCode(97 + (i * props.numberOfLettersPerGroup + j) % 26)
            const letterCell: letterCell = {
                id: idx,
                letter: letter
            }
            letterCells.push(letterCell)
            // Add the letter to lettersToType
            lettersToType.value.push(letter)
        }
        const group: LetterGroup = {
            id: i,
            letterCells: letterCells
        }
        groups.push(group)
    }
    return groups
})

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

    // Add the typed letter to lettersUserTyped
    lettersUserTyped.value.push(typedLetter)
    let idx = lettersUserTyped.value.length - 1
    // Check if the typed letter is correct
    if (typedLetter !== lettersToType.value[idx]) {
        // Add the typed letter to lettersUserTypedIncorrect
        lettersUserTypedIncorrect.value.push(typedLetter)
    } else {
        lettersUserTypedIncorrect.value.push("")
    }

    // Check if the count reached the total
    const totalLetters = props.numberOfGroups * props.numberOfLettersPerGroup
    if (lettersUserTyped.value.length === totalLetters) {
        // Notify the parent with the letters to type and the user typed letters
        emit("typingComplete", {
            lettersToType: lettersToType.value,
            lettersUserTyped: lettersUserTyped.value
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

onMounted(() => {
    window.addEventListener('keypress', handleKeyPress);
});

onUnmounted(() => {
    window.removeEventListener('keypress', handleKeyPress);
});

// prepare the mapping of letters to fingers
const keyboardLayout = {
    "L": [
        { row: 2, keys: ['1', '2', '3', '4', '5'] },
        { row: 1, keys: ['q', 'w', 'e', 'r', 't'] },
        { row: 0, keys: ['a', 's', 'd', 'f', 'g'] },
        { row: -1, keys: ['z', 'x', 'c', 'v', 'b'] },
    ],
    "R": [
        { row: 2, keys: ['6', '7', '8', '9', '0', '-', '='] },
        { row: 1, keys: ['y', 'u', 'i', 'o', 'p', '[', ']', '\\'] },
        { row: 0, keys: ['h', 'j', 'k', 'l', ';', "'"] },
        { row: -1, keys: ['n', 'm', ',', '.', '/'] },
    ],
    "shift": [
        { hand: "L", finger: 1, row: 2, keys: ['!', '@', '#', '$', '%'] },
        { hand: "R", finger: 1, row: 2, keys: ['^', '&', '*', '(', ')', '_', '+'] },
        { hand: "L", finger: 1, row: 1, keys: ['Q', 'W', 'E', 'R', 'T'] },
        { hand: "R", finger: 1, row: 1, keys: ['Y', 'U', 'I', 'O', 'P', '{', '}', '|'] },
        { hand: "L", finger: 1, row: 0, keys: ['A', 'S', 'D', 'F', 'G'] },
        { hand: "R", finger: 1, row: 0, keys: ['H', 'J', 'K', 'L', ':', '"'] },
        { hand: "L", finger: 1, row: -1, keys: ['Z', 'X', 'C', 'V', 'B'] },
        { hand: "R", finger: 1, row: -1, keys: ['N', 'M', '<', '>', '?'] },
    ],
}

function generateCharToFinger(layout: any): Record<string, FingerInfo> {
    const charToFinger: Record<string, FingerInfo> = {};

    for (const hand of (['L', 'R'] as const)) {
        for (const { row, keys } of layout[hand]) {
            for (let i = 0; i < keys.length; i++) {
                const finger = i < 3 ? i + 1 : 4;
                charToFinger[keys[i]] = { hand, finger, row, shift: false };
            }
        }
    }

    for (const { hand, finger, row, keys } of layout['shift']) {
        for (const key of keys) {
            charToFinger[key] = { hand, finger, row, shift: true };
        }
    }

    return charToFinger;
}

const mappingLettersToFingers = generateCharToFinger(keyboardLayout);

</script>

<style scoped>
.whole-pad {
    background-color: lightyellow;
    min-width: 800px;
    display: flex;
    gap: 50px 15px;
    flex-flow: row wrap;
    font-family: monospace;
    font-size: 1.2rem;
    justify-content: flex-start;
}

.letter-group {
    display: flex;
    flex-flow: row nowrap;
    row-gap: 0;
}

.letter-pair {
    display: flex;
    flex-flow: column;
    column-gap: 0;
}

.letter-pair span {
    line-height: 1;
}

.finger-number {
    opacity: 0.3;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 0.8rem;
    font-weight: 100;
}

.incorrect-indicator {
    height: 1ch;
}

.typing {
    text-decoration: underline;
}

.typed-correct {
    color: darkcyan;
    font-weight: bold;
}

.typed-incorrect {
    color: crimson;
    font-weight: bold;
}

span.not-typed {
    color: black;
}
</style>