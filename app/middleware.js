import { NextResponse } from "next/server";

export async function middleware(req) {
  // Protege rotas /protected/*
  if (req.nextUrl.pathname.startsWith("/protected")) {
    const res = await fetch(
      process.env.BASE_API_URL + "/api/auth/me",
      {
        credentials: "include",
        headers: { cookie: req.headers.get("cookie") || "" },
      }
    );
    if (res.status !== 200) {
      return NextResponse.redirect(new URL("/auth/login", req.url));
    }
  }
  return NextResponse.next();
}