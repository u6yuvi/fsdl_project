<script>
  import "carbon-components-svelte/css/all.css";
  import { Theme } from "carbon-components-svelte";
  import { TextInput, Header, Content } from "carbon-components-svelte";
  import { Button } from "carbon-components-svelte";
  import ImageSearch from "carbon-icons-svelte/lib/ImageSearch.svelte";
  import { Grid, Row, Column } from "carbon-components-svelte";
  import { Modal } from "carbon-components-svelte";
  import StarRating from "./StarRating.svelte";

  let openDetails = false;
  let imgIndex = 0;

  let theme = "g80"; // "white" | "g10" | "g80" | "g90" | "g100"

  $: document.documentElement.setAttribute("theme", theme);
  let searchText = "";
  const fetchImage = async () => {
    if (!searchText) {
      return [];
    }
    const response = await fetch("http://localhost:5000/v1/predictions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        accept: "*/*",
      },
      body: JSON.stringify(searchText),
    });
    const resp = await response.json();
    return resp.predictions.map((p) => ({
      ...p,
      metadata: JSON.parse(p.metadata),
    }));
  };
  let promise;
  const clickGetImage = () => {
    promise = fetchImage();
  };
</script>

<Content>
  <Grid padding>
    <Theme
      render="toggle"
      toggle={{
        themes: ["g10", "g80"],
        labelA: "Enable dark mode",
        labelB: "Enable dark mode",
        hideLabel: true,
        size: "sm",
      }}
    />
    <Row>
      <h1>Enter text to show matching images</h1>
    </Row>
    <form on:submit|preventDefault={clickGetImage}>
      <Row>
        <TextInput bind:value={searchText} placeholder="Enter text" autofocus />
        <Button
          icon={ImageSearch}
          iconDescription="Click to get images"
          on:click={clickGetImage}
        />
      </Row>
    </form>
    {#if promise != null}
      {#await promise}
        <p>...waiting</p>
      {:then images}
        <Grid padding>
          <Row>
            {#each images as image, index}
              <Column sm={8} md={4} lg={8}>
                <img
                  src={image.src}
                  alt={image.metadata.item_name}
                  on:click={() => {
                    openDetails = true;
                    imgIndex = index;
                  }}
                />
                <StarRating key={index} searchText={searchText} imgName={image.name} score={image.score}/>
              </Column>
            {/each}
          </Row>
        </Grid>
        {#if images[imgIndex]}
          <Modal
            passiveModal
            bind:open={openDetails}
            modalHeading="Details"
            on:close={() => (openDetails = false)}
            on:open
            on:submit={() => (openDetails = false)}
          >
            {#each Object.entries(images[imgIndex].metadata) as [key, values]}
              <p style="align:center; color:lightgreen">
                <b>{key.toUpperCase()}</b>
              </p>
              {#if Array.isArray(values)}
                {#each values as val}
                  <p>{val}</p>
                {/each}
              {:else}
                <p>{values}</p>
              {/if}
            {/each}
          </Modal>
        {/if}
      {:catch error}
        <p>An error occurred!</p>
        <p>{error}</p>
      {/await}
    {/if}
  </Grid>
</Content>

<style>
  :global(img) {
    opacity: 0.9;
    transition: all 0.2s;
  }
  :global(img):hover {
    opacity: 1;
    transform: scale(1.04);
  }
</style>
