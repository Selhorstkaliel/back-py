export async function apiFetch(path, opts = {}) {
  return fetch(`${process.env.BASE_API_URL}${path}`, {
    credentials: "include",
    ...opts,
  });
}