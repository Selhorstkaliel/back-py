"use client";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useState } from "react";

const schema = z.object({
  tipo: z.enum(["limpeza", "rating"]),
  doc: z.string(),
  nome: z.string(),
  telefone: z.string(),
  vendedor: z.string(),
  valor: z.number(),
  aceitoTermos: z.literal(true)
});

export default function CadastroPage() {
  const { register, handleSubmit, setValue, watch, formState: { errors } } = useForm({
    resolver: zodResolver(schema)
  });
  const [file, setFile] = useState(null);
  const [contratoUrl, setContratoUrl] = useState("");

  const onSubmit = async (data) => {
    const formData = new FormData();
    Object.keys(data).forEach(k => formData.append(k, data[k]));
    if (file) formData.append("file", file);
    const res = await fetch(process.env.BASE_API_URL + "/api/entries", {
      method: "POST",
      body: formData,
      credentials: "include"
    });
    if (res.ok) {
      const json = await res.json();
      setContratoUrl(json.contratoUrl);
      alert("Cadastro realizado!");
    } else {
      alert("Erro no cadastro");
    }
  };

  return (
    <form className="p-8" onSubmit={handleSubmit(onSubmit)}>
      <select {...register("tipo")}>
        <option value="limpeza">Limpeza</option>
        <option value="rating">Rating</option>
      </select>
      <input {...register("doc")} placeholder="CPF/CNPJ" />
      <input {...register("nome")} placeholder="Nome" />
      <input {...register("telefone")} placeholder="Telefone" />
      <input {...register("vendedor")} placeholder="Vendedor" />
      <input {...register("valor")} placeholder="Valor" type="number" />
      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <label>
        <input type="checkbox" {...register("aceitoTermos")} /> Aceito os Termos
      </label>
      {errors.aceitoTermos && <span>Obrigatório aceitar os termos</span>}
      <button type="submit">Cadastrar</button>
      {contratoUrl && (
        <a href={contratoUrl} target="_blank" rel="noopener noreferrer">Baixar Contrato PDF</a>
      )}
    </form>
  );
}