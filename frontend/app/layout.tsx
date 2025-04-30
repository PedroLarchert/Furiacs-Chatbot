import type React from "react"
import type { Metadata } from "next"
import { Inter, Exo, Montserrat } from "next/font/google"
import "./globals.css"
import { Header } from "@/components/header/page"

// Load fonts using Next.js font optimization
const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
})

const exo = Exo({
  subsets: ["latin"],
  variable: "--font-exo",
  display: "swap",
  weight: ["100", "200", "300", "400", "500", "600", "700", "800", "900"],
})

const montserrat = Montserrat({
  subsets: ["latin"],
  variable: "--font-montserrat",
  display: "swap",
  weight: ["100", "200", "300", "400", "500", "600", "700", "800", "900"],
})

export const metadata: Metadata = {
  title: "Furiachat",
  description: "Chatbot Furia Counter Strike",
  icons: {
    icon: "/favicon.svg",
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="pt-BR" className={`${inter.variable} ${exo.variable} ${montserrat.variable}`}>
      <head>
        <link rel="stylesheet" href="/twitter-embed-override.css" />
      </head>      
      <body className={inter.className} style={{ margin: 0, padding: 0 }}>
        <Header />
        {children}
      </body>
    </html>
  )
}
