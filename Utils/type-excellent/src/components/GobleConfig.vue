<script lang="ts">
import { defineComponent } from 'vue';

type FingerInfo = {
    hand: "L" | "R" | "B";  // left, right, both
    finger: number;
    row: number;
    shift: 0 | 1 | 2;   // 0: no shift, 1: shift, 2: both
}

export type LevelConfig = {
    row: number,
    fingers: number[],
    hands: string[],
    shift: number,
    frequency?: number
}[][];

// prepare the mapping of letters to fingers
export const keyboardLayout: Record<string, FingerInfo> = {
    "`": { hand: "L", finger: 4, row: 2, shift: 0 },
    "1": { hand: "L", finger: 4, row: 2, shift: 0 },
    "2": { hand: "L", finger: 3, row: 2, shift: 0 },
    "3": { hand: "L", finger: 2, row: 2, shift: 0 },
    "4": { hand: "L", finger: 1, row: 2, shift: 0 },
    "5": { hand: "L", finger: 0, row: 2, shift: 0 },
    "6": { hand: "R", finger: 0, row: 2, shift: 0 },
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
    "%": { hand: "L", finger: 0, row: 2, shift: 1 },
    "^": { hand: "R", finger: 0, row: 2, shift: 1 },
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
    "t": { hand: "L", finger: 0, row: 1, shift: 0 },
    "y": { hand: "R", finger: 0, row: 1, shift: 0 },
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
    "T": { hand: "L", finger: 0, row: 1, shift: 1 },
    "Y": { hand: "R", finger: 0, row: 1, shift: 1 },
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
    "g": { hand: "L", finger: 0, row: 0, shift: 0 },
    "h": { hand: "R", finger: 0, row: 0, shift: 0 },
    "j": { hand: "R", finger: 1, row: 0, shift: 0 },
    "k": { hand: "R", finger: 2, row: 0, shift: 0 },
    "l": { hand: "R", finger: 3, row: 0, shift: 0 },
    ";": { hand: "R", finger: 4, row: 0, shift: 0 },
    "'": { hand: "R", finger: 4, row: 0, shift: 0 },
    "A": { hand: "L", finger: 4, row: 0, shift: 1 },
    "S": { hand: "L", finger: 3, row: 0, shift: 1 },
    "D": { hand: "L", finger: 2, row: 0, shift: 1 },
    "F": { hand: "L", finger: 1, row: 0, shift: 1 },
    "G": { hand: "L", finger: 0, row: 0, shift: 1 },
    "H": { hand: "R", finger: 0, row: 0, shift: 1 },
    "J": { hand: "R", finger: 1, row: 0, shift: 1 },
    "K": { hand: "R", finger: 2, row: 0, shift: 1 },
    "L": { hand: "R", finger: 3, row: 0, shift: 1 },
    ":": { hand: "R", finger: 4, row: 0, shift: 1 },
    "\"": { hand: "R", finger: 4, row: 0, shift: 1 },
    "z": { hand: "L", finger: 4, row: -1, shift: 0 },
    "x": { hand: "L", finger: 3, row: -1, shift: 0 },
    "c": { hand: "L", finger: 2, row: -1, shift: 0 },
    "v": { hand: "L", finger: 1, row: -1, shift: 0 },
    "b": { hand: "L", finger: 0, row: -1, shift: 0 },
    "n": { hand: "R", finger: 0, row: -1, shift: 0 },
    "m": { hand: "R", finger: 1, row: -1, shift: 0 },
    ",": { hand: "R", finger: 2, row: -1, shift: 0 },
    ".": { hand: "R", finger: 3, row: -1, shift: 0 },
    "/": { hand: "R", finger: 4, row: -1, shift: 0 },
    "Z": { hand: "L", finger: 4, row: -1, shift: 1 },
    "X": { hand: "L", finger: 3, row: -1, shift: 1 },
    "C": { hand: "L", finger: 2, row: -1, shift: 1 },
    "V": { hand: "L", finger: 1, row: -1, shift: 1 },
    "B": { hand: "L", finger: 0, row: -1, shift: 1 },
    "N": { hand: "R", finger: 0, row: -1, shift: 1 },
    "M": { hand: "R", finger: 1, row: -1, shift: 1 },
    "<": { hand: "R", finger: 2, row: -1, shift: 1 },
    ">": { hand: "R", finger: 3, row: -1, shift: 1 },
    "?": { hand: "R", finger: 4, row: -1, shift: 1 },
};

