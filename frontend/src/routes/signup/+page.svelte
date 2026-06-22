<script lang="ts">
  let name = $state('');
  let email = $state('');
  let password = $state('');
  let showPassword = $state(false);
  let submitted = $state(false);

  function handleSubmit(e: Event) {
    e.preventDefault();
    submitted = true;
  }
</script>

<div class="page">
  <nav>
    <a href="/" class="nav-logo">AI Student Predictor</a>
    <div class="nav-links">
      <a href="/">Predict</a>
      <a href="/signup" class="active">Sign Up</a>
    </div>
  </nav>

  <div class="card">
    <div class="avatar">
      <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
        <circle cx="12" cy="7" r="4"/>
      </svg>
    </div>

    <h1>Create your account</h1>
    <p class="subtitle">Join us to start predicting student performance</p>

    <form onsubmit={handleSubmit}>
      <div class="input-group">
        <div class="input-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
        </div>
        <input
          type="text"
          bind:value={name}
          placeholder="John Doe"
          required
        />
      </div>

      <div class="input-group">
        <div class="input-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="4" width="20" height="16" rx="2"/>
            <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>
          </svg>
        </div>
        <input
          type="email"
          bind:value={email}
          placeholder="you@example.com"
          required
        />
      </div>

      <div class="input-group">
        <div class="input-icon">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
          </svg>
        </div>
        <input
          type={showPassword ? 'text' : 'password'}
          bind:value={password}
          placeholder="At least 6 characters"
          minlength={6}
          required
        />
        <button type="button" class="eye-btn" onclick={() => showPassword = !showPassword} aria-label="Toggle password visibility">
          {#if showPassword}
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
              <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
              <line x1="1" y1="1" x2="23" y2="23"/>
              <path d="M14.12 14.12a3 3 0 1 1-4.24-4.24"/>
            </svg>
          {:else}
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
              <circle cx="12" cy="12" r="3"/>
            </svg>
          {/if}
        </button>
      </div>

      <button type="submit" class="submit-btn">Create Account</button>
    </form>

    {#if submitted}
      <div class="success">Account created! (demo)</div>
    {/if}

    <p class="footer-text">
      Already have an account? <a href="/signin" class="link">Sign in</a>
    </p>
  </div>
</div>

<style>
  nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 420px;
    width: 100%;
    margin-bottom: 16px;
  }
  .nav-logo {
    font-weight: 700;
    font-size: 15px;
    background: linear-gradient(135deg, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-decoration: none;
  }
  .nav-links { display: flex; gap: 16px; }
  .nav-links a {
    color: #94a3b8;
    text-decoration: none;
    font-size: 13px;
    transition: color 0.15s;
  }
  .nav-links a:hover, .nav-links a.active { color: #a78bfa; }
  .page {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, #0f0a1e 0%, #1a0f2e 50%, #0f0a1e 100%);
    padding: 20px;
  }

  .card {
    background: #1e1236;
    border: 1px solid #2d1b4e;
    border-radius: 20px;
    padding: 48px 40px 36px;
    max-width: 420px;
    width: 100%;
    box-shadow: 0 25px 60px rgba(0,0,0,0.5);
  }

  .avatar {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7c3aed, #ec4899);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 24px;
    box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
  }

  h1 {
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    color: #f1f5f9;
    margin-bottom: 6px;
  }

  .subtitle {
    text-align: center;
    font-size: 14px;
    color: #94a3b8;
    margin-bottom: 32px;
  }

  form {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }

  .input-group {
    position: relative;
    display: flex;
    align-items: center;
  }

  .input-icon {
    position: absolute;
    left: 14px;
    color: #64748b;
    pointer-events: none;
    display: flex;
  }

  .input-group input {
    width: 100%;
    padding: 13px 14px 13px 44px;
    border: 1px solid #2d1b4e;
    border-radius: 12px;
    background: #140a26;
    color: #e2e8f0;
    font-size: 14px;
    transition: border-color 0.2s;
    outline: none;
  }

  .input-group input:focus {
    border-color: #7c3aed;
  }

  .input-group input::placeholder {
    color: #475569;
  }

  .eye-btn {
    position: absolute;
    right: 12px;
    background: none;
    border: none;
    color: #64748b;
    cursor: pointer;
    padding: 4px;
    display: flex;
    transition: color 0.15s;
  }

  .eye-btn:hover {
    color: #94a3b8;
  }

  .submit-btn {
    width: 100%;
    padding: 14px;
    border: none;
    border-radius: 12px;
    background: linear-gradient(135deg, #7c3aed, #ec4899);
    color: white;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: opacity 0.2s, transform 0.1s;
    margin-top: 6px;
  }

  .submit-btn:hover {
    opacity: 0.92;
  }

  .submit-btn:active {
    transform: scale(0.98);
  }

  .success {
    margin-top: 16px;
    padding: 10px;
    border-radius: 8px;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #6ee7b7;
    font-size: 13px;
    text-align: center;
  }

  .footer-text {
    text-align: center;
    font-size: 13px;
    color: #94a3b8;
    margin-top: 24px;
  }

  .link {
    color: #a78bfa;
    text-decoration: none;
    font-weight: 500;
  }

  .link:hover {
    text-decoration: underline;
  }
</style>
