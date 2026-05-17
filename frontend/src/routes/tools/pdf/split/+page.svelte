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

<svelte:head><title>Split — Atelier Tools</title></svelte:head>

<ToolShell num="02" title="Split.">
  {#snippet lede()}
    Excerpt a precise range from a PDF &mdash; from page <em>x</em> to page
    <em>y</em>, no more, no less. The remainder stays untouched.
  {/snippet}

  <form onsubmit={onSubmit} novalidate>
    <Dropzone
      bind:files
      accept="application/pdf"
      label="Place the document here"
      sublabel="— a single PDF —"
    />

    <fieldset class="range">
      <legend class="range__legend">
        <span class="section-num">No. 02 &middot; Page range</span>
      </legend>

      <div class="range__row">
        <label class="field">
          <span class="field__label">From page</span>
          <input
            class="field__input"
            type="number"
            min="1"
            bind:value={startPage}
            required
          />
        </label>

        <span class="range__dash" aria-hidden="true">&mdash;</span>

        <label class="field">
          <span class="field__label">Through page</span>
          <input
            class="field__input"
            type="number"
            min="1"
            bind:value={endPage}
            required
          />
        </label>
      </div>
    </fieldset>

    {#if error}
      <p class="notice notice--err" style="margin-top: 18px;">{error}</p>
    {/if}

    <div class="actions">
      <button class="btn btn--accent" type="submit" disabled={busy || !files.length}>
        {busy ? 'Excerpting…' : 'Excerpt range'}
        <span aria-hidden="true">&rarr;</span>
      </button>
      {#if lastFilename}
        <span class="lnk lnk--ok">✓ Issued {lastFilename}</span>
      {/if}
    </div>
  </form>

  {#snippet side()}
    <p>
      The range is inclusive on both ends. To take only one page, set
      <em>x</em> equal to <em>y</em>. The original document is never altered.
    </p>
  {/snippet}
</ToolShell>

<style>
  .range {
    margin: 28px 0 0;
    padding: 22px 0 0;
    border: 0;
    border-top: 1px solid var(--rule-strong);
  }

  .range__legend { padding: 0; }

  .range__row {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: end;
    gap: 18px;
    max-width: 520px;
    margin-top: 18px;
  }

  .range__dash {
    font-family: var(--serif);
    font-size: 1.6rem;
    color: var(--ink-mute);
    padding-bottom: 8px;
  }

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
