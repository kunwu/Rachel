/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

function getRandomIntWithDigits(d) {
	let min = Math.pow(10, d - 1);
	let max = Math.pow(10, d) - 1;
	return Math.floor(Math.random() * (max - min + 1) + min);
}

function generateAddQuestions(s, d, n) {
	let numbers = [];
	while (true) {
		numbers = [];
		let currentSum = 0;

		for (let i = 0; i < n - 1; i++) {
			numbers[i] = getRandomIntWithDigits(d);
			currentSum += numbers[i];
			if (currentSum > s) {
				break;
			}
		}

		if ((currentSum + Math.pow(10, d - 1) > s) || (currentSum + Math.pow(10, d) - 1 < s)) {
			continue;
		} else {
			numbers[n - 1] = s - currentSum;
		}

		break;
	}

	// join the numbers with '+' sign, make cast if needed
	numbers = numbers.join(' + ');
	return numbers;
}

export default {
	async fetch(request, env, ctx) {
		// get parameters if presented. if not presented, use default value
		// s default to 1000
		// d default to 3
		// n default to 5
		const params = new URL(request.url).searchParams;
		const s = params.get('s') || 1000;
		const d = params.get('d') || 3;
		const n = params.get('n') || 5;

		const questions = generateAddQuestions(s, d, n);
		return new Response(questions);
	},
};
