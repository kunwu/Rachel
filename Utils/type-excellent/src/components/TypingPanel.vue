<template>
    <v-container class="whole-pad">
        <span class="letter-group" v-for="group in letterGroups" :key="group.id">
            <span class="letter-column" v-for="letterCell in group.letterCells" :key="letterCell.id">
                <span class="finger-number">{{ keyboardLayout[letterCell.letter]['finger'] }}</span>
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

interface FingerInfo {
    hand: "L" | "R" | "B";  // left, right, both
    finger: number;
    row: number;
    shift: 0 | 1 | 2;   // 0: no shift, 1: shift, 2: both
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
    regenerateCount: {
        type: Number,
        required: true
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
        if (audioPlayerWarning.value) {
            audioPlayerWarning.value.currentTime = 0;
            audioPlayerWarning.value.play();
        }
    } else {
        lettersUserTypedIncorrect.value.push("")
        if (audioPlayerTyping.value) {
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

onMounted(() => {
    window.addEventListener('keypress', handleKeyPress);
});

onUnmounted(() => {
    window.removeEventListener('keypress', handleKeyPress);
});

// prepare the mapping of letters to fingers
const keyboardLayout: Record<string, FingerInfo> = {
    "`": { hand: "L", finger: 4, row: 2, shift: 0 },
    "1": { hand: "L", finger: 4, row: 2, shift: 0 },
    "2": { hand: "L", finger: 3, row: 2, shift: 0 },
    "3": { hand: "L", finger: 2, row: 2, shift: 0 },
    "4": { hand: "L", finger: 1, row: 2, shift: 0 },
    "5": { hand: "L", finger: 1, row: 2, shift: 0 },
    "6": { hand: "R", finger: 1, row: 2, shift: 0 },
    "7": { hand: "R", finger: 1, row: 2, shift: 0 },
    "8": { hand: "R", finger: 2, row: 2, shift: 0 },
    "9": { hand: "R", finger: 3, row: 2, shift: 0 },
    "0": { hand: "R", finger: 4, row: 2, shift: 0 },
    "-": { hand: "R", finger: 4, row: 2, shift: 0 },
    "=": { hand: "R", finger: 4, row: 2, shift: 0 },
    "~": { hand: "L", finger: 4, row: 2, shift: 1 },
    "!": { hand: "L", finger: 4, row: 2, shift: 1 },
    "@": { hand: "L", finger: 3, row: 2, shift: 1 },
    "#": { hand: "L", finger: 2, row: 2, shift: 1 },
    "$": { hand: "L", finger: 1, row: 2, shift: 1 },
    "%": { hand: "L", finger: 1, row: 2, shift: 1 },
    "^": { hand: "R", finger: 1, row: 2, shift: 1 },
    "&": { hand: "R", finger: 1, row: 2, shift: 1 },
    "*": { hand: "R", finger: 2, row: 2, shift: 1 },
    "(": { hand: "R", finger: 3, row: 2, shift: 1 },
    ")": { hand: "R", finger: 4, row: 2, shift: 1 },
    "_": { hand: "R", finger: 4, row: 2, shift: 1 },
    "+": { hand: "R", finger: 4, row: 2, shift: 1 },
    "q": { hand: "L", finger: 4, row: 1, shift: 0 },
    "w": { hand: "L", finger: 3, row: 1, shift: 0 },
    "e": { hand: "L", finger: 2, row: 1, shift: 0 },
    "r": { hand: "L", finger: 1, row: 1, shift: 0 },
    "t": { hand: "L", finger: 1, row: 1, shift: 0 },
    "y": { hand: "R", finger: 1, row: 1, shift: 0 },
    "u": { hand: "R", finger: 1, row: 1, shift: 0 },
    "i": { hand: "R", finger: 2, row: 1, shift: 0 },
    "o": { hand: "R", finger: 3, row: 1, shift: 0 },
    "p": { hand: "R", finger: 4, row: 1, shift: 0 },
    "[": { hand: "R", finger: 4, row: 1, shift: 0 },
    "]": { hand: "R", finger: 4, row: 1, shift: 0 },
    "\\": { hand: "R", finger: 4, row: 1, shift: 0 },
    "Q": { hand: "L", finger: 4, row: 1, shift: 1 },
    "W": { hand: "L", finger: 3, row: 1, shift: 1 },
    "E": { hand: "L", finger: 2, row: 1, shift: 1 },
    "R": { hand: "L", finger: 1, row: 1, shift: 1 },
    "T": { hand: "L", finger: 1, row: 1, shift: 1 },
    "Y": { hand: "R", finger: 1, row: 1, shift: 1 },
    "U": { hand: "R", finger: 1, row: 1, shift: 1 },
    "I": { hand: "R", finger: 2, row: 1, shift: 1 },
    "O": { hand: "R", finger: 3, row: 1, shift: 1 },
    "P": { hand: "R", finger: 4, row: 1, shift: 1 },
    "{": { hand: "R", finger: 4, row: 1, shift: 1 },
    "}": { hand: "R", finger: 4, row: 1, shift: 1 },
    "|": { hand: "R", finger: 4, row: 1, shift: 1 },
    "a": { hand: "L", finger: 4, row: 0, shift: 0 },
    "s": { hand: "L", finger: 3, row: 0, shift: 0 },
    "d": { hand: "L", finger: 2, row: 0, shift: 0 },
    "f": { hand: "L", finger: 1, row: 0, shift: 0 },
    "g": { hand: "L", finger: 1, row: 0, shift: 0 },
    "h": { hand: "R", finger: 1, row: 0, shift: 0 },
    "j": { hand: "R", finger: 1, row: 0, shift: 0 },
    "k": { hand: "R", finger: 2, row: 0, shift: 0 },
    "l": { hand: "R", finger: 3, row: 0, shift: 0 },
    ";": { hand: "R", finger: 4, row: 0, shift: 0 },
    "'": { hand: "R", finger: 4, row: 0, shift: 0 },
    "A": { hand: "L", finger: 4, row: 0, shift: 1 },
    "S": { hand: "L", finger: 3, row: 0, shift: 1 },
    "D": { hand: "L", finger: 2, row: 0, shift: 1 },
    "F": { hand: "L", finger: 1, row: 0, shift: 1 },
    "G": { hand: "L", finger: 1, row: 0, shift: 1 },
    "H": { hand: "R", finger: 1, row: 0, shift: 1 },
    "J": { hand: "R", finger: 1, row: 0, shift: 1 },
    "K": { hand: "R", finger: 2, row: 0, shift: 1 },
    "L": { hand: "R", finger: 3, row: 0, shift: 1 },
    ":": { hand: "R", finger: 4, row: 0, shift: 1 },
    "\"": { hand: "R", finger: 4, row: 0, shift: 1 },
    "z": { hand: "L", finger: 4, row: -1, shift: 0 },
    "x": { hand: "L", finger: 3, row: -1, shift: 0 },
    "c": { hand: "L", finger: 2, row: -1, shift: 0 },
    "v": { hand: "L", finger: 1, row: -1, shift: 0 },
    "b": { hand: "L", finger: 1, row: -1, shift: 0 },
    "n": { hand: "R", finger: 1, row: -1, shift: 0 },
    "m": { hand: "R", finger: 1, row: -1, shift: 0 },
    ",": { hand: "R", finger: 2, row: -1, shift: 0 },
    ".": { hand: "R", finger: 3, row: -1, shift: 0 },
    "/": { hand: "R", finger: 4, row: -1, shift: 0 },
    "Z": { hand: "L", finger: 4, row: -1, shift: 1 },
    "X": { hand: "L", finger: 3, row: -1, shift: 1 },
    "C": { hand: "L", finger: 2, row: -1, shift: 1 },
    "V": { hand: "L", finger: 1, row: -1, shift: 1 },
    "B": { hand: "L", finger: 1, row: -1, shift: 1 },
    "N": { hand: "R", finger: 1, row: -1, shift: 1 },
    "M": { hand: "R", finger: 1, row: -1, shift: 1 },
    "<": { hand: "R", finger: 2, row: -1, shift: 1 },
    ">": { hand: "R", finger: 3, row: -1, shift: 1 },
    "?": { hand: "R", finger: 4, row: -1, shift: 1 },
};

// letter group generation
type LevelConfig =
    {
        row: number, fingers: number[], hands: string[], shift: number
    }[][];

const levelConfig: LevelConfig = [
    [{ row: 0, fingers: [1], hands: ['L', 'R'], shift: 0 }],
    [
        { row: 0, fingers: [1, 2, 3, 4], hands: ['L'], shift: 0 },
        { row: 0, fingers: [1, 2, 3], hands: ['R'], shift: 0 }
    ],
    [{ row: 0, fingers: [1, 2, 3, 4], hands: ['L', 'R'], shift: 0 }],
    [
        { row: 0, fingers: [1, 2, 3, 4], hands: ['L', 'R'], shift: 0 },
        { row: 1, fingers: [1, 2], hands: ['L', 'R'], shift: 0 },
    ],
    [
        { row: 0, fingers: [1, 2, 3, 4], hands: ['L', 'R'], shift: 2 },
        { row: 1, fingers: [1, 2, 3, 4], hands: ['L', 'R'], shift: 0 },
    ],
];

const generateLetterCandidateSet = (levelConfig: LevelConfig, level: number): string[] => {
    const candidateSet: string[] = [];
    const config = levelConfig[level];
    // iterate through keyboadLayout
    for (const [key, value] of Object.entries(keyboardLayout)) {
        // iterate through config
        for (const c of config) {
            // check if the key matches the config
            if (
                c.row === value.row &&
                c.fingers.includes(value.finger) &&
                c.hands.includes(value.hand) &&
                (c.shift === 2 || c.shift === value.shift)
            ) {
                candidateSet.push(key);
            }
        }
    }

    return candidateSet;
};

const generateLetterArray = (numberOfGroups: number, numberOfLettersPerGroup: number, level: number): string[] => {
    const letters: string[] = []

    const candidateSet = generateLetterCandidateSet(levelConfig, level)
    const numberOfLetters = numberOfGroups * numberOfLettersPerGroup
    for (let i = 0; i < numberOfLetters; i++) {
        const letter = candidateSet[Math.floor(Math.random() * candidateSet.length)]
        letters.push(letter)
    }

    return letters
}

const generateLetterGroups = (): LetterGroup[] => {
    console.log(props.regenerateCount)
    const lettersGenerated = generateLetterArray(props.numberOfGroups, props.numberOfLettersPerGroup, props.level)
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

.finger-number {
    text-align: center;
    opacity: 0.3;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 0.8rem;
    font-weight: 100;
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