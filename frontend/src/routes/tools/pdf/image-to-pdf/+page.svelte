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
      error = err.message || 'Failed to set images';
    } finally {
      busy = false;
    }
  }
</script>

<svelte:head><title>Images — Atelier Tools</title></svelte:head>

<ToolShell num="03" title="Set images.">
  {#snippet lede()}
    Set photographs and stills onto crisp PDF pages, one per leaf.
    JPEG, PNG, and WebP are welcomed.
  {/snippet}

  <form onsubmit={onSubmit} novalidate>
    <Dropzone
      bind:files
      multiple
      accept="image/jpeg,image/png,image/webp"
      label="Lay your images here"
      sublabel="— in the order they should appear —"
    />

    {#if error}
      <p class="notice notice--err" style="margin-top: 18px;">{error}</p>
    {/if}

    <div class="actions">
      <button class="btn btn--accent" type="submit" disabled={busy || !files.length}>
        {busy ? 'Setting…' : 'Set into PDF'}
        <span aria-hidden="true">&rarr;</span>
      </button>
      {#if lastFilename}
        <span class="lnk lnk--ok">✓ Issued {lastFilename}</span>
      {/if}
    </div>
  </form>

  {#snippet side()}
    <p>
      Each image becomes one page. Order matters &mdash; reorder using the
      arrows on each entry. The aspect of the page follows the image.
    </p>
    <p style="margin-top: 14px;">
      <span class="eyebrow">Accepted</span><br />
      JPEG &middot; PNG &middot; WebP
    </p>
  {/snippet}
</ToolShell>

<style>
  .actions {
    margin-top: 28px;
    display: flex;
    align-items: center;
    gap: 18px;
    flex-wrap: wrap;
  }
  .lnk {
    font-family: var(--mono);
    font-size: 0.74rem;
    letter-spacing: 0.1em;
    color: var(--ink-mute);
  }
  .lnk--ok { color: var(--good); }
</style>
