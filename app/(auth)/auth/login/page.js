"use client";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useRouter } from "next/navigation";

const schema = z.object({
  username: z.string().min(3),
  password: z.string().min(4),
});

export default function LoginPage() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema)
  });
  const router = useRouter();

  const onSubmit = async (data) => {
    const res = await fetch(process.env.BASE_API_URL + "/api/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
      credentials: "include",
      headers: { "Content-Type": "application/json" },
    });
    if (res.ok) {
      router.push("/protected/dashboard");
    } else {
      alert("Login inválido");
    }
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-screen">
      <form className="bg-zinc-900 p-8 rounded shadow-md flex flex-col gap-4" onSubmit={handleSubmit(onSubmit)}>
        <h1 className="text-neon-500 text-3xl font-bold mb-4">Login</h1>
        <input {...register("username")} placeholder="Usuário" className="input" />
        {errors.username && <span>{errors.username.message}</span>}
        <input {...register("password")} type="password" placeholder="Senha" className="input" />
        {errors.password && <span>{errors.password.message}</span>}
        <button type="submit" className="bg-neon-500 py-2 rounded">Entrar</button>
      </form>
    </main>
  );
}