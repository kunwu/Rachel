<template>
    <div>
        <label>和: <input v-model.number="sum" type="number"></label>
        <label>几位数: <input v-model.number="digitsNumber" type="number"></label>
        <label>几个数: <input v-model.number="integersCount" type="number"></label>
        <button @click="calculate">生成</button>
        <ul>
            <li v-for="(number, index) in outputList" :key="index">{{ number }}</li>
        </ul>
    </div>
</template>
  
<script>
function getRandomIntWithDigits(d) {
    let min = Math.pow(10, d - 1);
    let max = Math.pow(10, d) - 1;
    return Math.floor(Math.random() * (max - min + 1) + min);
}

function generateNumbers(sum, digitsNumber, integersCount) {
    if (sum < Math.pow(10, digitsNumber - 1) * integersCount || sum > Math.pow(10, digitsNumber) * integersCount) {
        return [];
    }

    let numbers = [];
    let found = false;

    while (!found) {
        numbers = [];
        let currentSum = 0;

        for (let i = 0; i < integersCount - 1; i++) {
            numbers[i] = getRandomIntWithDigits(digitsNumber);
            currentSum += numbers[i];
            if (currentSum > sum) {
                break;
            }
        }

        if ((currentSum + Math.pow(10, digitsNumber - 1) > sum) || (currentSum + Math.pow(10, digitsNumber) - 1 < sum)) {
            continue;
        } else {
            numbers[integersCount - 1] = sum - currentSum;
            found = true;
        }
    }

    return numbers;
}

export default {
    data() {
        return {
            sum: 1000,
            digitsNumber: 3,
            integersCount: 4,
            outputList: [],
        }
    },
    methods: {
        calculate() {
            // Assuming generateNumbers is a globally accessible function
            this.outputList = generateNumbers(this.sum, this.digitsNumber, this.integersCount);
        },
    },
}
</script>
  
<style scoped>
/* Add your CSS styles if needed */
</style>
  