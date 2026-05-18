<script>
  import '../app.css';
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { token, user, logout } from '$lib/auth.js';
  import { fetchMe } from '$lib/profile.js';

  let avatarUrl = $state(null);
  let mounted = $state(false);
  let menuOpen = $state(false);

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

  const navItems = [
    { href: '/tools/pdf/merge', label: 'Merge' },
    { href: '/tools/pdf/split', label: 'Split' },
    { href: '/tools/pdf/image-to-pdf', label: 'Images' }
  ];
</script>

<div class="shell">
  <header class="topbar">
    <div class="topbar__inner">
      <a href="/" class="brand">
        <span class="brand__logo" aria-hidden="true">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <rect x="2" y="2" width="20" height="20" rx="6" fill="var(--volt)"/>
            <path d="M11 5L6 13h4.5l-1.5 6 7.5-10h-4.5l1.5-4z" fill="var(--bg)"/>
          </svg>
        </span>
        <span class="brand__name">Voltage</span>
        <span class="brand__badge">v0.1</span>
      </a>

      <nav class="nav" aria-label="Primary">
        {#each navItems as item}
          <a href={item.href} class:active={$page.url.pathname.startsWith(item.href)}>
            {item.label}
          </a>
        {/each}
      </nav>

      <div class="topbar__right">
        {#if mounted && $token && $user}
          <button class="user" onclick={() => (menuOpen = !menuOpen)} aria-haspopup="menu" aria-expanded={menuOpen}>
            <span class="user__avatar" aria-hidden="true">
              {#if avatarUrl}
                <img src={avatarUrl} alt="" />
              {:else}
                <span>{$user.username?.[0]?.toUpperCase() ?? '·'}</span>
              {/if}
            </span>
            <span class="user__name">{$user.username}</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="opacity: 0.6;">
              <polyline points="6 9 12 15 18 9" />
            </svg>
          </button>
          {#if menuOpen}
            <div class="menu" role="menu" onmouseleave={() => (menuOpen = false)}>
              <a href="/profile" class="menu__item" onclick={() => (menuOpen = false)}>Profile</a>
              <div class="menu__divider"></div>
              <button class="menu__item menu__item--del" onclick={onLogout}>Sign out</button>
            </div>
          {/if}
        {:else if mounted}
          <a href="/login" class="btn btn--ghost">Sign in</a>
        {/if}
      </div>
    </div>
  </header>

  <main class="main">
    {@render children()}
  </main>

  <footer class="foot">
    <div class="foot__inner">
      <span class="foot__brand">
        <span class="brand__logo" aria-hidden="true" style="width: 14px; height: 14px;">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
            <rect x="2" y="2" width="20" height="20" rx="6" fill="var(--volt)"/>
            <path d="M11 5L6 13h4.5l-1.5 6 7.5-10h-4.5l1.5-4z" fill="var(--bg)"/>
          </svg>
        </span>
        Voltage Tools — self-hosted utilities
      </span>
      <span class="foot__meta">
        <span>Local · localhost:3000</span>
        <span class="foot__dot">·</span>
        <span>API /api/*</span>
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

  .topbar {
    position: sticky;
    top: 0;
    z-index: 50;
    backdrop-filter: blur(20px) saturate(140%);
    -webkit-backdrop-filter: blur(20px) saturate(140%);
    background: #0a0a0cb8;
    border-bottom: 1px solid var(--line);
  }

  .topbar__inner {
    max-width: 1400px;
    margin: 0 auto;
    padding: 14px clamp(20px, 4vw, 40px);
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    align-items: center;
    gap: 24px;
  }

  .brand {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    color: var(--fg);
  }
  .brand:hover { color: var(--fg); }

  .brand__logo {
    display: grid;
    place-items: center;
  }

  .brand__name {
    font-weight: 600;
    font-size: 1.05rem;
    letter-spacing: -0.02em;
  }

  .brand__badge {
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--fg-mute);
    padding: 2px 6px;
    border-radius: 4px;
    background: var(--surface-2);
    border: 1px solid var(--line-2);
  }

  .nav {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 4px;
    background: var(--surface);
    border: 1px solid var(--line-2);
    border-radius: var(--r-pill);
  }

  .nav a {
    padding: 7px 16px;
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--fg-mute);
    border-radius: var(--r-pill);
    transition: all 200ms var(--ease);
  }

  .nav a:hover {
    color: var(--fg);
    background: var(--surface-2);
  }

  .nav a.active {
    color: var(--bg);
    background: var(--volt);
  }
  .nav a.active:hover { background: var(--volt-2); color: var(--bg); }

  .topbar__right {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    position: relative;
  }

  .user {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 4px 12px 4px 4px;
    border-radius: var(--r-pill);
    border: 1px solid var(--line-2);
    background: var(--surface);
    cursor: pointer;
    transition: border-color 200ms var(--ease), background 200ms var(--ease);
  }

  .user:hover {
    border-color: var(--line-3);
    background: var(--surface-2);
  }

  .user__avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--volt) 0%, var(--plum) 100%);
    color: var(--bg);
    overflow: hidden;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.78rem;
  }
  .user__avatar img { width: 100%; height: 100%; object-fit: cover; }

  .user__name {
    font-size: 0.85rem;
    font-weight: 500;
  }

  .menu {
    position: absolute;
    top: calc(100% + 8px);
    right: 0;
    min-width: 180px;
    padding: 6px;
    background: var(--surface);
    border: 1px solid var(--line-3);
    border-radius: var(--r-2);
    box-shadow: var(--shadow-1);
    display: grid;
    gap: 2px;
    z-index: 100;
  }

  .menu__item {
    display: block;
    width: 100%;
    text-align: left;
    padding: 8px 12px;
    font-size: 0.88rem;
    color: var(--fg-2);
    border-radius: var(--r-1);
    transition: background 160ms var(--ease), color 160ms var(--ease);
  }
  .menu__item:hover {
    background: var(--surface-2);
    color: var(--fg);
  }
  .menu__item--del:hover { color: var(--rose); }
  .menu__divider {
    height: 1px;
    background: var(--line-2);
    margin: 4px 0;
  }

  .main {
    flex: 1;
    max-width: 1400px;
    width: 100%;
    margin: 0 auto;
    padding: 56px clamp(20px, 4vw, 40px);
  }

  .foot {
    border-top: 1px solid var(--line);
    padding: 24px clamp(20px, 4vw, 40px);
    margin-top: 64px;
  }

  .foot__inner {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--fg-mute);
  }

  .foot__brand {
    display: inline-flex;
    align-items: center;
    gap: 8px;
  }

  .foot__meta {
    display: inline-flex;
    align-items: center;
    gap: 8px;
  }
  .foot__dot { opacity: 0.5; }

  @media (max-width: 760px) {
    .topbar__inner { grid-template-columns: auto 1fr; gap: 12px; }
    .nav {
      grid-column: 1 / -1;
      order: 3;
      justify-content: center;
    }
    .nav a { padding: 6px 12px; font-size: 0.8rem; }
    .user__name { display: none; }
    .brand__badge { display: none; }
  }
</style>
