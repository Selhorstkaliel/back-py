"use client";
import { useEffect, useState } from "react";
import { Chart } from "react-chartjs-2";

export default function DashboardPage() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetch(process.env.BASE_API_URL + "/api/stats", { credentials: "include" })
      .then(res => res.json()).then(setStats);
  }, []);

  if (!stats) return <div>Carregando...</div>;
  return (
    <div className="p-8">
      <h1 className="text-2xl mb-4">Dashboard</h1>
      <div className="grid grid-cols-2 gap-4">
        <div>KPI Bruto: R$ {stats.bruto}</div>
        <div>KPI Líquido: R$ {stats.liquido}</div>
        <div>Limpezas: {stats.limpezasCount}</div>
        <div>Ratings: {stats.ratingCount}</div>
      </div>
      {/* Gráficos: implemente usando Chart.js conforme necessário */}
    </div>
  );
}