<template>
    <div>
        <div class="m-3">
            <transition name="fade" mode="out-in">
                <p class="number-list" v-if="outputList.length > 0" :key="numberListKey">{{ outputList.join(' + ') }}</p>
            </transition>
            <p class="actual-sum">= {{ actualSum }}</p>
        </div>
        <div class="row m-1">
            <button @click="calculate" class="btn btn-primary col-3">出题</button>
            <button @click="showAnswer" class="btn btn-info col-2 ml-2">答案</button>
        </div>
        <hr />
        <div class="row m-1">
            <button @click="isCorrect" type="button" class="btn btn-success col-4">做对啦：{{ countCorrect
            }}</button>
            <button @click="isInCorrect" type="button" class="btn btn-danger col-4 ml-1">失误了：{{ countIncorrect
            }}</button>
            <button @click="resetScore" type="button" class="btn btn-info col-2 ml-3">重来</button>
        </div>
        <hr />
        <div class="m-1"><b-button v-b-toggle.controlBox variant="primary">配置</b-button></div>
        <b-collapse id="controlBox" class="mt-2">
            <div class="card">
                <div class="card-body">
                    <div class="form-group">
                        <label>总和: </label>
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
                        <label>对和扰动: </label>
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
            actualSumHide: 1000,
            actualSum: "?",
            outputList: [],
            showSum: false,
            numberListKey: 0,
            countCorrect: 0,
            countIncorrect: 0,
        }
    },
    methods: {
        calculate() {
            // Assuming generateNumbers is a globally accessible function
            let result = generateNumbers(this.sum, this.digitsNumber, this.integersCount, this.sumHasRandom);
            this.outputList = result.numbers;
            this.actualSumHide = result.actualSum;
            this.actualSum = "?";
            this.showSum = false;
            this.numberListKey = this.numberListKey + 1;
        },
        showAnswer() {
            this.actualSum = this.actualSumHide;
        },
        isCorrect() {
            this.countCorrect++;
        },
        isInCorrect() {
            this.countIncorrect++;
        },
        resetScore() {
            this.countCorrect = 0;
            this.countIncorrect = 0;
        },
    },
    mounted() {
        this.calculate();
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

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to

/* .fade-leave-active below version 2.1.8 */
    {
    opacity: 0;
}
</style>
  