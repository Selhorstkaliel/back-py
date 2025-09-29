import Link from "next/link";
import { headers } from "next/headers";
import { redirect } from "next/navigation";

function resolveAuthEndpoint() {
  const baseUrl =
    process.env.BASE_API_URL ??
    process.env.NEXT_PUBLIC_BASE_API_URL ??
    process.env.NEXT_PUBLIC_BASE_URL ??
    "";

  if (!baseUrl) {
    return "/api/auth/me";
  }

  return `${baseUrl.replace(/\/$/, "")}/api/auth/me`;
}

async function hasValidSession(cookieHeader) {
  const endpoint = resolveAuthEndpoint();

  try {
    const response = await fetch(endpoint, {
      headers: cookieHeader ? { cookie: cookieHeader } : {},
      credentials: "include",
      cache: "no-store",
    });

    return response.ok;
  } catch (error) {
    return false;
  }
}

export default async function HomePage() {
  const cookieHeader = headers().get("cookie") ?? "";

  if (await hasValidSession(cookieHeader)) {
    redirect("/protected/dashboard");
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-8 bg-zinc-950 px-4 text-center text-zinc-100">
      <div className="max-w-xl space-y-4">
        <h1 className="text-4xl font-bold text-neon-500">Back Office</h1>
        <p className="text-lg text-zinc-300">
          Gerencie seus dados com segurança e praticidade. Faça login para
          acessar o painel administrativo.
        </p>
      </div>
      <Link
        href="/auth/login"
        className="rounded bg-neon-500 px-6 py-3 text-lg font-semibold text-zinc-950 transition hover:bg-neon-400"
      >
        Acessar painel
      </Link>
    </main>
  );
}
