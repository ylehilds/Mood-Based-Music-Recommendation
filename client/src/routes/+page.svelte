<script lang="ts">
	import TrackList from './TrackList.svelte';
	import moodify from '$lib/images/moodify.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';

	let trackList: { url: string; name: string, id: string, artist: string }[] = [];
	let searchQuery: string = '';

	async function fetchTrackList(query: string) {
		console.log(`Fetching track list for query: ${query}`);
		const response = await fetch('http://localhost:3000/spotify?searchQuery=' + searchQuery);
		const data = await response.json();
		trackList = data;
		console.log(trackList);
	}
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<h1>
		<span class="welcome">
			<picture>
				<source srcset={moodify} type="image/webp" />
				<img src={welcome_fallback} alt="Welcome" />
			</picture>
		</span>
		<br />
		Describe your mood and get a Spotify song recommendation
		<br />
		<br />
		<input type="text" bind:value={searchQuery}> <button on:click={() => fetchTrackList(searchQuery)}>Search</button>
	</h1>

	<TrackList { trackList }/>
</section>

<style>

	.welcome {
		display: block;
		position: relative;
		width: 100%;
		height: 0;
		padding: 0 0 calc(100% * 495 / 2048) 0;
	}

	.welcome img {
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		display: block;
	}
</style>
