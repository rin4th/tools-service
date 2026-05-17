<script>
  import { onDestroy } from 'svelte';

  let {
    multiple = false,
    accept = '',
    files = $bindable([]),
    label = 'Drop files here',
    sublabel = '— or click to browse —'
  } = $props();

  let dragOver = $state(false);
  let inputEl;

  function onDrop(e) {
    e.preventDefault();
    dragOver = false;
    const list = Array.from(e.dataTransfer.files || []);
    if (!list.length) return;
    files = multiple ? [...files, ...list] : list.slice(0, 1);
  }

  function onPick(e) {
    const list = Array.from(e.target.files || []);
    if (!list.length) return;
    files = multiple ? [...files, ...list] : list.slice(0, 1);
    e.target.value = '';
  }

  function remove(idx) {
    files = files.filter((_, i) => i !== idx);
  }

  function move(idx, dir) {
    const target = idx + dir;
    if (target < 0 || target >= files.length) return;
    const next = files.slice();
    [next[idx], next[target]] = [next[target], next[idx]];
    files = next;
  }

  function fmtSize(n) {
    if (n < 1024) return `${n} B`;
    if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
    return `${(n / (1024 * 1024)).toFixed(1)} MB`;
  }
</script>

<div class="drop" class:drop--active={dragOver}
  ondragover={(e) => { e.preventDefault(); dragOver = true; }}
  ondragleave={() => { dragOver = false; }}
  ondrop={onDrop}
  role="region"
  aria-label="File upload"
>
  <input
    bind:this={inputEl}
    type="file"
    {multiple}
    {accept}
    onchange={onPick}
    hidden
  />

  <button type="button" class="drop__inner" onclick={() => inputEl.click()}>
    <span class="drop__corner drop__corner--tl" aria-hidden="true"></span>
    <span class="drop__corner drop__corner--tr" aria-hidden="true"></span>
    <span class="drop__corner drop__corner--bl" aria-hidden="true"></span>
    <span class="drop__corner drop__corner--br" aria-hidden="true"></span>

    <span class="drop__mark" aria-hidden="true">+</span>
    <span class="drop__label">{label}</span>
    <span class="drop__sub">{sublabel}</span>
  </button>
</div>

{#if files.length}
  <ol class="files">
    {#each files as f, i (f.name + i)}
      <li class="file">
        <span class="file__num">{String(i + 1).padStart(2, '0')}</span>
        <span class="file__body">
          <span class="file__name">{f.name}</span>
          <span class="file__meta">
            {fmtSize(f.size)} &middot; {f.type || 'unknown'}
          </span>
        </span>
        {#if multiple}
          <span class="file__actions">
            <button type="button" class="micro" disabled={i === 0} onclick={() => move(i, -1)} aria-label="Move up">↑</button>
            <button type="button" class="micro" disabled={i === files.length - 1} onclick={() => move(i, 1)} aria-label="Move down">↓</button>
          </span>
        {/if}
        <button type="button" class="micro micro--del" onclick={() => remove(i)} aria-label="Remove">×</button>
      </li>
    {/each}
  </ol>
{/if}

<style>
  .drop {
    position: relative;
  }

  .drop__inner {
    position: relative;
    display: grid;
    place-items: center;
    gap: 6px;
    width: 100%;
    min-height: 240px;
    padding: 36px;
    background: repeating-linear-gradient(
      45deg,
      transparent 0 14px,
      #18141008 14px 15px
    ), var(--paper-2);
    border: 1px dashed var(--rule-strong);
    border-radius: var(--rad-lg);
    cursor: pointer;
    transition: background 200ms ease, transform 200ms ease, border-color 200ms ease;
  }

  .drop__inner:hover {
    border-color: var(--accent);
    transform: translateY(-1px);
  }

  .drop--active .drop__inner {
    border-color: var(--accent);
    background: var(--accent-tint), var(--paper-2);
  }

  .drop__corner {
    position: absolute;
    width: 14px;
    height: 14px;
    border: 1px solid var(--ink);
  }
  .drop__corner--tl { top: 8px; left: 8px; border-right: 0; border-bottom: 0; }
  .drop__corner--tr { top: 8px; right: 8px; border-left: 0; border-bottom: 0; }
  .drop__corner--bl { bottom: 8px; left: 8px; border-right: 0; border-top: 0; }
  .drop__corner--br { bottom: 8px; right: 8px; border-left: 0; border-top: 0; }

  .drop__mark {
    font-family: var(--serif);
    font-style: italic;
    font-size: 3rem;
    color: var(--accent);
    line-height: 1;
    font-variation-settings: 'opsz' 144;
  }

  .drop__label {
    font-family: var(--serif);
    font-size: 1.3rem;
    color: var(--ink);
  }

  .drop__sub {
    font-family: var(--mono);
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--ink-mute);
  }

  .files {
    list-style: none;
    padding: 0;
    margin: 24px 0 0;
    display: grid;
    gap: 0;
    border-top: 1px solid var(--rule-strong);
  }

  .file {
    display: grid;
    grid-template-columns: 36px 1fr auto auto;
    align-items: center;
    gap: 16px;
    padding: 14px 4px;
    border-bottom: 1px solid var(--rule);
  }

  .file__num {
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--ink-mute);
  }

  .file__body { display: grid; gap: 2px; min-width: 0; }
  .file__name {
    font-family: var(--serif);
    font-size: 1.05rem;
    color: var(--ink);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .file__meta {
    font-family: var(--mono);
    font-size: 0.7rem;
    letter-spacing: 0.06em;
    color: var(--ink-mute);
  }

  .file__actions { display: inline-flex; gap: 4px; }

  .micro {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    border: 1px solid var(--rule-strong);
    background: var(--paper);
    color: var(--ink);
    font-family: var(--mono);
    font-size: 0.85rem;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: background 160ms ease, color 160ms ease;
  }

  .micro:hover { background: var(--ink); color: var(--paper); }
  .micro:disabled { opacity: 0.3; cursor: not-allowed; }
  .micro--del:hover { background: var(--accent); border-color: var(--accent); }
</style>
