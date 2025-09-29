"use client";
import { useState, useEffect } from "react";

export default function SupportPage() {
  const [tickets, setTickets] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [file, setFile] = useState(null);

  useEffect(() => {
    fetch(process.env.BASE_API_URL + "/api/tickets", { credentials: "include" })
      .then(res => res.json()).then(setTickets);
  }, []);

  const openTicket = async e => {
    e.preventDefault();
    const data = new FormData();
    data.append("title", title);
    data.append("description", description);
    if (file) data.append("file", file);

    const res = await fetch(process.env.BASE_API_URL + "/api/tickets", {
      method: "POST",
      body: data,
      credentials: "include"
    });
    if (res.ok) {
      alert("Ticket aberto!");
      setTitle(""); setDescription(""); setFile(null);
    }
  };

  return (
    <div className="p-8">
      <h1>Suporte</h1>
      <form onSubmit={openTicket}>
        <input value={title} onChange={e => setTitle(e.target.value)} placeholder="Título" />
        <textarea value={description} onChange={e => setDescription(e.target.value)} placeholder="Descrição" />
        <input type="file" onChange={e => setFile(e.target.files[0])} />
        <button type="submit">Abrir chamado</button>
      </form>
      <h2>Meus Tickets</h2>
      <ul>
        {tickets.map(t => (
          <li key={t.id}>{t.title} - {t.created_at}</li>
        ))}
      </ul>
    </div>
  );
}