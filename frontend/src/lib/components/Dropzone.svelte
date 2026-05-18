<script>
  let {
    multiple = false,
    accept = '',
    files = $bindable([]),
    label = 'Drop files here',
    sublabel = 'or click to browse'
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
    <span class="drop__halo" aria-hidden="true"></span>
    <span class="drop__icon" aria-hidden="true">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 13V3" />
        <path d="M7 8l5-5 5 5" />
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      </svg>
    </span>
    <span class="drop__label">{label}</span>
    <span class="drop__sub">{sublabel}</span>
  </button>
</div>

{#if files.length}
  <ol class="files">
    {#each files as f, i (f.name + i)}
      <li class="file">
        <span class="file__num">{String(i + 1).padStart(2, '0')}</span>
        <span class="file__icon" aria-hidden="true">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
          </svg>
        </span>
        <span class="file__body">
          <span class="file__name">{f.name}</span>
          <span class="file__meta">{fmtSize(f.size)}</span>
        </span>
        {#if multiple}
          <span class="file__actions">
            <button type="button" class="micro" disabled={i === 0} onclick={() => move(i, -1)} aria-label="Move up">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15" /></svg>
            </button>
            <button type="button" class="micro" disabled={i === files.length - 1} onclick={() => move(i, 1)} aria-label="Move down">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9" /></svg>
            </button>
          </span>
        {/if}
        <button type="button" class="micro micro--del" onclick={() => remove(i)} aria-label="Remove">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" /></svg>
        </button>
      </li>
    {/each}
  </ol>
{/if}

<style>
  .drop { position: relative; }

  .drop__inner {
    position: relative;
    display: grid;
    place-items: center;
    gap: 8px;
    width: 100%;
    min-height: 220px;
    padding: 36px;
    background: var(--surface);
    border: 1px dashed var(--line-3);
    border-radius: var(--r-2);
    cursor: pointer;
    overflow: hidden;
    transition: background 200ms var(--ease), border-color 200ms var(--ease), transform 200ms var(--ease);
  }
  .drop__inner::after {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
      radial-gradient(#ffffff08 1px, transparent 1px);
    background-size: 22px 22px;
    pointer-events: none;
    opacity: 0.6;
  }
  .drop__inner:hover {
    border-color: var(--volt);
    background: var(--surface-2);
  }
  .drop--active .drop__inner {
    border-color: var(--volt);
    background: var(--volt-tint);
    transform: scale(1.005);
  }
  .drop__halo {
    position: absolute;
    width: 200px; height: 200px;
    border-radius: 50%;
    background: radial-gradient(circle, var(--volt-glow) 0%, transparent 70%);
    opacity: 0;
    transition: opacity 300ms var(--ease);
    pointer-events: none;
  }
  .drop__inner:hover .drop__halo,
  .drop--active .drop__halo { opacity: 1; }

  .drop__icon {
    display: grid;
    place-items: center;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: var(--surface-3);
    color: var(--volt);
    margin-bottom: 4px;
    border: 1px solid var(--line-2);
    z-index: 1;
  }

  .drop__label {
    font-size: 1.05rem;
    font-weight: 500;
    color: var(--fg);
    z-index: 1;
  }
  .drop__sub {
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--fg-mute);
    z-index: 1;
  }

  .files {
    list-style: none;
    padding: 0;
    margin: 18px 0 0;
    display: grid;
    gap: 6px;
  }

  .file {
    display: grid;
    grid-template-columns: auto auto 1fr auto auto;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    background: var(--surface);
    border: 1px solid var(--line-2);
    border-radius: var(--r-1);
    transition: border-color 160ms var(--ease), background 160ms var(--ease);
  }
  .file:hover {
    border-color: var(--line-3);
    background: var(--surface-2);
  }

  .file__num {
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--fg-faint);
    width: 18px;
  }

  .file__icon {
    display: grid;
    place-items: center;
    width: 30px;
    height: 30px;
    border-radius: 6px;
    background: var(--surface-3);
    color: var(--fg-mute);
  }

  .file__body { display: grid; gap: 1px; min-width: 0; }
  .file__name {
    font-size: 0.92rem;
    color: var(--fg);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .file__meta {
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--fg-mute);
  }

  .file__actions { display: inline-flex; gap: 4px; }

  .micro {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    background: var(--surface-3);
    color: var(--fg-mute);
    border: 1px solid transparent;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background 160ms var(--ease), color 160ms var(--ease), border-color 160ms var(--ease);
  }
  .micro:hover { background: var(--surface); color: var(--fg); border-color: var(--line-3); }
  .micro:disabled { opacity: 0.3; cursor: not-allowed; }
  .micro--del:hover { background: #ff5c8a18; color: var(--rose); border-color: #ff5c8a40; }
</style>
