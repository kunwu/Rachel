<style scoped>
.monospace {
    font-family: 'Courier New', Courier, monospace;
    font-weight: bold;
    font-size: 2em;
}

.calc-container {
    height: 35vh;
}

.pad-row {
    height: 6vh;
}

.pad-container {
    border-top: 1px solid #ccc;
    border-bottom: 1px solid #ccc;
}

.btn-pad {
    font-size: 1.2em;
}
</style>

<template>
    <v-app>
        <div class="d-flex justify-center text-h4 py-5" style="border-bottom: solid 2px black;">心算连加</div>
        <v-container d-flex justify-center align-center class="calc-container">
            <v-row align="center" justify="center" class="mt-6">
                <v-col cols="1">
                    <div class="text-end monospace display-1">
                        <div></div>
                        <div>X</div>
                        <div></div>
                    </div>
                </v-col>
                <v-col cols="8">
                    <div class="text-end monospace display-1">
                        <div>{{ longNumber }}</div>
                        <div>{{ shortNumber }}</div>
                        <hr>
                        <div>&nbsp;{{ answer }}</div>
                    </div>
                </v-col>
            </v-row>
        </v-container>
        <v-container fluid class="px-4 py-4 pad-container">
            <v-row class="pad-row align-center">
                <v-col class="px-1 py-0" v-for="n in [1, 2, 3]" :key="n">
                    <v-btn block class="btn-pad" @click="appendToAnswer(n)">{{ n }}</v-btn>
                </v-col>
            </v-row>
            <v-row class="pad-row align-center">
                <v-col class="px-1 py-0" v-for="n in [4, 5, 6]" :key="n">
                    <v-btn block class="btn-pad" @click="appendToAnswer(n)">{{ n }}</v-btn>
                </v-col>
            </v-row>
            <v-row class="pad-row align-center">
                <v-col class="px-1 py-0" v-for="n in [7, 8, 9]" :key="n">
                    <v-btn block class="btn-pad" @click="appendToAnswer(n)">{{ n }}</v-btn>
                </v-col>
            </v-row>
            <v-row class="pad-row align-center">
                <v-col class="px-1 py-0">
                    <v-btn block class="btn-pad" @click="appendToAnswer(0)">0</v-btn>
                </v-col>
                <v-col class="px-1 py-0">
                    <v-btn block class="btn-pad" @click="deleteLastDigit">del</v-btn>
                </v-col>
                <v-col class="px-1 py-0">
                    <v-btn block class="btn-pad" @click="clearAnswer">clr</v-btn>
                </v-col>
            </v-row>
        </v-container>
        <v-container class="mt-3">
            <v-row>
                <v-col class="px-1 py-1">
                    <v-btn block @click="checkAnswer">对答案</v-btn>
                </v-col>
                <v-col class="px-1 py-1">
                    <v-btn block @click="nextQuestion">再来一题</v-btn>
                </v-col>
            </v-row>
        </v-container>
        <!-- 结果对话框 -->
        <v-dialog v-model="dialog" max-width="300px">
            <v-card>
                <v-card-title class="text-h5">{{ dialogTitle }}</v-card-title>
                <v-card-text v-if="showAnswer">答案：{{ correctAnswer }}</v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn v-if="!correct" color="red darken-1" text @click="showAnswer = true">看答案</v-btn>
                    <v-btn v-if="correct" color="green darken-1" text @click="nextQuestion">再来一题</v-btn>
                    <v-btn color="green darken-1" text @click="closeDialog">Close</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-app>
</template>
  
<script>
export default {
    data() {
        return {
            numberOfDigits: 9,
            longNumber: 987654321,
            shortNumber: 7,
            answer: '',
            // dialog
            dialog: false,
            dialogTitle: '',
            correctAnswer: '',
            showAnswer: false,
            correct: false,
        };
    },
    methods: {
        appendToAnswer(n) {
            this.answer = n + this.answer;
        },
        deleteLastDigit() {
            // remove the most left letters
            this.answer = this.answer.slice(1);
        },
        clearAnswer() {
            this.answer = '';
        },
        checkAnswer() {
            this.correctAnswer = this.longNumber * this.shortNumber;
            if (this.answer == this.correctAnswer) {
                this.dialogTitle = '答对了！';
                this.correct = true;
                this.dialog = true;
            } else {
                this.dialogTitle = '答错了！';
                this.correct = false;
                this.dialog = true;
            }
        },
        nextQuestion() {
            let max = Math.pow(10, this.numberOfDigits) - 1;
            let min = Math.pow(10, this.numberOfDigits - 1);
            this.longNumber = Math.floor(Math.random() * (max - min + 1)) + min;
            // Get a random number between 1 and 10, square it, then map the range from 1-100 to 2-9
            let randomNum = Math.random() * 9.9;
            let squaredNum = Math.pow(randomNum, 2);
            this.shortNumber = 9 - Math.floor(squaredNum / 11);
            console.log('randomNum: ' + randomNum + ', squaredNum: ' + squaredNum + ', shortNumber: ' + this.shortNumber);
            this.answer = '';
            this.closeDialog();
        },
        closeDialog() {
            this.dialog = false;
            this.showAnswer = false;
        },
    },
    mounted() {
        this.nextQuestion();
    },
};
</script>

