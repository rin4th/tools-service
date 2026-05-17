<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { token } from '$lib/auth.js';

  let { num, title, lede, children, side } = $props();

  onMount(() => {
    if (!$token) goto('/login');
  });
</script>

<article class="tool">
  <header class="tool__head">
    <p class="section-num rise rise-1">§ {num} &mdash; A Tool</p>
    <h1 class="tool__title rise rise-2">{title}</h1>
    {#if lede}
      <p class="tool__lede rise rise-3">{@render lede()}</p>
    {/if}
    <div class="rule rise rise-3" style="margin-top: 24px;"></div>
  </header>

  <div class="tool__body">
    <section class="tool__work rise rise-4">
      {@render children()}
    </section>

    {#if side}
      <aside class="tool__side rise rise-5">
        {@render side()}
      </aside>
    {/if}
  </div>
</article>

<style>
  .tool { display: grid; gap: 32px; }

  .tool__head { max-width: 60ch; }

  .tool__title {
    font-family: var(--serif);
    font-size: clamp(2.4rem, 5vw, 3.6rem);
    margin: 14px 0 18px;
    line-height: 1.05;
    letter-spacing: -0.02em;
  }

  .tool__lede {
    font-family: var(--serif);
    font-style: italic;
    color: var(--ink-2);
    font-size: 1.1rem;
    line-height: 1.5;
    max-width: 56ch;
  }

  .tool__body {
    display: grid;
    grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr);
    gap: clamp(24px, 4vw, 56px);
    align-items: start;
  }

  .tool__side {
    border-left: 1px solid var(--rule-strong);
    padding-left: clamp(20px, 3vw, 40px);
    color: var(--ink-mute);
    font-family: var(--serif);
    font-style: italic;
    line-height: 1.5;
  }

  @media (max-width: 900px) {
    .tool__body { grid-template-columns: 1fr; }
    .tool__side { border-left: 0; padding-left: 0; border-top: 1px solid var(--rule-strong); padding-top: 24px; }
  }
</style>
