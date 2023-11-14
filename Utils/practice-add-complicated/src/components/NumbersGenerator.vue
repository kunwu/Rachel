<template>
    <div>
        <button @click="calculate" class="btn btn-primary">生成</button>
        <button @click="showAnswer" class="btn btn-info">答案</button>
        <p class="number-list" v-if="outputList.length > 0">{{ outputList.join(' + ') }}</p>
        <p class="actual-sum" v-if="showSum">= {{ actualSum }}</p>
        <b-button v-b-toggle.controlBox variant="primary">配置</b-button>
        <b-collapse id="controlBox" class="mt-2">
            <div class="card">
                <div class="card-body">
                    <div class="form-group">
                        <label>和: </label>
                        <input v-model.number="sum" type="number" class="form-control">
                    </div>
                    <div class="form-group">
                        <label>几位数: </label>
                        <input v-model.number="digitsNumber" type="number" class="form-control">
                    </div>
                    <div class="form-group">
                        <label>几个数: </label>
                        <input v-model.number="integersCount" type="number" class="form-control">
                    </div>
                    <div class="form-group">
                        <label>和扰动: </label>
                        <!-- 和是否扰动，默认 true -->
                        <b-form-checkbox v-model="sumHasRandom">和扰动</b-form-checkbox>
                    </div>
                </div>
            </div>
        </b-collapse>
    </div>
</template>
  

 
  
<script>
function getRandomIntWithDigits(d) {
    let min = Math.pow(10, d - 1);
    let max = Math.pow(10, d) - 1;
    return Math.floor(Math.random() * (max - min + 1) + min);
}

function generateNumbers(sum, digitsNumber, integersCount, sumHasRandom) {
    if (sumHasRandom) {
        sum = sum + Math.floor(Math.random() * 20 - 10);
    }

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

    return {
        numbers: numbers,
        actualSum: sum,
    };
}

export default {
    data() {
        return {
            sum: 1000,
            digitsNumber: 3,
            integersCount: 4,
            sumHasRandom: true,
            actualSum: 1000,
            outputList: [],
            showSum: false,
        }
    },
    methods: {
        calculate() {
            // Assuming generateNumbers is a globally accessible function
            let result = generateNumbers(this.sum, this.digitsNumber, this.integersCount, this.sumHasRandom);
            this.outputList = result.numbers;
            this.actualSum = result.actualSum;
            this.showSum = false;
        },
        showAnswer() {
            this.showSum = true;
        }
    },
}
</script>
  
<style scoped>
.number-list,
.actual-sum {
    font-size: 20px;
}

@media (max-width: 576px) {

    .number-list,
    .actual-sum {
        font-size: 30px;
    }
}
</style>
  