export const levelGroupsForFrequency = [
    ['f', 'j'],
    ['g', 'h'],
    ['d', 's', 'k', 'l', 'a'],
    ['r', 'u'],
    ['t', 'y'],
    ['v', 'b', 'n', 'm'],
    ['e', 'i'],
    ['w', 'o'],
    ['q', 'p'],
    ['c', 'x', 'z'],
    [',', '.', '\'', '!'],
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
    ['+', '-', '*', '/', '=', '>', '<', '"', '?', '(', ')', '[', ']'],
    ['@', '#', '$', '%'],
    ['^', '&', '_', '|', '~', '\\', '{', '}']
];

export const adjustLevelByFeedback = (levelCurrent: number, lastLettersToType: string[], lastUserTyped: string[]): number => {
    let levelRet = levelCurrent;
    if (levelRet >= levelGroupsForFrequency.length) {
        return levelRet;
    }

    const falseCount: { [key: string]: number } = {}
    for (let i = 0; i < lastUserTyped.length; i++) {
        const letter = lastLettersToType[i];
        const typed = lastUserTyped[i];
        if (letter !== typed) {
            falseCount[letter] = (falseCount[letter] || 0) + 1;
        }
    }

    if ((lastUserTyped.length === lastLettersToType.length) && (Object.keys(falseCount).length === 0)) {
        levelRet = levelCurrent + 1;
    }

    return levelRet;
}

export const generateLetterArrayByFeedback = (numberOfLetters: number, levelCurrent: number, lastLettersToType: string[], lastUserTyped: string[]): string[] => {
    const FrequencyCurrent = 1000   // 当前组权重
    const FrequencyAdjust = 0.8    // 前一组权重比例
    const FalseThreshold = 2      // 错误阈值，超过阈值才提高权重
    const FalseAjust = 1.5          // 错误权重比例

    // 计算初始化权重
    const rawLetterFrequency: { [key: string]: number } = {};
    // 当前组直到第一组
    for (let i = levelCurrent; i >= 0; i--) {
        const letters = levelGroupsForFrequency[i];
        const frequency = FrequencyCurrent * Math.pow(FrequencyAdjust, levelCurrent - i);
        for (const letter of letters) {
            rawLetterFrequency[letter] = frequency;
        }
    }
    // 上轮错误字母的权限
    const falseCount: { [key: string]: number } = {}
    for (let i = 0; i < lastUserTyped.length; i++) {
        const letter = lastLettersToType[i];
        const typed = lastUserTyped[i];
        if (letter !== typed) {
            falseCount[letter] = (falseCount[letter] || 0) + 1;
        }
    }
    // 根据错误字母调整权重
    for (const [letter, count] of Object.entries(falseCount)) {
        if (count >= FalseThreshold) {
            rawLetterFrequency[letter] = FrequencyCurrent + FalseAjust;
        }
    }

    // print out to console.log the frequency of each letter in decreasing order, print in lines
    const sortedLetters = Object.entries(rawLetterFrequency).sort((a, b) => b[1] - a[1]);
    console.log(sortedLetters.map(([letter, frequency]) => `${letter}: ${frequency}`).join('\n'));

    const letters: string[] = generateLetterArrayByFrequency(rawLetterFrequency, numberOfLetters);
    return letters;
}

