<style scoped>
.monospace {
    font-family: 'Courier New', Courier, monospace;
    font-weight: bold;
    font-size: 2em;
}

.calc-container {
    height: 180px;
}

.pad-container {
    border-top: 1px solid #ccc;
    border-bottom: 1px solid #ccc;
}

.pad-row {
    height: 62px;

}

.btn-pad {
    font-size: 2em;
}
</style>

<template>
    <v-app>
        <v-container d-flex justify-center align-center class="calc-container">
            <v-row align="center" justify="center">
                <v-col cols="8">
                    <div class="text-end monospace display-1">
                        <div>{{ longNumber }}</div>
                        <div class="position-relative">
                            <v-icon class="postition-absolute" style="left: -150px;" icon="$close" />
                            {{ shortNumber }}
                        </div>
                        <hr>
                        <div>{{ answer }}</div>
                    </div>
                </v-col>
            </v-row>
        </v-container>
        <v-container fluid class="px-4 py-4 pad-container">
            <v-row class="pad-row align-center">
                <v-col class="px-1 py-0" v-for="n in [1, 2, 3]" :key="n">
                    <v-btn block height="60" class="btn-pad" @click="appendToAnswer(n)">{{ n }}</v-btn>
                </v-col>
            </v-row>
            <v-row class="pad-row align-center">
                <v-col class="px-1 py-0" v-for="n in [4, 5, 6]" :key="n">
                    <v-btn block height="60" class="btn-pad" @click="appendToAnswer(n)">{{ n }}</v-btn>
                </v-col>
            </v-row>
            <v-row class="pad-row align-center">
                <v-col class="px-1 py-0" v-for="n in [7, 8, 9]" :key="n">
                    <v-btn block height="60" class="btn-pad" @click="appendToAnswer(n)">{{ n }}</v-btn>
                </v-col>
            </v-row>
            <v-row class="pad-row align-center">
                <v-col class="px-1 py-0">
                    <v-btn block height="60" class="btn-pad" @click="appendToAnswer(0)">0</v-btn>
                </v-col>
                <v-col class="px-1 py-0">
                    <v-btn block height="60" class="btn-pad" @click="deleteLastDigit">del</v-btn>
                </v-col>
                <v-col class="px-1 py-0">
                    <v-btn block height="60" class="btn-pad" @click="clearAnswer">clr</v-btn>
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
        <!-- 配置区 -->
        <v-expansion-panels model-value="">
            <v-expansion-panel>
                <v-expansion-panel-title expand-icon="$dropdown">配置</v-expansion-panel-title>
                <v-expansion-panel-text>
                    <v-slider v-model="numberOfDigits" :min="2" :max="9" step="1" thumb-label="always"
                        label="第一个乘数的位数"></v-slider>
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
            numberOfDigits: 6,
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
            this.shortNumber = Math.floor(Math.sqrt(100 * Math.random()) * 8 / 10) + 2;
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
    watch: {
        numberOfDigits() {
            this.nextQuestion();
        },
    },
};
</script>

