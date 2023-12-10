<script lang="ts">
export type LevelConfig = {
    row: number,
    fingers: number[],
    hands: string[],
    shift: number,
    frequency?: number
}[][];

export const levelConfig: LevelConfig = [
    [{ row: 0, fingers: [1], hands: ['L', 'R'], shift: 0 }],
    [
        { row: 0, fingers: [1], hands: ['L', 'R'], shift: 0 },
        { row: 0, fingers: [0], hands: ['L', 'R'], shift: 0, frequency: 0.5 }
    ],
    [
        { row: 0, fingers: [0, 1, 2, 3, 4], hands: ['L'], shift: 0 },
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
</script>