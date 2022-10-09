export const BACKEND_URL = process.env.VUE_APP_BACKEND_URL;

if (!BACKEND_URL) {
  throw new Error('VUE_APP_BACKEND_URL is undefined');
}
