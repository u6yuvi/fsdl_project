<!-- Source: https://svelte.dev/repl/b6a9c67f21944c1c8ad2378a07c3cd48?version=3.32.3 -->
<script>
	import { fade, slide } from "svelte/transition";
	import { quintOut } from "svelte/easing";
	import Star from "./Star.svelte";
	import { LogicalPartition } from "carbon-icons-svelte";
	// import Star from "carbon-icons-svelte/lib/Star.svelte";
	export let key = 1;

	// User rating states
	let rating = null;
	let hoverRating = null;

	// form interaction states
	let collectFeedback = false;
	let feedbackCompleted = false;

	// "$:" triggers when something in the line changes
	// When these variables reach true/false, they trigger these functions
	$: collectFeedback && addWatchListeners();
	$: !collectFeedback && feedbackFormClosed();

	function feedbackFormClosed() {
		feedbackCompleted = false;
		removeWatchListeners();
	}

	function addWatchListeners() {
		document.addEventListener("keydown", userDismissFeedback);
		document.addEventListener("click", userClickedOutsideOfFeedback);
	}
	function removeWatchListeners() {
		document.removeEventListener("keydown", userDismissFeedback);
		document.removeEventListener("click", userClickedOutsideOfFeedback);
	}
	function userClickedOutsideOfFeedback(event) {
		const container = document.getElementById("feedbackContiner" + key);
		if (!container.contains(event.target)) {
			collectFeedback = false;
		}
	}
	function userDismissFeedback(event) {
		switch (event.key) {
			case "Escape":
				collectFeedback = false;
				break;
			default:
				return;
		}
	}

	// using curried function to initialize hover with id
	const handleHover = (id) => () => {
		hoverRating = id;
	};
	const handleRate = (id) => (event) => {
		if (
			collectFeedback &&
			rating &&
			rating.toString() === event.srcElement.dataset.starid
		) {
			console.log("Not handling");
			collectFeedback = false;
			return;
		}
		rating = id;
		collectFeedback = true;
		console.log("feedback rating:", rating);
	};

	let stars = [
		{ id: 1, title: "One Star" },
		{ id: 2, title: "Two Stars" },
		{ id: 3, title: "Three Stars" },
		{ id: 4, title: "Four Stars" },
		{ id: 5, title: "Five Stars" },
	];

	function handleCollectFeedback(e) {
		const textarea = e.srcElement.querySelector("textarea");
		const value = textarea.value;

		// let them know we recieved it
		feedbackCompleted = true;
		console.log("text feedback:", value);
		sendFeedback({ star: rating, text: value })
		// then reset view
		setTimeout(() => {
			collectFeedback = false;
			feedbackCompleted = false;
		}, 1250);
	}

	const sendFeedback = async (rate_obj) => {
		const response = await fetch("http://localhost:5000/v1/feedback", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				accept: "*/*",
			},
			body: JSON.stringify(rate_obj),
		});
		const resp = await response.json();
		return resp.status;
	};

	function handleLinkFeedback() {
		collectFeedback = true;
	}
</script>

<div class="feedback">
	<span
		id={"feedbackContiner" + key}
		class="feedbackContainer"
		class:feedbackContainerDisabled={feedbackCompleted}
	>
		<span class="starContainer">
			{#each stars as star (star.id)}
				<Star
					filled={hoverRating
						? hoverRating >= star.id
						: rating >= star.id}
					starId={star.id}
					on:mouseover={handleHover(star.id)}
					on:mouseleave={() => (hoverRating = null)}
					on:click={handleRate(star.id)}
				/>
			{/each}
		</span>
		<br />
		<p class="secondaryAction">
			{#if rating !== null}
				Thank you for your feedback - <a
					href="#!"
					on:click={() => (rating = null)}
					on:click={(event) =>
						window.confirm(
							"Your feedback is very valuable. Are you sure you want to reset?"
						)
							? event.preventDefault()
							: null}>reset</a
				>
			{:else}
				<a href="#!" on:click={handleLinkFeedback}>Give Feedback</a>
			{/if}
		</p>
		<br />
		<p>
			CollectFeedback {collectFeedback} FeedBack Completed: {feedbackCompleted}
		</p>
		{#if collectFeedback}
			<div class="collectFeedbackContainer" transition:fade>
				{#if feedbackCompleted}
					<p>Thank you!</p>
				{:else}
					<form
						on:submit|preventDefault={handleCollectFeedback}
						transition:slide={{ duration: 450 }}
					>
						<p>
							You've selected {rating ? rating : "no"} star{rating ===
							1
								? ""
								: "s"},
							<br />
							please tell us why you gave us this rating
						</p>
						<textarea />
						<button> Send Feedback </button>
						<button
							on:click={() => (collectFeedback = false)}
							type="button"
							class="cancel"
						>
							No Thanks
						</button>
					</form>
				{/if}
			</div>
		{/if}
	</span>
</div>

<style>
	.feedback {
		position: relative;
	}
	.collectFeedbackContainer {
		width: 300px;
		position: absolute;
		top: 44px;
		left: 0;
		background: #fff;
		border: 1px solid #666;
		padding: 8px;
		transition: transform 0.2s ease-out;
	}
	.collectFeedbackContainer textarea {
		display: block;
		width: 100%;
		height: 120px;
		resize: none;
	}
	.cancel {
		background: none;
		text-decoration: underline;
		border: none;
	}
	.starContainer {
		display: inline-block;
		transition: background 0.2s ease-out;
		border-radius: 8px;
		padding: 4px 6px 0;
	}
	.feedbackContainer:hover .starContainer {
		background: #efefef;
	}
	.secondaryAction {
		margin: 8px;
		font-size: 12px;
		display: inline-block;
	}
	.feedbackContainerDisabled {
		pointer-events: none;
	}
	:global(button) {
		cursor: pointer;
	}
</style>
