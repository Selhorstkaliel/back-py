import { useEffect, useState } from "react";
import { apiFetch } from "../lib/fetch";

export function useUser() {
  const [user, setUser] = useState(null);
  useEffect(() => {
    apiFetch("/api/auth/me").then(res => {
      if (res.ok) return res.json().then(setUser);
    });
  }, []);
  return user;
}