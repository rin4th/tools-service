import { browser } from '$app/environment';
import { writable, get } from 'svelte/store';

const TOKEN_KEY = 'tools.token';

function readToken() {
  if (!browser) return null;
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

export const token = writable(readToken());
export const user = writable(null);

token.subscribe((v) => {
  if (!browser) return;
  try {
    if (v) localStorage.setItem(TOKEN_KEY, v);
    else localStorage.removeItem(TOKEN_KEY);
  } catch {}
});

export function setToken(value) {
  token.set(value);
}

export function logout() {
  token.set(null);
  user.set(null);
}

export function getToken() {
  return get(token);
}
