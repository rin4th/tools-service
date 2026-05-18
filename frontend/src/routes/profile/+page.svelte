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
      avatarOk = 'Avatar updated.';
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

<svelte:head><title>Account — Voltage</title></svelte:head>

<article class="profile">
  <header class="profile__head">
    <p class="eyebrow rise rise-1">Account</p>
    <h1 class="display profile__title rise rise-2">
      Hello, <span class="profile__accent">{$user?.username ?? '·'}</span>.
    </h1>
    <p class="profile__lede rise rise-3">Manage your portrait and credentials.</p>
  </header>

  <div class="grid">
    <section class="block rise rise-3">
      <header class="block__head">
        <span class="block__num">01</span>
        <h2 class="block__title">Avatar</h2>
        <span class="block__hint">JPEG · PNG · WebP, up to 2 MB</span>
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
        </div>

        <form class="portrait__form" onsubmit={uploadAvatar}>
          <label class="upload">
            <input type="file" accept="image/jpeg,image/png,image/webp" onchange={pickAvatar} hidden />
            <span class="upload__btn">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/></svg>
              Choose image
            </span>
          </label>

          {#if avatarFile}
            <p class="picked">{avatarFile.name} ready to upload</p>
          {/if}

          {#if avatarError}<p class="notice notice--err">{avatarError}</p>{/if}
          {#if avatarOk}<p class="notice notice--ok">{avatarOk}</p>{/if}

          <button class="btn" type="submit" disabled={!avatarFile || avatarBusy}>
            {#if avatarBusy}
              <span class="spinner"></span>
              Uploading
            {:else}
              Save avatar
            {/if}
          </button>
        </form>
      </div>
    </section>

    <section class="block rise rise-4">
      <header class="block__head">
        <span class="block__num">02</span>
        <h2 class="block__title">Password</h2>
        <span class="block__hint">Use at least 6 characters</span>
      </header>

      <form class="pwd" onsubmit={submitPassword}>
        <label class="field">
          <span class="field__label">Current password</span>
          <input class="field__input" type="password" autocomplete="current-password" bind:value={currentPwd} required />
        </label>

        <label class="field">
          <span class="field__label">New password</span>
          <input class="field__input" type="password" autocomplete="new-password" bind:value={newPwd} required minlength="6" />
        </label>

        <label class="field">
          <span class="field__label">Confirm new password</span>
          <input class="field__input" type="password" autocomplete="new-password" bind:value={confirmPwd} required minlength="6" />
        </label>

        {#if pwdError}<p class="notice notice--err">{pwdError}</p>{/if}
        {#if pwdOk}<p class="notice notice--ok">{pwdOk}</p>{/if}

        <button class="btn btn--ghost" type="submit" disabled={pwdBusy}>
          {#if pwdBusy}
            <span class="spinner spinner--ghost"></span>
            Saving
          {:else}
            Change password
          {/if}
        </button>
      </form>
    </section>
  </div>
</article>

<style>
  .profile { display: grid; gap: 40px; }

  .profile__title {
    font-size: clamp(2.4rem, 5vw, 3.6rem);
    margin: 14px 0 14px;
  }

  .profile__accent {
    background: linear-gradient(120deg, var(--volt) 0%, var(--volt-2) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    font-style: italic;
    font-family: var(--serif);
    font-weight: 400;
  }

  .profile__lede {
    color: var(--fg-2);
    font-size: 1.05rem;
    max-width: 56ch;
    margin: 0;
  }

  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }

  .block {
    padding: 28px;
    background: linear-gradient(180deg, var(--surface) 0%, var(--bg-elev) 100%);
    border: 1px solid var(--line-2);
    border-radius: var(--r-2);
  }

  .block__head {
    display: grid;
    grid-template-columns: auto 1fr;
    grid-template-rows: auto auto;
    column-gap: 12px;
    margin-bottom: 24px;
  }

  .block__num {
    grid-row: 1 / 3;
    align-self: center;
    width: 36px;
    height: 36px;
    display: grid;
    place-items: center;
    border-radius: 8px;
    background: var(--surface-3);
    border: 1px solid var(--line-2);
    color: var(--volt);
    font-family: var(--mono);
    font-size: 0.78rem;
  }

  .block__title {
    font-size: 1.1rem;
    font-weight: 500;
  }

  .block__hint {
    font-family: var(--mono);
    font-size: 0.74rem;
    color: var(--fg-mute);
  }

  .portrait {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 22px;
    align-items: start;
  }

  .portrait__frame {
    width: 130px;
    height: 130px;
    border-radius: var(--r-2);
    border: 1px solid var(--line-2);
    background: var(--surface-2);
    overflow: hidden;
    position: relative;
  }

  .portrait__frame img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .portrait__placeholder {
    display: grid;
    place-items: center;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, var(--volt) 0%, var(--plum) 100%);
    color: var(--bg);
    font-family: var(--sans);
    font-weight: 600;
    font-size: 3rem;
  }

  .portrait__form { display: grid; gap: 12px; }

  .upload { cursor: pointer; }
  .upload__btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    height: 36px;
    padding: 0 14px;
    background: var(--surface);
    border: 1px solid var(--line-3);
    border-radius: var(--r-1);
    font-size: 0.85rem;
    color: var(--fg);
    transition: background 160ms var(--ease), border-color 160ms var(--ease);
    width: max-content;
  }
  .upload:hover .upload__btn {
    background: var(--surface-2);
    border-color: var(--volt);
  }

  .picked {
    margin: 0;
    font-family: var(--mono);
    font-size: 0.78rem;
    color: var(--fg-mute);
  }

  .pwd { display: grid; gap: 16px; }

  .spinner {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    border: 2px solid #0a0a0c40;
    border-top-color: var(--bg);
    animation: spin 700ms linear infinite;
  }
  .spinner--ghost {
    border-color: var(--line-3);
    border-top-color: var(--fg);
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  @media (max-width: 900px) {
    .grid { grid-template-columns: 1fr; }
  }
</style>
