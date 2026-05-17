<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { token, user } from '$lib/auth.js';
  import { fetchMe, changePassword } from '$lib/profile.js';
  import { apiForm } from '$lib/api.js';

  let avatarBust = $state(0);
  let avatarFile = $state(null);
  let avatarPreview = $state(null);
  let avatarBusy = $state(false);
  let avatarError = $state('');
  let avatarOk = $state('');

  let currentPwd = $state('');
  let newPwd = $state('');
  let confirmPwd = $state('');
  let pwdBusy = $state(false);
  let pwdError = $state('');
  let pwdOk = $state('');

  onMount(async () => {
    if (!$token) {
      goto('/login');
      return;
    }
    try {
      await fetchMe();
    } catch {
      goto('/login');
    }
  });

  function pickAvatar(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    avatarFile = file;
    avatarPreview = URL.createObjectURL(file);
    avatarError = '';
    avatarOk = '';
  }

  async function uploadAvatar(e) {
    e.preventDefault();
    if (!avatarFile || avatarBusy) return;
    avatarBusy = true;
    avatarError = '';
    try {
      const fd = new FormData();
      fd.append('file', avatarFile);
      const res = await apiForm('/api/profile/avatar', fd);
      const me = await res.json();
      user.set(me);
      avatarBust = Date.now();
      avatarFile = null;
      if (avatarPreview) URL.revokeObjectURL(avatarPreview);
      avatarPreview = null;
      avatarOk = 'Portrait updated.';
    } catch (err) {
      avatarError = err.message || 'Failed to upload avatar';
    } finally {
      avatarBusy = false;
    }
  }

  async function submitPassword(e) {
    e.preventDefault();
    if (pwdBusy) return;
    pwdError = '';
    pwdOk = '';
    if (newPwd !== confirmPwd) {
      pwdError = 'Confirmation does not match.';
      return;
    }
    if (newPwd.length < 6) {
      pwdError = 'Use at least six characters.';
      return;
    }
    pwdBusy = true;
    try {
      await changePassword(currentPwd, newPwd);
      pwdOk = 'Password changed.';
      currentPwd = newPwd = confirmPwd = '';
    } catch (err) {
      pwdError = err.message || 'Failed to change password';
    } finally {
      pwdBusy = false;
    }
  }

  let avatarSrc = $derived(
    avatarPreview ||
      ($user?.avatar_url ? `${$user.avatar_url}?t=${avatarBust || 1}` : null)
  );
</script>

<svelte:head><title>Profile — Atelier Tools</title></svelte:head>

