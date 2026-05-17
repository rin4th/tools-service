<script>
  import { token } from '$lib/auth.js';

  const tools = [
    { num: 'i', slug: 'merge', title: 'Merge', sub: 'Compose multiple PDFs into a single bound volume.', verb: 'Bind' },
    { num: 'ii', slug: 'split', title: 'Split', sub: 'Excerpt a precise range — page x to y, nothing more.', verb: 'Excerpt' },
    { num: 'iii', slug: 'image-to-pdf', title: 'Images', sub: 'Set photographs and stills onto crisp PDF pages.', verb: 'Set' }
  ];
</script>

<section class="hero">
  <div class="hero__col hero__col--lead">
    <p class="eyebrow rise rise-1">No. 01 &mdash; A workshop</p>
    <h1 class="display rise rise-2">
      Quiet<br /><em>tools</em><br />for noisy<br />documents.
    </h1>
    <p class="lede rise rise-3">
      A small studio of utilities for handling PDFs &mdash; merge, excerpt, set
      from images. Made for people who prefer their interfaces in the
      background, and their work in the foreground.
    </p>
    <div class="actions rise rise-4">
      {#if $token}
        <a class="btn" href="/tools/pdf/merge">Open the studio &rarr;</a>
        <a class="lnk" href="/profile">Manage account</a>
      {:else}
        <a class="btn" href="/login">Sign in &rarr;</a>
        <span class="lnk lnk--mute">Account required</span>
      {/if}
    </div>
  </div>

  <aside class="hero__col hero__col--mark" aria-hidden="true">
    <div class="hero__mark rise rise-2">
      <span class="hero__mark__big">A</span>
      <span class="hero__mark__year">MMXXVI</span>
      <span class="hero__mark__rule"></span>
      <span class="hero__mark__lat"><em>Faber est suae quisque fortunae</em></span>
    </div>
  </aside>
</section>

<div class="rule rise rise-3"></div>

<section class="index">
  <header class="index__head rise rise-3">
    <span class="section-num">§ 02 &mdash; Index of tools</span>
    <h2 class="index__title">Three instruments, one bench.</h2>
  </header>

  <ol class="grid">
    {#each tools as t, i}
      <li class="cell rise rise-{4 + i}">
        <a class="cell__link" href={`/tools/pdf/${t.slug}`}>
          <span class="cell__num">{t.num}.</span>
          <h3 class="cell__title">{t.title}</h3>
          <p class="cell__sub">{t.sub}</p>
          <span class="cell__verb">
            <span>{t.verb}</span>
            <span class="cell__arrow">&rarr;</span>
          </span>
        </a>
      </li>
    {/each}
  </ol>
</section>

<style>
  .hero {
    display: grid;
    grid-template-columns: 1.4fr 1fr;
    gap: clamp(24px, 6vw, 96px);
    align-items: stretch;
    padding: 48px 0 64px;
  }

  .hero__col--lead { max-width: 720px; }

  .display {
    margin-top: 22px;
    font-size: clamp(3.6rem, 9vw, 8rem);
  }

  .display em {
    font-style: italic;
    color: var(--accent);
    font-variation-settings: 'opsz' 144, 'SOFT' 100;
  }

  .lede {
    margin-top: 32px;
    max-width: 52ch;
    font-family: var(--serif);
    font-size: 1.2rem;
    line-height: 1.5;
    color: var(--ink-2);
  }

  .actions {
    margin-top: 36px;
    display: flex;
    align-items: center;
    gap: 20px;
  }

  .lnk {
    font-family: var(--mono);
    font-size: 0.74rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--ink-mute);
  }

  .lnk--mute { color: var(--ink-mute); }

  .hero__col--mark {
    align-self: stretch;
    border-left: 1px solid var(--rule-strong);
    padding-left: clamp(20px, 3vw, 48px);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .hero__mark {
    text-align: center;
    color: var(--ink);
    display: grid;
    gap: 18px;
    place-items: center;
    padding: 32px;
    border: 1px solid var(--rule-strong);
    background: var(--paper-2);
    box-shadow: var(--shadow-paper);
    transform: rotate(-1.2deg);
    max-width: 360px;
    width: 100%;
  }

  .hero__mark__big {
    font-family: var(--serif);
    font-size: clamp(8rem, 14vw, 12rem);
    font-style: italic;
    font-weight: 300;
    line-height: 0.85;
    color: var(--accent);
    font-variation-settings: 'opsz' 144, 'SOFT' 60;
  }

  .hero__mark__year {
    font-family: var(--mono);
    font-size: 0.7rem;
    letter-spacing: 0.4em;
    color: var(--ink-mute);
  }

  .hero__mark__rule {
    width: 32px;
    height: 1px;
    background: var(--rule-strong);
  }

  .hero__mark__lat {
    font-family: var(--serif);
    font-style: italic;
    color: var(--ink-mute);
    font-size: 0.95rem;
    line-height: 1.3;
    max-width: 24ch;
  }

  .index { padding: 56px 0 16px; }

  .index__head {
    display: grid;
    gap: 12px;
    margin-bottom: 36px;
    max-width: 60ch;
  }

  .index__title {
    font-family: var(--serif);
    font-size: clamp(1.6rem, 3vw, 2.4rem);
    line-height: 1.1;
  }

  .grid {
    list-style: none;
    margin: 0;
    padding: 0;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border-top: 1px solid var(--rule-strong);
    border-left: 1px solid var(--rule-strong);
  }

  .cell {
    border-right: 1px solid var(--rule-strong);
    border-bottom: 1px solid var(--rule-strong);
    background: transparent;
    transition: background 200ms ease;
  }

  .cell:hover { background: var(--paper-2); }

  .cell__link {
    display: block;
    padding: 36px 32px;
    color: var(--ink);
    height: 100%;
  }

  .cell__link:hover { text-decoration: none; color: var(--ink); }

  .cell__num {
    display: inline-block;
    font-family: var(--serif);
    font-style: italic;
    font-size: 1.3rem;
    color: var(--accent);
    margin-bottom: 18px;
  }

  .cell__title {
    font-family: var(--serif);
    font-size: 2.4rem;
    line-height: 1;
    margin-bottom: 14px;
    font-weight: 400;
    letter-spacing: -0.02em;
  }

  .cell__sub {
    font-family: var(--serif);
    font-style: italic;
    color: var(--ink-mute);
    font-size: 1.02rem;
    line-height: 1.45;
    margin: 0 0 28px;
    max-width: 32ch;
  }

  .cell__verb {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: var(--mono);
    font-size: 0.74rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--ink-mute);
    transition: color 160ms ease, gap 160ms ease;
  }

  .cell:hover .cell__verb {
    color: var(--accent);
    gap: 14px;
  }

  .cell__arrow { transition: transform 160ms ease; }
  .cell:hover .cell__arrow { transform: translateX(2px); }

  @media (max-width: 900px) {
    .hero { grid-template-columns: 1fr; }
    .hero__col--mark { border-left: 0; padding-left: 0; padding-top: 24px; }
    .grid { grid-template-columns: 1fr; }
  }
</style>
