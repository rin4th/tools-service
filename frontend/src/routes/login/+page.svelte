<script>
  import { goto } from '$app/navigation';
  import { setToken } from '$lib/auth.js';
  import { login, fetchMe } from '$lib/profile.js';

  let username = $state('');
  let password = $state('');
  let loading = $state(false);
  let error = $state('');
  let showPwd = $state(false);

  async function onSubmit(e) {
    e.preventDefault();
    if (loading) return;
    error = '';
    loading = true;
    try {
      const { access_token } = await login(username.trim(), password);
      setToken(access_token);
      await fetchMe();
      goto('/tools/pdf/merge');
    } catch (err) {
      error = err.message || 'Sign in failed';
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head><title>Sign in — Voltage</title></svelte:head>

<section class="login">
  <div class="login__panel">
    <a href="/" class="login__back">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12" /><polyline points="12 19 5 12 12 5" /></svg>
      Back home
    </a>

    <div class="login__head rise rise-1">
      <span class="brand-mark" aria-hidden="true">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
          <rect x="2" y="2" width="20" height="20" rx="6" fill="var(--volt)"/>
          <path d="M11 5L6 13h4.5l-1.5 6 7.5-10h-4.5l1.5-4z" fill="var(--bg)"/>
        </svg>
      </span>
      <h1 class="login__title">Welcome back.</h1>
      <p class="login__sub">Sign in to access the studio.</p>
    </div>

    <form class="login__form rise rise-2" onsubmit={onSubmit} novalidate>
      <label class="field">
        <span class="field__label">Username</span>
        <input
          class="field__input"
          type="text"
          autocomplete="username"
          bind:value={username}
          placeholder="your handle"
          required
          minlength="3"
          maxlength="64"
        />
      </label>

      <label class="field">
        <span class="field__label">Password</span>
        <span class="pwd">
          <input
            class="field__input"
            type={showPwd ? 'text' : 'password'}
            autocomplete="current-password"
            bind:value={password}
            placeholder="••••••••"
            required
            minlength="6"
          />
          <button type="button" class="pwd__toggle" onclick={() => (showPwd = !showPwd)} aria-label={showPwd ? 'Hide password' : 'Show password'}>
            {#if showPwd}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
            {:else}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            {/if}
          </button>
        </span>
      </label>

      {#if error}
        <p class="notice notice--err">{error}</p>
      {/if}

      <button class="btn login__submit" type="submit" disabled={loading}>
        {#if loading}
          <span class="spinner"></span>
          Verifying
        {:else}
          Sign in
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" /></svg>
        {/if}
      </button>
    </form>

    <div class="login__foot rise rise-3">
      <span>No public registration.</span>
      <span class="dot">·</span>
      <span>Ask your operator for credentials.</span>
    </div>
  </div>

  <aside class="login__art rise rise-2" aria-hidden="true">
    <div class="art-frame">
      <span class="art-frame__corner art-frame__corner--tl"></span>
      <span class="art-frame__corner art-frame__corner--tr"></span>
      <span class="art-frame__corner art-frame__corner--bl"></span>
      <span class="art-frame__corner art-frame__corner--br"></span>
      <div class="art-frame__inner">
        <div class="art-status">
          <span class="art-status__dot"></span>
          <span>service ready</span>
        </div>
        <div class="art-stat">
          <span class="art-stat__num">JWT</span>
          <span class="art-stat__lbl">60 minutes · HS256</span>
        </div>
        <div class="art-stat">
          <span class="art-stat__num">/api/*</span>
          <span class="art-stat__lbl">backend on this host</span>
        </div>
        <div class="art-stat">
          <span class="art-stat__num">localStorage</span>
          <span class="art-stat__lbl">token, yours to clear</span>
        </div>
      </div>
    </div>
  </aside>
</section>

<style>
  .login {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: clamp(32px, 6vw, 80px);
    padding: 32px 0 24px;
    align-items: center;
    min-height: calc(100vh - 200px);
  }

  .login__panel {
    max-width: 440px;
    width: 100%;
  }

  .login__back {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--fg-mute);
    margin-bottom: 32px;
    transition: color 200ms var(--ease), gap 200ms var(--ease);
  }
  .login__back:hover { color: var(--fg); gap: 8px; }

  .login__head { margin-bottom: 32px; }

  .brand-mark {
    display: inline-grid;
    place-items: center;
    margin-bottom: 18px;
  }

  .login__title {
    font-size: 2.2rem;
    font-weight: 500;
    letter-spacing: -0.03em;
    margin: 0 0 6px;
  }

  .login__sub {
    color: var(--fg-mute);
    font-size: 0.95rem;
    margin: 0;
  }

  .login__form {
    display: grid;
    gap: 18px;
  }

  .pwd {
    position: relative;
    display: block;
  }
  .pwd .field__input { padding-right: 40px; }
  .pwd__toggle {
    position: absolute;
    right: 4px;
    top: 50%;
    transform: translateY(-50%);
    width: 36px;
    height: 36px;
    border-radius: 6px;
    color: var(--fg-mute);
    display: grid;
    place-items: center;
    cursor: pointer;
    transition: background 160ms var(--ease), color 160ms var(--ease);
  }
  .pwd__toggle:hover { background: var(--surface-2); color: var(--fg); }

  .login__submit {
    width: 100%;
    height: 46px;
    margin-top: 6px;
    justify-content: center;
  }

  .spinner {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    border: 2px solid #0a0a0c40;
    border-top-color: var(--bg);
    animation: spin 700ms linear infinite;
  }

  .login__foot {
    margin-top: 28px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--fg-mute);
    flex-wrap: wrap;
  }
  .login__foot .dot { opacity: 0.5; }

  /* Art panel */
  .login__art {
    align-self: center;
    justify-self: center;
    width: 100%;
    max-width: 460px;
  }

  .art-frame {
    position: relative;
    aspect-ratio: 4 / 5;
    background:
      radial-gradient(circle at 50% 0%, var(--volt-tint) 0%, transparent 50%),
      var(--surface);
    border: 1px solid var(--line-2);
    border-radius: var(--r-3);
    padding: 28px;
    overflow: hidden;
  }

  .art-frame__corner {
    position: absolute;
    width: 14px;
    height: 14px;
    border: 1px solid var(--volt);
  }
  .art-frame__corner--tl { top: 8px; left: 8px; border-right: 0; border-bottom: 0; }
  .art-frame__corner--tr { top: 8px; right: 8px; border-left: 0; border-bottom: 0; }
  .art-frame__corner--bl { bottom: 8px; left: 8px; border-right: 0; border-top: 0; }
  .art-frame__corner--br { bottom: 8px; right: 8px; border-left: 0; border-top: 0; }

  .art-frame__inner {
    height: 100%;
    display: grid;
    align-content: end;
    gap: 24px;
  }

  .art-status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    align-self: start;
    padding: 6px 12px;
    background: #5cffae12;
    border: 1px solid #5cffae40;
    border-radius: var(--r-pill);
    color: var(--good);
    font-family: var(--mono);
    font-size: 0.74rem;
    width: max-content;
  }
  .art-status__dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--good);
    box-shadow: 0 0 10px var(--good);
    animation: pulse 2s var(--ease) infinite;
  }

  .art-stat {
    display: grid;
    gap: 4px;
    padding-left: 14px;
    border-left: 2px solid var(--volt);
  }

  .art-stat__num {
    font-family: var(--mono);
    font-size: 0.92rem;
    color: var(--fg);
    font-weight: 500;
  }
  .art-stat__lbl {
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--fg-mute);
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  @media (max-width: 960px) {
    .login { grid-template-columns: 1fr; min-height: auto; }
    .login__art { display: none; }
  }
</style>
