<script>
  import { token } from '$lib/auth.js';

  const tools = [
    {
      slug: 'merge',
      title: 'Merge PDFs',
      sub: 'Combine multiple PDFs into one bound document',
      verb: 'Bind',
      accent: 'volt',
      icon: 'M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01'
    },
    {
      slug: 'split',
      title: 'Split a PDF',
      sub: 'Extract a precise page range from any PDF',
      verb: 'Extract',
      accent: 'plum',
      icon: 'M9 3H5a2 2 0 0 0-2 2v4M19 3h-4M21 9V5a2 2 0 0 0-2-2M3 15v4a2 2 0 0 0 2 2h4M21 15v4a2 2 0 0 1-2 2h-4'
    },
    {
      slug: 'image-to-pdf',
      title: 'Images → PDF',
      sub: 'Stitch JPEGs, PNGs, or WebPs into a single PDF',
      verb: 'Convert',
      accent: 'rose',
      icon: 'M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12'
    }
  ];
</script>

<svelte:head><title>Voltage — fast, self-hosted file tools</title></svelte:head>

<section class="hero">
  <div class="hero__lead">
    <span class="pill rise rise-1">
      <span class="pill__dot"></span>
      Self-hosted · No data leaves your server
    </span>
    <h1 class="display rise rise-2">
      File tools<br/>without<br/>the <span class="hero__accent">noise</span>.
    </h1>
    <p class="hero__lede rise rise-3">
      A small set of focused utilities for PDFs and images. Open-source, self-hosted, and built for people who want their tools fast and quiet.
    </p>
    <div class="hero__actions rise rise-4">
      {#if $token}
        <a class="btn" href="/tools/pdf/merge">
          Open studio
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" /></svg>
        </a>
        <a class="btn btn--ghost" href="/profile">Manage account</a>
      {:else}
        <a class="btn" href="/login">
          Sign in
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" /></svg>
        </a>
        <span class="hero__hint">
          <span class="kbd">⏎</span>
          Account required — ask the admin
        </span>
      {/if}
    </div>
  </div>

  <aside class="hero__art rise rise-2" aria-hidden="true">
    <div class="art">
      <div class="art__card art__card--a">
        <span class="art__dot"></span>
        <span class="art__line art__line--1"></span>
        <span class="art__line art__line--2"></span>
        <span class="art__line art__line--3"></span>
      </div>
      <div class="art__card art__card--b">
        <span class="art__dot"></span>
        <span class="art__line art__line--1"></span>
        <span class="art__line art__line--2"></span>
      </div>
      <div class="art__card art__card--c">
        <span class="art__dot"></span>
        <span class="art__line art__line--1"></span>
        <span class="art__line art__line--2"></span>
        <span class="art__line art__line--3"></span>
        <span class="art__line art__line--4"></span>
      </div>
      <div class="art__bolt">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="var(--volt)">
          <path d="M11 2L3 14h7l-2 8 11-14h-7l2-6z" />
        </svg>
      </div>
    </div>
  </aside>
</section>

<section class="bento">
  <header class="bento__head rise rise-3">
    <span class="eyebrow">Tools</span>
    <h2 class="bento__title">Three instruments. One bench.</h2>
  </header>

  <div class="grid">
    {#each tools as t, i}
      <a href={`/tools/pdf/${t.slug}`} class="card-tool rise rise-{4 + i}" data-accent={t.accent}>
        <span class="card-tool__top">
          <span class="card-tool__icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <path d={t.icon} />
            </svg>
          </span>
          <span class="card-tool__verb">{t.verb}</span>
        </span>
        <span class="card-tool__body">
          <h3 class="card-tool__title">{t.title}</h3>
          <p class="card-tool__sub">{t.sub}</p>
        </span>
        <span class="card-tool__cta">
          <span>Open</span>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" /></svg>
        </span>
      </a>
    {/each}
  </div>
</section>

<section class="features rise rise-5">
  <div class="feat">
    <span class="feat__num">99 MB</span>
    <span class="feat__lbl">Max upload</span>
  </div>
  <div class="feat">
    <span class="feat__num">~1s</span>
    <span class="feat__lbl">Avg. process</span>
  </div>
  <div class="feat">
    <span class="feat__num">0</span>
    <span class="feat__lbl">Trackers</span>
  </div>
  <div class="feat">
    <span class="feat__num">24h</span>
    <span class="feat__lbl">Output TTL</span>
  </div>
</section>

<style>
  .hero {
    display: grid;
    grid-template-columns: 1.4fr 1fr;
    gap: clamp(32px, 6vw, 80px);
    align-items: center;
    padding: 48px 0 80px;
  }

  .pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    background: var(--surface);
    border: 1px solid var(--line-2);
    border-radius: var(--r-pill);
    font-family: var(--mono);
    font-size: 0.74rem;
    color: var(--fg-2);
  }
  .pill__dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--volt);
    box-shadow: 0 0 12px var(--volt-glow);
    animation: pulse 2s var(--ease) infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }

  .display {
    margin-top: 24px;
    font-size: clamp(3.4rem, 8vw, 6.4rem);
  }

  .hero__accent {
    background: linear-gradient(120deg, var(--volt) 0%, var(--volt-2) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-style: italic;
    font-family: var(--serif);
    font-weight: 400;
  }

  .hero__lede {
    margin-top: 24px;
    color: var(--fg-2);
    font-size: 1.1rem;
    line-height: 1.55;
    max-width: 50ch;
  }

  .hero__actions {
    margin-top: 32px;
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
  }

  .hero__hint {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--fg-mute);
  }

  /* Hero art — abstract floating cards */
  .hero__art {
    position: relative;
    aspect-ratio: 1 / 1;
    max-width: 460px;
    width: 100%;
    margin-left: auto;
  }

  .art {
    position: relative;
    width: 100%;
    height: 100%;
  }

  .art__card {
    position: absolute;
    width: 56%;
    aspect-ratio: 3 / 4;
    background: var(--surface);
    border: 1px solid var(--line-3);
    border-radius: var(--r-2);
    padding: 18px;
    display: grid;
    gap: 8px;
    align-content: start;
    box-shadow: var(--shadow-1);
    backdrop-filter: blur(20px);
  }

  .art__card--a {
    top: 4%;
    left: 0;
    transform: rotate(-7deg);
    z-index: 2;
    animation: float 8s var(--ease) infinite;
  }
  .art__card--b {
    top: 22%;
    right: 4%;
    transform: rotate(6deg);
    z-index: 1;
    background: var(--surface-2);
    animation: float 9s var(--ease) infinite -3s;
  }
  .art__card--c {
    bottom: 0;
    left: 18%;
    transform: rotate(-2deg);
    z-index: 3;
    border-color: var(--volt);
    box-shadow: 0 0 0 1px var(--volt-glow), var(--shadow-1);
    animation: float 10s var(--ease) infinite -5s;
  }

  @keyframes float {
    0%, 100% { translate: 0 0; }
    50% { translate: 0 -10px; }
  }

  .art__dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--volt);
  }
  .art__card--b .art__dot { background: var(--plum); }
  .art__card--c .art__dot { background: var(--rose); }

  .art__line {
    height: 6px;
    background: var(--surface-3);
    border-radius: var(--r-pill);
  }
  .art__line--1 { width: 80%; }
  .art__line--2 { width: 60%; }
  .art__line--3 { width: 70%; }
  .art__line--4 { width: 45%; }

  .art__bolt {
    position: absolute;
    bottom: 12%;
    right: 6%;
    z-index: 4;
    background: var(--surface);
    width: 84px;
    height: 84px;
    border-radius: 50%;
    border: 1px solid var(--volt);
    display: grid;
    place-items: center;
    box-shadow: 0 0 32px var(--volt-glow), inset 0 0 0 1px #0a0a0c;
    animation: spin 12s linear infinite;
  }
  @keyframes spin {
    from { rotate: 0deg; }
    to { rotate: 360deg; }
  }
  .art__bolt svg { animation: spin 12s linear infinite reverse; }

  /* Bento section */
  .bento {
    margin-top: 32px;
  }

  .bento__head {
    display: flex;
    align-items: baseline;
    gap: 18px;
    margin-bottom: 24px;
  }

  .bento__title {
    font-size: clamp(1.6rem, 3vw, 2.2rem);
    letter-spacing: -0.02em;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }

  .card-tool {
    position: relative;
    display: grid;
    gap: 36px;
    padding: 24px;
    min-height: 240px;
    background: linear-gradient(180deg, var(--surface) 0%, var(--bg-elev) 100%);
    border: 1px solid var(--line-2);
    border-radius: var(--r-2);
    overflow: hidden;
    color: var(--fg);
    transition: border-color 280ms var(--ease), transform 280ms var(--ease), box-shadow 280ms var(--ease);
  }
  .card-tool::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(400px 200px at 50% 0%, var(--volt-tint) 0%, transparent 60%);
    opacity: 0;
    transition: opacity 300ms var(--ease);
    pointer-events: none;
  }
  .card-tool:hover {
    border-color: var(--volt);
    transform: translateY(-2px);
    color: var(--fg);
    box-shadow: 0 16px 36px -16px var(--volt-glow);
  }
  .card-tool:hover::after { opacity: 1; }

  .card-tool[data-accent="plum"]:hover {
    border-color: var(--plum);
    box-shadow: 0 16px 36px -16px #7c5cff60;
  }
  .card-tool[data-accent="plum"]::after {
    background: radial-gradient(400px 200px at 50% 0%, var(--plum-tint) 0%, transparent 60%);
  }
  .card-tool[data-accent="rose"]:hover {
    border-color: var(--rose);
    box-shadow: 0 16px 36px -16px #ff5c8a50;
  }
  .card-tool[data-accent="rose"]::after {
    background: radial-gradient(400px 200px at 50% 0%, #ff5c8a14 0%, transparent 60%);
  }

  .card-tool__top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    z-index: 1;
  }

  .card-tool__icon {
    display: grid;
    place-items: center;
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: var(--surface-3);
    color: var(--volt);
    border: 1px solid var(--line-2);
  }
  .card-tool[data-accent="plum"] .card-tool__icon { color: var(--plum); }
  .card-tool[data-accent="rose"] .card-tool__icon { color: var(--rose); }

  .card-tool__verb {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--fg-mute);
    padding: 4px 10px;
    border-radius: var(--r-pill);
    background: var(--surface-3);
    border: 1px solid var(--line-2);
  }

  .card-tool__title {
    font-size: 1.45rem;
    font-weight: 500;
    z-index: 1;
    margin-bottom: 6px;
  }
  .card-tool__sub {
    color: var(--fg-2);
    font-size: 0.92rem;
    line-height: 1.5;
    margin: 0;
    max-width: 30ch;
    z-index: 1;
  }

  .card-tool__cta {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    align-self: end;
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--fg-mute);
    transition: color 200ms var(--ease), gap 200ms var(--ease);
    z-index: 1;
  }
  .card-tool:hover .card-tool__cta {
    color: var(--volt);
    gap: 10px;
  }
  .card-tool[data-accent="plum"]:hover .card-tool__cta { color: var(--plum); }
  .card-tool[data-accent="rose"]:hover .card-tool__cta { color: var(--rose); }

  /* Features */
  .features {
    margin-top: 64px;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--line-2);
    border: 1px solid var(--line-2);
    border-radius: var(--r-2);
    overflow: hidden;
  }

  .feat {
    background: var(--bg);
    padding: 28px 24px;
    display: grid;
    gap: 4px;
  }

  .feat__num {
    font-family: var(--sans);
    font-size: 1.8rem;
    font-weight: 500;
    color: var(--fg);
    letter-spacing: -0.03em;
  }

  .feat__lbl {
    font-family: var(--mono);
    font-size: 0.74rem;
    color: var(--fg-mute);
  }

  @media (max-width: 960px) {
    .hero { grid-template-columns: 1fr; }
    .hero__art { max-width: 360px; margin: 0 auto; }
    .grid { grid-template-columns: 1fr; }
    .features { grid-template-columns: repeat(2, 1fr); }
  }
</style>
