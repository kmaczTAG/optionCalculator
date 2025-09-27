import axios from 'axios';

// Axios instance automatically points to the proxied /api path
export const api = axios.create({
  baseURL: '/api',
});

/**
 * Calls the backend hello endpoint.
 * @param {string} name
 * @returns {Promise<string>} greeting text
 */
export async function getGreeting(name) {
  const resp = await api.post('/hello', { name });
  return resp.data.greeting;
}