<script lang="ts">
  export let trackList: { url: string; name: string, id: string, artist: string }[] = [];
</script>

<div class="track-list">
    <h2>Track List</h2>
    <div class="grid">
        {#each trackList as track}
            <!--			<li>Artist Name: { track.name }</li>-->
            <!--			<li>Album: <a href="{track.url}" target="_blank">{track.url}</a></li>-->
            <!--			<li>id: {track.id}</li>-->
            <div>
<!--            {track.id}-->
                <iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/{track.id}?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
            </div>
        {/each}
    </div>
</div>

<style>
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
    }
</style>
