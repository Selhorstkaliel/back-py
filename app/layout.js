import "./globals.css";

export default function RootLayout({ children }) {
  return (
    <html lang="pt-BR" className="dark">
      <body className="bg-black text-neon-100">
        {children}
      </body>
    </html>
  );
}