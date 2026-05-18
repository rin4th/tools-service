<script>
  import ToolShell from '$lib/components/ToolShell.svelte';
  import Dropzone from '$lib/components/Dropzone.svelte';
  import { apiBlob, downloadBlob } from '$lib/api.js';

  let files = $state([]);
  let startPage = $state(1);
  let endPage = $state(1);
  let busy = $state(false);
  let error = $state('');
  let lastFilename = $state('');

  async function onSubmit(e) {
    e.preventDefault();
    if (busy) return;
    if (files.length !== 1) {
      error = 'Pick exactly one PDF.';
      return;
    }
    if (startPage < 1 || endPage < startPage) {
      error = 'Invalid page range.';
      return;
    }
    error = '';
    busy = true;
    try {
      const fd = new FormData();
      fd.append('file', files[0]);
      fd.append('start_page', String(startPage));
      fd.append('end_page', String(endPage));
      const { blob, filename } = await apiBlob('/api/tools/pdf/split', fd);
      lastFilename = filename;
      downloadBlob(blob, filename);
    } catch (err) {
      error = err.message || 'Failed to split';
    } finally {
      busy = false;
    }
  }
</script>

<svelte:head><title>Split PDF — Voltage</title></svelte:head>

<ToolShell eyebrow="Tools / PDF" title="Split a PDF.">
  {#snippet lede()}
    Extract a precise range from any PDF — pages <em>x</em> through <em>y</em>, no more, no less.
  {/snippet}

  <form onsubmit={onSubmit} novalidate>
    <Dropzone
      bind:files
      accept="application/pdf"
      label="Drop a PDF here"
      sublabel="single file"
    />

    <div class="range">
      <label class="field">
        <span class="field__label">From page</span>
        <input class="field__input" type="number" min="1" bind:value={startPage} required />
      </label>
      <span class="range__sep" aria-hidden="true">→</span>
      <label class="field">
        <span class="field__label">To page</span>
        <input class="field__input" type="number" min="1" bind:value={endPage} required />
      </label>
    </div>

    {#if error}
      <p class="notice notice--err" style="margin-top: 16px;">{error}</p>
    {/if}
    {#if lastFilename}
      <p class="notice notice--ok" style="margin-top: 16px;">
        Generated {lastFilename} — download started automatically.
      </p>
    {/if}

    <div class="actions">
      <button class="btn" type="submit" disabled={busy || !files.length}>
        {#if busy}
          <span class="spinner"></span>
          Extracting
        {:else}
          Extract range
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" /></svg>
        {/if}
      </button>
      {#if files.length}
        <span class="meta">pages {startPage}–{endPage}</span>
      {/if}
    </div>
  </form>

  {#snippet side()}
    <h3 style="font-size: 0.92rem; font-weight: 500; margin-bottom: 10px; color: var(--fg);">How it works</h3>
    <p style="margin: 0 0 12px;">The range is inclusive on both ends. To take a single page, set <em>from</em> equal to <em>to</em>.</p>
    <p class="hint" style="margin: 0;">The original document is never modified.</p>
  {/snippet}
</ToolShell>

<style>
  .range {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: end;
    gap: 16px;
    margin-top: 22px;
    max-width: 460px;
  }
  .range__sep {
    font-family: var(--mono);
    color: var(--fg-mute);
    padding-bottom: 12px;
  }
  .actions {
    margin-top: 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
  }
  .meta {
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--fg-mute);
  }
  .spinner {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    border: 2px solid #0a0a0c40;
    border-top-color: var(--bg);
    animation: spin 700ms linear infinite;
  }
  .hint { color: var(--fg-mute); font-size: 0.86rem; }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>
