<script>
  import '../app.css';
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { token, user, logout } from '$lib/auth.js';
  import { fetchMe } from '$lib/profile.js';

  let avatarUrl = $state(null);
  let mounted = $state(false);

  onMount(async () => {
    mounted = true;
    if ($token && !$user) {
      try {
        await fetchMe();
      } catch {
        logout();
      }
    }
  });

  $effect(() => {
    if ($user?.avatar_url) {
      avatarUrl = $user.avatar_url + (`?t=${Date.now()}`);
    } else {
      avatarUrl = null;
    }
  });

  function onLogout() {
    logout();
    goto('/login');
  }

  let { children } = $props();
</script>

<div class="shell">
  <header class="masthead">
    <div class="masthead__bar">
      <div class="masthead__mark">
        <a href="/" class="mark">
          <span class="mark__symbol" aria-hidden="true">A</span>
          <span class="mark__name">Atelier</span>
          <span class="mark__sep">/</span>
          <span class="mark__sub">Tools</span>
        </a>
      </div>

      <nav class="masthead__nav" aria-label="Primary">
        <a href="/tools/pdf/merge" class:active={$page.url.pathname.startsWith('/tools/pdf/merge')}>
          <span class="num">i.</span> Merge
        </a>
        <a href="/tools/pdf/split" class:active={$page.url.pathname.startsWith('/tools/pdf/split')}>
          <span class="num">ii.</span> Split
        </a>
        <a href="/tools/pdf/image-to-pdf" class:active={$page.url.pathname.startsWith('/tools/pdf/image-to-pdf')}>
          <span class="num">iii.</span> Images
        </a>
      </nav>

      <div class="masthead__account">
        {#if mounted && $token && $user}
          <a href="/profile" class="account">
            <span class="account__name">{$user.username}</span>
            <span class="account__avatar" aria-hidden="true">
              {#if avatarUrl}
                <img src={avatarUrl} alt="" />
              {:else}
                <span>{$user.username?.[0]?.toUpperCase() ?? '·'}</span>
              {/if}
            </span>
          </a>
          <button class="lnk" onclick={onLogout}>Sign out</button>
        {:else if mounted}
          <a href="/login" class="lnk lnk--strong">Sign in &rarr;</a>
        {/if}
      </div>
    </div>

    <div class="masthead__rule" aria-hidden="true">
      <span class="masthead__date">
        {new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'long', year: 'numeric' })}
      </span>
      <span class="masthead__rule-line"></span>
      <span class="masthead__edition">Vol. I &middot; Edition 01</span>
    </div>
  </header>

  <main class="main">
    {@render children()}
  </main>

  <footer class="foot">
    <div class="foot__inner">
      <span class="foot__col">
        <span class="eyebrow">Colophon</span>
        <p class="foot__text">
          Set in <em>Fraunces</em> &amp; <em>IBM Plex</em>. Printed on cream &mdash; rendered in pixels.
        </p>
      </span>
      <span class="foot__col foot__col--mid">
        <span class="eyebrow">Local</span>
        <p class="foot__text">localhost:3000 &middot; api: /api/*</p>
      </span>
      <span class="foot__col foot__col--end">
        <span class="eyebrow">&copy;</span>
        <p class="foot__text">{new Date().getFullYear()} &mdash; an open workshop.</p>
      </span>
    </div>
  </footer>
</div>

<style>
  .shell {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .masthead {
    padding: 22px clamp(20px, 4vw, 56px) 0;
  }

  .masthead__bar {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 24px;
  }

  .mark {
    display: inline-flex;
    align-items: baseline;
    gap: 10px;
    color: var(--ink);
  }

  .mark:hover {
    color: var(--ink);
    text-decoration: none;
  }

  .mark__symbol {
    font-family: var(--serif);
    font-style: italic;
    font-weight: 300;
    font-size: 1.85rem;
    line-height: 1;
    color: var(--accent);
    font-variation-settings: 'opsz' 144;
  }

  .mark__name {
    font-family: var(--serif);
    font-weight: 500;
    font-size: 1.05rem;
    letter-spacing: 0.02em;
  }

  .mark__sep {
    font-family: var(--serif);
    color: var(--ink-mute);
    font-style: italic;
  }

  .mark__sub {
    font-family: var(--mono);
    font-size: 0.7rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--ink-mute);
  }

  .masthead__nav {
    display: flex;
    gap: 28px;
    justify-content: center;
  }

  .masthead__nav a {
    font-family: var(--mono);
    font-size: 0.74rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--ink-mute);
    padding: 6px 0;
    border-bottom: 1px solid transparent;
    transition: color 160ms ease, border-color 160ms ease;
  }

  .masthead__nav a:hover {
    color: var(--ink);
    text-decoration: none;
    border-bottom-color: var(--rule-strong);
  }

  .masthead__nav a.active {
    color: var(--accent);
    border-bottom-color: var(--accent);
  }

  .num {
    font-style: italic;
    color: var(--ink-mute);
    margin-right: 4px;
  }

  .masthead__account {
    display: flex;
    align-items: center;
    gap: 18px;
    justify-content: flex-end;
  }

  .account {
    display: inline-flex;
    align-items: center;
    gap: 10px;
  }

  .account__name {
    font-family: var(--mono);
    font-size: 0.78rem;
    letter-spacing: 0.04em;
  }

  .account__avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--ink);
    color: var(--paper);
    overflow: hidden;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-family: var(--serif);
    font-style: italic;
    font-size: 0.95rem;
    border: 1px solid var(--rule-strong);
  }

  .account__avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .lnk {
    font-family: var(--mono);
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--ink-mute);
    cursor: pointer;
    transition: color 160ms ease;
  }

  .lnk:hover { color: var(--accent); }
  .lnk--strong { color: var(--ink); }

  .masthead__rule {
    margin-top: 18px;
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    gap: 16px;
    padding-bottom: 18px;
    border-bottom: 1px solid var(--rule-strong);
  }

  .masthead__date,
  .masthead__edition {
    font-family: var(--mono);
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--ink-mute);
  }

  .masthead__rule-line {
    height: 1px;
    background: var(--rule-strong);
  }

  .main {
    flex: 1;
    padding: 56px clamp(20px, 4vw, 56px);
  }

  .foot {
    padding: 32px clamp(20px, 4vw, 56px);
    border-top: 1px solid var(--rule-strong);
    margin-top: 64px;
  }

  .foot__inner {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 24px;
    align-items: start;
  }

  .foot__col p {
    margin: 6px 0 0;
    font-family: var(--serif);
    font-style: italic;
    color: var(--ink-mute);
  }

  .foot__col--mid { text-align: center; }
  .foot__col--end { text-align: right; }

  @media (max-width: 800px) {
    .masthead__bar {
      grid-template-columns: 1fr 1fr;
    }
    .masthead__nav {
      grid-column: 1 / -1;
      order: 3;
      justify-content: flex-start;
      flex-wrap: wrap;
    }
    .foot__inner { grid-template-columns: 1fr; }
    .foot__col--mid, .foot__col--end { text-align: left; }
  }
</style>
