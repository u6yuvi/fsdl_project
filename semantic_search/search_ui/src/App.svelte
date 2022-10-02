<script>
  import "carbon-components-svelte/css/all.css";
  import {
    Theme,
    RadioButtonGroup,
    RadioButton,
    Select,
    SelectItem,
  } from "carbon-components-svelte";
  import {
    TextInput,
    Header,
    Content,
    Tooltip,
  } from "carbon-components-svelte";
  import { ImageLoader, Button, Popover } from "carbon-components-svelte";
  import ImageSearch from "carbon-icons-svelte/lib/ImageSearch.svelte";
  import { Grid, Row, Column } from "carbon-components-svelte";
  import { writable } from "svelte/store";
  import { onMount } from "svelte";
  import Gallery from "svelte-brick-gallery";

  let theme = "g80"; // "white" | "g10" | "g80" | "g90" | "g100"

  $: document.documentElement.setAttribute("theme", theme);
  let searchText = "";
  let imageLoader;
  let error;
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
    return resp.predictions;
  };
  let promise;
  const clickGetImage = () => {
    promise = fetchImage();
  };
</script>

<Content>
  <Grid padding>
    <Theme bind:theme />
    <Header>
      <RadioButtonGroup legendText="Choose Theme" bind:selected={theme}>
        {#each ["white", "g10", "g80", "g90", "g100"] as value}
          <RadioButton labelText={value} {value} />
        {/each}
      </RadioButtonGroup>
    </Header>
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
        <Gallery {images}>
          <div
            slot="image"
            let:index
            let:style
            let:displayWidth
            let:displayHeight
            style="height:100%; position:relative;"
          >
            <img
              class="img"
              src={images[index].src}
              {style}
              alt={images[index].score}
            />
            <span
              style="position:absolute; z-index:2; top:0; left:0; padding:2px;
              opacity: 70%; border-radius: 5px; background-color:white;
              color:black;"
              >{images[index].name}</span
            >
            <span
              style="position:absolute; z-index:2; bottom:0; right:0;
              padding:2px; opacity: 70%; border-radius: 5px;
              background-color:white; color:black;"
              >Score: {images[index].alt}</span
            >
          </div>
        </Gallery>
      {:catch error}
        <p>An error occurred!</p>
      {/await}
    {/if}
  </Grid>
</Content>

<style>
  .bar {
    display: flex;
    justify-content: space-between;
    margin-bottom: var(--cds-layout-02);
    border-bottom: 1px solid var(--cds-ui-03);
  }

  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
  :global(img) {
    opacity: 0.9;
    transition: all 0.2s;
  }
  :global(img):hover {
    opacity: 1;
    transform: scale(1.04);
  }
</style>
