<script>
  import ToolShell from '$lib/components/ToolShell.svelte';
  import Dropzone from '$lib/components/Dropzone.svelte';
  import { apiBlob, downloadBlob } from '$lib/api.js';

  let files = $state([]);
  let busy = $state(false);
  let error = $state('');
  let lastFilename = $state('');

  async function onSubmit(e) {
    e.preventDefault();
    if (busy) return;
    if (!files.length) {
      error = 'Pick at least one image.';
      return;
    }
    error = '';
    busy = true;
    try {
      const fd = new FormData();
      for (const f of files) fd.append('files', f);
      const { blob, filename } = await apiBlob('/api/tools/pdf/image-to-pdf', fd);
      lastFilename = filename;
      downloadBlob(blob, filename);
    } catch (err) {
      error = err.message || 'Failed to convert';
    } finally {
      busy = false;
    }
  }
</script>

<svelte:head><title>Images → PDF — Voltage</title></svelte:head>

<ToolShell eyebrow="Tools / PDF" title="Images → PDF.">
  {#snippet lede()}
    Stitch JPEGs, PNGs, or WebPs into a single PDF — one image per page, in the order you set.
  {/snippet}

  <form onsubmit={onSubmit} novalidate>
    <Dropzone
      bind:files
      multiple
      accept="image/jpeg,image/png,image/webp"
      label="Drop image files here"
      sublabel="JPEG · PNG · WebP"
    />

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
          Converting
        {:else}
          Convert {files.length} {files.length === 1 ? 'image' : 'images'}
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" /></svg>
        {/if}
      </button>
      <span class="meta">{files.length} {files.length === 1 ? 'image' : 'images'} ready</span>
    </div>
  </form>

  {#snippet side()}
    <h3 style="font-size: 0.92rem; font-weight: 500; margin-bottom: 10px; color: var(--fg);">How it works</h3>
    <p style="margin: 0 0 12px;">Each image becomes one page. Reorder using the arrows on each entry. The page aspect follows the image.</p>
    <p class="hint" style="margin: 0;"><strong style="color: var(--fg);">Accepted</strong> — JPEG, PNG, WebP up to 99 MB each.</p>
  {/snippet}
</ToolShell>

<style>
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