<article class="profile">
  <header class="profile__head">
    <p class="section-num rise rise-1">§ 04 &mdash; Account</p>
    <h1 class="profile__title rise rise-2">
      <em>{$user?.username ?? '·'}</em>'s ledger.
    </h1>
    <p class="profile__lede rise rise-3">
      Settle your portrait and key. The rest of the workshop will follow your
      example.
    </p>
    <div class="rule rise rise-3" style="margin-top: 24px;"></div>
  </header>

  <div class="profile__body">
    <section class="block rise rise-4">
      <header class="block__head">
        <span class="section-num">No. 01</span>
        <h2 class="block__title">Portrait.</h2>
      </header>

      <div class="portrait">
        <div class="portrait__frame">
          {#if avatarSrc}
            <img src={avatarSrc} alt="Avatar" />
          {:else}
            <span class="portrait__placeholder" aria-hidden="true">
              {$user?.username?.[0]?.toUpperCase() ?? '·'}
            </span>
          {/if}
          <span class="portrait__caption">{$user?.username ?? ''}</span>
        </div>

        <form class="portrait__form" onsubmit={uploadAvatar}>
          <label class="upload">
            <input type="file" accept="image/jpeg,image/png,image/webp" onchange={pickAvatar} />
            <span class="upload__btn">Choose a likeness</span>
            <span class="upload__hint">JPEG, PNG, or WebP &middot; up to 2 MB</span>
          </label>

          {#if avatarFile}
            <p class="picked">
              <em>{avatarFile.name}</em> chosen &mdash; ready to submit.
            </p>
          {/if}

          {#if avatarError}<p class="notice notice--err">{avatarError}</p>{/if}
          {#if avatarOk}<p class="notice notice--ok">{avatarOk}</p>{/if}

          <button class="btn btn--accent" type="submit" disabled={!avatarFile || avatarBusy}>
            {avatarBusy ? 'Sending…' : 'Submit portrait'}
          </button>
        </form>
      </div>
    </section>

    <section class="block rise rise-5">
      <header class="block__head">
        <span class="section-num">No. 02</span>
        <h2 class="block__title">Key.</h2>
      </header>

      <form class="pwd" onsubmit={submitPassword}>
        <label class="field">
          <span class="field__label">Current password</span>
          <input
            class="field__input"
            type="password"
            autocomplete="current-password"
            bind:value={currentPwd}
            required
          />
        </label>

        <label class="field">
          <span class="field__label">New password</span>
          <input
            class="field__input"
            type="password"
            autocomplete="new-password"
            bind:value={newPwd}
            required
            minlength="6"
          />
        </label>

        <label class="field">
          <span class="field__label">Confirm new password</span>
          <input
            class="field__input"
            type="password"
            autocomplete="new-password"
            bind:value={confirmPwd}
            required
            minlength="6"
          />
        </label>

        {#if pwdError}<p class="notice notice--err">{pwdError}</p>{/if}
        {#if pwdOk}<p class="notice notice--ok">{pwdOk}</p>{/if}

        <button class="btn" type="submit" disabled={pwdBusy}>
          {pwdBusy ? 'Reforging…' : 'Replace key'}
        </button>
      </form>
    </section>
  </div>
</article>

<style>
  .profile { display: grid; gap: 32px; }

  .profile__title {
    font-family: var(--serif);
    font-size: clamp(2.4rem, 5vw, 3.6rem);
    line-height: 1.05;
    letter-spacing: -0.02em;
    margin: 14px 0 18px;
  }

  .profile__title em {
    font-style: italic;
    color: var(--accent);
    font-variation-settings: 'opsz' 144, 'SOFT' 80;
  }

  .profile__lede {
    font-family: var(--serif);
    font-style: italic;
    color: var(--ink-2);
    font-size: 1.1rem;
    max-width: 56ch;
  }

  .profile__body {
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: clamp(24px, 4vw, 64px);
    align-items: start;
  }

  .block { display: grid; gap: 22px; }
  .block__head { display: grid; gap: 6px; }
  .block__title {
    font-family: var(--serif);
    font-size: 1.6rem;
  }

  .portrait {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 28px;
    align-items: start;
  }

  .portrait__frame {
    width: 180px;
    background: var(--paper-2);
    border: 1px solid var(--rule-strong);
    padding: 12px 12px 14px;
    box-shadow: var(--shadow-paper);
    display: grid;
    gap: 8px;
    transform: rotate(-1deg);
  }

  .portrait__frame img {
    width: 100%;
    aspect-ratio: 1 / 1;
    object-fit: cover;
    background: var(--paper-3);
  }

  .portrait__placeholder {
    display: grid;
    place-items: center;
    aspect-ratio: 1 / 1;
    background: var(--ink);
    color: var(--paper);
    font-family: var(--serif);
    font-style: italic;
    font-size: 4.5rem;
  }

  .portrait__caption {
    font-family: var(--mono);
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--ink-mute);
    text-align: center;
  }

  .portrait__form { display: grid; gap: 16px; align-content: start; }

  .upload { display: grid; gap: 6px; cursor: pointer; }
  .upload input { display: none; }
  .upload__btn {
    display: inline-flex;
    align-items: center;
    height: 40px;
    padding: 0 18px;
    border: 1px solid var(--rule-strong);
    border-radius: var(--rad);
    font-family: var(--mono);
    font-size: 0.74rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--ink);
    background: var(--paper);
    width: max-content;
    transition: background 160ms ease, color 160ms ease;
  }
  .upload:hover .upload__btn { background: var(--ink); color: var(--paper); }
  .upload__hint {
    font-family: var(--serif);
    font-style: italic;
    color: var(--ink-mute);
    font-size: 0.95rem;
  }

  .picked {
    margin: 0;
    font-family: var(--serif);
    font-style: italic;
    color: var(--ink-2);
  }

  .pwd { display: grid; gap: 22px; max-width: 480px; }

  @media (max-width: 900px) {
    .profile__body { grid-template-columns: 1fr; }
    .portrait { grid-template-columns: 1fr; }
  }
</style>
