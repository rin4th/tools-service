<script>
  import { goto } from '$app/navigation';
  import { setToken } from '$lib/auth.js';
  import { login } from '$lib/profile.js';
  import { fetchMe } from '$lib/profile.js';

  let username = $state('');
  let password = $state('');
  let loading = $state(false);
  let error = $state('');

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

<section class="login">
  <div class="login__col login__col--lead">
    <p class="eyebrow rise rise-1">§ Folio &mdash; Sign in</p>
    <h1 class="display rise rise-2">
      Take a<br /><em>seat</em>.
    </h1>
    <p class="lede rise rise-3">
      The studio is members-only &mdash; we keep a small ledger so that your
      uploads stay yours alone. Sign in with the credentials given to you by
      the keeper of the workshop.
    </p>
    <div class="meta rise rise-4">
      <span class="eyebrow">Forgot the key?</span>
      <p>
        There is no public registration. Your operator can issue or reset a
        password from the command line.
      </p>
    </div>
  </div>

  <div class="login__col login__col--form">
    <form class="form rise rise-3" onsubmit={onSubmit} novalidate>
      <header class="form__head">
        <span class="section-num">No. 01</span>
        <h2 class="form__title">Credentials.</h2>
      </header>

      <label class="field">
        <span class="field__label">Username</span>
        <input
          class="field__input"
          type="text"
          autocomplete="username"
          bind:value={username}
          placeholder="e.g. atelier"
          required
          minlength="3"
          maxlength="64"
        />
      </label>

      <label class="field">
        <span class="field__label">Password</span>
        <input
          class="field__input"
          type="password"
          autocomplete="current-password"
          bind:value={password}
          placeholder="••••••••"
          required
          minlength="6"
        />
      </label>

      {#if error}
        <p class="notice notice--err">{error}</p>
      {/if}

      <div class="form__foot">
        <button class="btn btn--accent" type="submit" disabled={loading}>
          {loading ? 'Verifying…' : 'Enter the studio'}
          <span aria-hidden="true">&rarr;</span>
        </button>
        <a class="lnk" href="/">&larr; Back</a>
      </div>
    </form>

    <ol class="ledger rise rise-5" aria-hidden="true">
      <li><span class="ledger__num">i.</span> JWT token, 60 minutes.</li>
      <li><span class="ledger__num">ii.</span> Stored locally — yours to clear.</li>
      <li><span class="ledger__num">iii.</span> Sent only to /api/* on this host.</li>
    </ol>
  </div>
</section>

<style>
  .login {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: clamp(24px, 6vw, 96px);
    align-items: start;
    padding: 32px 0 32px;
  }

  .login__col--lead { max-width: 540px; }

  .display {
    margin-top: 24px;
    font-size: clamp(3.5rem, 8vw, 6.4rem);
  }

  .display em {
    font-style: italic;
    color: var(--accent);
    font-variation-settings: 'opsz' 144, 'SOFT' 100;
  }

  .lede {
    margin-top: 28px;
    font-family: var(--serif);
    font-size: 1.1rem;
    line-height: 1.55;
    color: var(--ink-2);
    max-width: 46ch;
  }

  .meta {
    margin-top: 36px;
    padding-top: 18px;
    border-top: 1px solid var(--rule-strong);
    max-width: 46ch;
  }

  .meta p {
    font-family: var(--serif);
    font-style: italic;
    margin: 6px 0 0;
    color: var(--ink-mute);
  }

  .form {
    background: var(--paper-2);
    border: 1px solid var(--rule-strong);
    padding: clamp(28px, 4vw, 44px);
    box-shadow: var(--shadow-lift);
    display: grid;
    gap: 28px;
  }

  .form__head { display: grid; gap: 6px; }
  .form__title {
    font-family: var(--serif);
    font-size: 1.6rem;
    margin: 0;
  }

  .form__foot {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
    margin-top: 4px;
  }

  .lnk {
    font-family: var(--mono);
    font-size: 0.74rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--ink-mute);
  }

  .ledger {
    margin: 24px 0 0;
    padding: 0;
    list-style: none;
    display: grid;
    gap: 4px;
  }
  .ledger li {
    font-family: var(--mono);
    font-size: 0.72rem;
    letter-spacing: 0.06em;
    color: var(--ink-mute);
  }
  .ledger__num { color: var(--accent); margin-right: 6px; }

  @media (max-width: 900px) {
    .login { grid-template-columns: 1fr; }
  }
</style>
