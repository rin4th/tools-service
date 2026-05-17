import { getToken, logout } from './auth.js';

export class ApiError extends Error {
  constructor(message, status, body) {
    super(message);
    this.status = status;
    this.body = body;
  }
}

async function parseError(res) {
  let body = null;
  try {
    body = await res.json();
  } catch {}
  const detail = body?.detail;
  const message =
    typeof detail === 'string'
      ? detail
      : Array.isArray(detail) && detail[0]?.msg
        ? detail[0].msg
        : `Request failed (${res.status})`;
  return new ApiError(message, res.status, body);
}

function authHeaders(extra = {}) {
  const t = getToken();
  return t ? { ...extra, Authorization: `Bearer ${t}` } : extra;
}

export async function apiJson(path, { method = 'GET', body, auth = true } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  const res = await fetch(path, {
    method,
    headers: auth ? authHeaders(headers) : headers,
    body: body ? JSON.stringify(body) : undefined
  });
  if (res.status === 401 && auth) logout();
  if (!res.ok) throw await parseError(res);
  if (res.status === 204) return null;
  return res.json();
}

export async function apiForm(path, formData, { method = 'POST', auth = true } = {}) {
  const res = await fetch(path, {
    method,
    headers: auth ? authHeaders() : {},
    body: formData
  });
  if (res.status === 401 && auth) logout();
  if (!res.ok) throw await parseError(res);
  return res;
}

export async function apiBlob(path, formData, opts = {}) {
  const res = await apiForm(path, formData, opts);
  const blob = await res.blob();
  const cd = res.headers.get('content-disposition') || '';
  const match = /filename="?([^";]+)"?/i.exec(cd);
  const filename = match?.[1] || 'download.pdf';
  return { blob, filename };
}

export function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