export const levelConfig: LevelConfig = [
    [
        { row: 0, fingers: [1], hands: ['L', 'R'], shift: 0 },
        { row: 0, fingers: [0], hands: ['L', 'R'], shift: 0, frequency: 0.5 }
    ],
    [
        { row: 0, fingers: [0, 1], hands: ['L', 'R'], shift: 0 },
    ],
    [
        { row: 0, fingers: [0, 1, 2], hands: ['L', 'R'], shift: 0 },
    ],
    [
        { row: 0, fingers: [0, 1, 2, 3], hands: ['L', 'R'], shift: 0 },
    ],
    [
        { row: 0, fingers: [0, 1, 2], hands: ['L', 'R'], shift: 0 },
        { row: 0, fingers: [4], hands: ['L'], shift: 0 },
    ],
    [
        { row: 0, fingers: [0, 1, 2], hands: ['L', 'R'], shift: 0, frequency: 0.5 },
        { row: 0, fingers: [4], hands: ['L'], shift: 0, frequency: 0.5 },
        { row: 1, fingers: [1], hands: ['L', 'R'], shift: 0 },
        { row: -1, fingers: [1], hands: ['L', 'R'], shift: 0 },
    ],
    [
        { row: 0, fingers: [0, 1, 2], hands: ['L', 'R'], shift: 0, frequency: 0.5 },
        { row: 0, fingers: [4], hands: ['L'], shift: 0, frequency: 0.5 },
        { row: 1, fingers: [0, 1], hands: ['L', 'R'], shift: 0 },
        { row: -1, fingers: [0, 1], hands: ['L', 'R'], shift: 0 },
    ],
    [
        { row: 0, fingers: [0, 1, 2], hands: ['L', 'R'], shift: 0, frequency: 0.5 },
        { row: 0, fingers: [4], hands: ['L'], shift: 0, frequency: 0.5 },
        { row: 1, fingers: [0, 1, 2, 3], hands: ['L', 'R'], shift: 0 },
        { row: -1, fingers: [0, 1], hands: ['L', 'R'], shift: 0 },
        { row: -1, fingers: [2, 3, 4], hands: ['L'], shift: 0 },
    ],
];

export const generateLetterArray = (numberOfGroups: number, numberOfLettersPerGroup: number, level: number): string[] => {
    const numberOfLetters = numberOfGroups * numberOfLettersPerGroup

    return generateLetterArrayByPredefinedLevel(level, numberOfLetters);
};

const generateLetterArrayByPredefinedLevel = (level: number, numberOfLetters: number): string[] => {
    const config = levelConfig[level];
    const lettersFrequency: { [key: string]: number } = {};

    for (const c of config) {
        const frequncyNotSplit: { [key: string]: number } = {};

        for (const [key, value] of Object.entries(keyboardLayout)) {
            if (
                c.row === value.row &&
                c.fingers.includes(value.finger) &&
                c.hands.includes(value.hand) &&
                (c.shift === 2 || c.shift === value.shift)
            ) {
                const frequency = c.frequency || 1;
                frequncyNotSplit[key] = frequency;
            }
        }

        const amplifier = 100;

        for (const [key, value] of Object.entries(frequncyNotSplit)) {
            const frequency = value / Object.keys(frequncyNotSplit).length;
            lettersFrequency[key] = Math.floor(frequency * amplifier);
        }
    }

    return generateLetterArrayByFrequency(lettersFrequency, numberOfLetters);
};

const generateLetterArrayByFrequency = (lettersFrequency: { [key: string]: number }, numberOfLetters: number): string[] => {
    const lettersPool: string[] = [];
    for (const [letter, frequency] of Object.entries(lettersFrequency)) {
        const count = Math.floor(frequency * numberOfLetters);
        for (let i = 0; i < count; i++) {
            lettersPool.push(letter);
        }
    }

    const letters: string[] = [];
    let retry = 10;
    while (letters.length < numberOfLetters) {
        const randomIndex = Math.floor(Math.random() * lettersPool.length);
        const randomLetter = lettersPool[randomIndex];

        if (letters.length > 1 && letters[letters.length - 1] === letters[letters.length - 2] && letters[letters.length - 1] === randomLetter) {
            if (retry-- > 0) {
                continue;
            }
        }

        letters.push(randomLetter);
    }
    return letters
}

export default defineComponent({
    name: 'GlobalConfig',
    setup() {
    },
});


</script>