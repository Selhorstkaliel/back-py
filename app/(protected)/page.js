"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function ProtectedHome() {
  const router = useRouter();
  useEffect(() => { router.replace("/protected/dashboard"); }, []);
  return null;
}