<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { token } from '$lib/auth.js';

  let { eyebrow, title, lede, children, side } = $props();

  onMount(() => {
    if (!$token) goto('/login');
  });
</script>

<article class="tool">
  <header class="tool__head">
    <p class="eyebrow rise rise-1">{eyebrow}</p>
    <h1 class="display tool__title rise rise-2">{title}</h1>
    {#if lede}
      <p class="tool__lede rise rise-3">{@render lede()}</p>
    {/if}
  </header>

  <div class="tool__body">
    <section class="tool__work rise rise-3">
      {@render children()}
    </section>

    {#if side}
      <aside class="tool__side rise rise-4">
        {@render side()}
      </aside>
    {/if}
  </div>
</article>

<style>
  .tool { display: grid; gap: 32px; }

  .tool__head { max-width: 60ch; }

  .tool__title {
    font-size: clamp(2.4rem, 5vw, 3.6rem);
    margin: 14px 0 16px;
  }

  .tool__lede {
    color: var(--fg-2);
    font-size: 1.05rem;
    line-height: 1.55;
    max-width: 56ch;
    margin: 0;
  }

  .tool__body {
    display: grid;
    grid-template-columns: minmax(0, 1.7fr) minmax(0, 1fr);
    gap: 32px;
    align-items: start;
  }

  .tool__side {
    padding: 22px;
    background: var(--surface);
    border: 1px solid var(--line-2);
    border-radius: var(--r-2);
    color: var(--fg-2);
    font-size: 0.92rem;
    line-height: 1.55;
  }

  @media (max-width: 960px) {
    .tool__body { grid-template-columns: 1fr; }
  }
</style>
