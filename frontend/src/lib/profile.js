import { apiJson } from './api.js';
import { user } from './auth.js';

export async function fetchMe() {
  const me = await apiJson('/api/profile/me');
  user.set(me);
  return me;
}

export async function login(username, password) {
  const res = await apiJson('/api/auth/login', {
    method: 'POST',
    body: { username, password },
    auth: false
  });
  return res;
}

export async function changePassword(current_password, new_password) {
  return apiJson('/api/profile/change-password', {
    method: 'POST',
    body: { current_password, new_password }
  });
}
