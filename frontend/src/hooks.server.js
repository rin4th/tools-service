import { env } from '$env/dynamic/private';

const BACKEND_URL = env.BACKEND_URL || 'http://backend:8000';

const HOP_BY_HOP = new Set([
  'connection',
  'keep-alive',
  'proxy-authenticate',
  'proxy-authorization',
  'te',
  'trailers',
  'transfer-encoding',
  'upgrade',
  'host',
  'content-length'
]);

function filterHeaders(src) {
  const out = new Headers();
  for (const [k, v] of src.entries()) {
    if (!HOP_BY_HOP.has(k.toLowerCase())) out.set(k, v);
  }
  return out;
}

export async function handle({ event, resolve }) {
  const { pathname, search } = event.url;

  if (pathname.startsWith('/api/')) {
    const target = new URL(pathname + search, BACKEND_URL);
    const method = event.request.method;
    const init = {
      method,
      headers: filterHeaders(event.request.headers),
      redirect: 'manual'
    };
    if (!['GET', 'HEAD'].includes(method)) {
      init.body = await event.request.arrayBuffer();
    }
    const upstream = await fetch(target, init);
    return new Response(upstream.body, {
      status: upstream.status,
      statusText: upstream.statusText,
      headers: filterHeaders(upstream.headers)
    });
  }

  return resolve(event);
}
