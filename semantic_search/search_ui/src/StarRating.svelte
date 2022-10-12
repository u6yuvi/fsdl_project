<!-- Inspired from: https://svelte.dev/repl/b6a9c67f21944c1c8ad2378a07c3cd48?version=3.32.3 -->
<!-- Made with svelte carbon components -->
<script>
	import Star from "carbon-icons-svelte/lib/Star.svelte";
	export let key = 1;
	import { Button } from "carbon-components-svelte";
	import StarFilled from "carbon-icons-svelte/lib/StarFilled.svelte";
	import { Modal, Form, TextArea } from "carbon-components-svelte";

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
		if (!container?.contains(event.target)) {
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
			collectFeedback = false;
			return;
		}
		rating = id;
		collectFeedback = true;
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
		if (rating !== null) {
			sendFeedback({ star: rating, text: value, imgIndex: key });
		}
		// then reset view
		setTimeout(() => {
			collectFeedback = false;
			feedbackCompleted = false;
		}, 500);
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

<div>
	<span id={"feedbackContiner" + key}>
		<span class="starContainer">
			{#each stars as star (star.id)}
				<Button
					kind="ghost"
					id={star.id.toString()}
					on:mouseover={handleHover(star.id)}
					on:mouseleave={() => (hoverRating = null)}
					on:click={handleRate(star.id)}
				>
					{#if hoverRating ? hoverRating >= star.id : rating >= star.id}
						<StarFilled size={24} />
					{:else}
						<Star size={24} />
					{/if}
				</Button>
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
		{#if collectFeedback}
			<Modal
				bind:open={collectFeedback}
				passiveModal
				modalHeading="Feedback"
				on:open
				on:close={() => {
					rating = null;
					collectFeedback = false;
				}}
			>
				<Form
					on:submit={(e) => {
						e.preventDefault();
						handleCollectFeedback(e);
					}}
				>
					<p style="align-content:center;">
						You've selected {rating ? rating : "no"} star{rating ===
						1
							? ""
							: "s"}, Please tell us why you gave us this rating
					</p>
					<TextArea />
					<Button kind="tertiary" size="small" type="submit">
						Send Feedback
					</Button>
					<Button
						kind="tertiary"
						size="small"
						type="cancel"
						on:click={() => {
							collectFeedback = false;
							rating = null;
						}}
					>
						No Thanks
					</Button>
				</Form>
			</Modal>
		{/if}
	</span>
</div>

<style>
	.starContainer {
		display: inline-block;
		transition: background 0.2s ease-out;
		border-radius: 8px;
		padding: 4px 6px 0;
	}
	.secondaryAction {
		margin: 8px;
		font-size: 12px;
		display: inline-block;
	}
	:global(button) {
		cursor: pointer;
	}
</style>
