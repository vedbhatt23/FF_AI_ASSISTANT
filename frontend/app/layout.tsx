import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Insights Assistant | Entertainment Analytics",
  description: "Secure, multi-source AI analytics assistant for business intelligence.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body>{children}</body>
    </html>
  );
}
