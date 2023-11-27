<template>
    <div class="d-flex justify-center text-h4 py-5">心算连加</div>
    <div>
        <v-carousel :continuous="false" :model-value="0" :show-arrows="false" :height="100" :hide-delimiters="true"
            :progress="true">
            <v-carousel-item v-for="(item, i) in numbersToAdd" :key="i">
                <div class="d-flex fill-height justify-center align-center text-h4">{{ item }}</div>
            </v-carousel-item>
        </v-carousel>
    </div>
    <div>
        <v-text-field v-model="inputAnswer" prefix="和 =" placeholder="请输入数字之和" type="number"
            hide-details="true"></v-text-field>
    </div>
    <div class="mx-2">
        <div class="my-1">
            <v-btn @click="checkAnswer">对答案</v-btn>
            <span class="ml-2 font-weight-thin">({{ digitsSummary }})</span>
        </div>
        <div class="my-1">
            <v-btn @click="generateNumbers">再来一题</v-btn>
        </div>
    </div>
    <v-expansion-panels>
        <v-expansion-panel>
            <v-expansion-panel-title expand-icon="mdi-menu-down">配置</v-expansion-panel-title>
            <v-expansion-panel-text>
                <v-form>
                    <v-text-field v-model="countOfNumbers" label="加数个数" type="number"
                        :rules="[v => (v >= 2 && v <= 20) || 'Number must be between 2 and 20']"></v-text-field>
                    <v-text-field v-model="numberOfDigits" label="加数位数" type="number"
                        :rules="[v => (v >= 2 && v <= 6) || 'Number must be between 2 and 6']"></v-text-field>
                    <v-select v-model="levelOfDifficulty" :items="[0, 1, 2]" label="难度"></v-select>
                </v-form>
            </v-expansion-panel-text>
        </v-expansion-panel>
    </v-expansion-panels>
    <!-- 结果对话框 -->
    <v-dialog v-model="dialog" max-width="300px">
        <v-card>
            <v-card-title class="text-h5">{{ dialogTitle }}</v-card-title>
            <v-card-text v-if="showAnswer">答案：{{ correctAnswer }}</v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn v-if="!correct" color="red darken-1" text @click="showAnswer = true">看答案</v-btn>
                <v-btn color="green darken-1" text @click="closeDialog">Close</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
  
<script>

export default {
    name: 'AddNumbers',
    components: {
    },
    data() {
        return {
            numbersToAdd: [],
            inputAnswer: null,
            // dialog
            dialog: false,
            dialogTitle: '',
            correct: false,
            correctAnswer: null,
            showAnswer: false,
            // configuration
            countOfNumbers: 4,
            numberOfDigits: 3,
            levelOfDifficulty: 2,
        }
    },
    methods: {
        generateNumbers() {
            let countOfNumbers = this.countOfNumbers;
            let numberOfDigits = this.numberOfDigits;
            let levelOfDifficulty = this.levelOfDifficulty;

            let numbers = [];
            let max = Math.pow(10, numberOfDigits) - 1;
            let min = Math.pow(10, numberOfDigits - 1);
            let countTry = 100;
            do {
                numbers = [];
                for (let i = 0; i < countOfNumbers; i++) {
                    let number = Math.floor(Math.random() * (max - min + 1)) + min;
                    numbers.push(number);
                }
                console.log(numbers);
                if (countTry-- < 0) {
                    alert('无法生成符合条件的题目');
                    break;
                }
            } while (!this.meetsDifficulty(numbers, levelOfDifficulty));
            console.log(numbers.reduce((a, b) => a + b, 0));

            this.numbersToAdd = numbers;
            this.inputAnswer = null;
            this.dialog = false;
        },
        meetsDifficulty(numbers, levelOfDifficulty) {
            let simpleCarryCounts = [];
            let doubleCarryCounts = [];

            let sum = numbers[0];

            for (let i = 1; i < numbers.length; i++) {
                let carry = 0;
                let b = numbers[i];
                let digitsSum = sum.toString().split('').reverse();
                let digitsB = b.toString().split('').reverse();
                let maxLen = Math.max(digitsSum.length, digitsB.length);
                let currentSum = 0;
                simpleCarryCounts.push(0);
                doubleCarryCounts.push(0);
                for (let j = 0; j < maxLen; j++) {
                    let digitSum = digitsSum[j] ? parseInt(digitsSum[j]) : 0;
                    let digitB = digitsB[j] ? parseInt(digitsB[j]) : 0;
                    if (carry > 0) {
                        simpleCarryCounts[i - 1] = simpleCarryCounts[i - 1] + 1;
                    }
                    if (carry > 0 && digitSum + digitB + carry >= 10) {
                        doubleCarryCounts[i - 1] = doubleCarryCounts[i - 1] + 1;
                    }
                    // console.log('digitsSum=', digitsSum, 'digitsB=', digitsB, 'digitSum=', digitSum, 'digitB=', digitB, 'carry=', carry);
                    // console.log('simpleCarryCounts=', simpleCarryCounts, 'doubleCarryCounts=', doubleCarryCounts);
                    currentSum = digitSum + digitB + carry;
                    carry = Math.floor(currentSum / 10);
                }
                if (carry > 0) {
                    simpleCarryCounts[i - 1] = simpleCarryCounts[i - 1] + 1;
                }
                sum = sum + b;
            }

            console.log('按轮单纯进位个数：', simpleCarryCounts);
            console.log('按轮二次进位个数', doubleCarryCounts);

            let level = 0;
            if (simpleCarryCounts.reduce((a, b) => a + b, 0) > 0) {
                level = 1;
            }
            if (doubleCarryCounts.reduce((a, b) => a + b, 0) > 0) {
                level = 2;
            }

            return level == levelOfDifficulty;
        },
        checkAnswer() {
            let answer = this.numbersToAdd.reduce((a, b) => a + b, 0);
            this.correctAnswer = answer;
            if (answer == this.inputAnswer) {
                this.dialogTitle = '答对了';
                this.correct = true;
            } else {
                if (this.inputAnswer == '' || this.inputAnswer == null) {
                    this.dialogTitle = '没回答';
                } else {
                    if (answer > this.inputAnswer) {
                        this.dialogTitle = '答小了';
                    } else if (answer < this.inputAnswer) {
                        this.dialogTitle = '答大了';
                    } else {
                        this.dialogTitle = '答错了';
                    }
                }
                this.correct = false;
            }
            this.dialog = true;
        },
        closeDialog() {
            this.dialog = false;
            this.showAnswer = false;
        },
    },
    computed: {
        digitsSummary() {
            let sum = this.numbersToAdd.reduce((acc, num) => {
                let digits = num.toString().split('').map(Number);
                return acc + digits.reduce((a, b) => a + b, 0);
            }, 0);

            while (sum > 9) {
                let digits = sum.toString().split('').map(Number);
                sum = digits.reduce((a, b) => a + b, 0);
            }

            return sum;
        }
    },
    mounted() {
        this.generateNumbers();
    }
}
</script>