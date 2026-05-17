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
    if (files.length < 2) {
      error = 'Pick at least two PDF files to bind.';
      return;
    }
    error = '';
    busy = true;
    try {
      const fd = new FormData();
      for (const f of files) fd.append('files', f);
      const { blob, filename } = await apiBlob('/api/tools/pdf/merge', fd);
      lastFilename = filename;
      downloadBlob(blob, filename);
    } catch (err) {
      error = err.message || 'Failed to merge';
    } finally {
      busy = false;
    }
  }
</script>

<svelte:head><title>Merge — Atelier Tools</title></svelte:head>

<ToolShell num="01" title="Merge.">
  {#snippet lede()}
    Compose two or more PDFs into a single bound volume. Drag to set the order
    &mdash; the first sheet is the cover.
  {/snippet}

  <form onsubmit={onSubmit} novalidate>
    <Dropzone
      bind:files
      multiple
      accept="application/pdf"
      label="Lay your PDFs here"
      sublabel="— at least two, in reading order —"
    />

    {#if error}
      <p class="notice notice--err" style="margin-top: 18px;">{error}</p>
    {/if}

    <div class="actions">
      <button class="btn btn--accent" type="submit" disabled={busy || files.length < 2}>
        {busy ? 'Binding…' : 'Bind into one'}
        <span aria-hidden="true">&rarr;</span>
      </button>
      {#if lastFilename}
        <span class="lnk lnk--ok">✓ Issued {lastFilename}</span>
      {/if}
    </div>
  </form>

  {#snippet side()}
    <p>
      Pages are taken in order, top to bottom. Use the arrows on each entry to
      rearrange. Files leave your browser only briefly, traveling to the
      workshop and returning bound.
    </p>
    <p style="margin-top: 14px;">
      <span class="eyebrow">Constraints</span><br />
      Up to 50 MB per file. Only application/pdf accepted.
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
