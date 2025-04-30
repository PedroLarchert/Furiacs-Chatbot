"use client"
import { useState, useEffect, useRef } from "react"
import styles from "./page.module.css"
import { Mensagers } from "@/components/mensagers/page"
import { TextBar } from "@/components/textBar/page"
import functions from "@/components/functions"

export function Chat() {
  const [messages, setMessages] = useState<{ text: string; isUser: boolean; time?: string }[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const chatRef = useRef<HTMLDivElement>(null)

  // Scroll to bottom when messages change
  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight
    }
  }, [messages, isLoading])

  const handleSubmit = async (text: string) => {
    // Add user message
    const userMessage = {
      text,
      isUser: true,
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    }

    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    try {
      // Call API to get response
      const response = await functions.submit(text)

      // Add bot response
      const botMessage = {
        text: response,
        isUser: false,
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      }

      setMessages((prev) => [...prev, botMessage])
    } catch (error) {
      console.error("Error getting response:", error)

      // Add error message
      const errorMessage = {
        text: "Sorry, I couldn't process your request. Please try again.",
        isUser: false,
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      }

      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className={styles.chatContainer}>
      <div className={styles.chat} ref={chatRef}>
        {messages.length === 0 ? (
          <div className={styles.emptyState}>
            <h3>Bem-vindo ao FuriaChat</h3>
            <p>
              Digite uma mensagem abaixo para iniciar uma conversa com o chatbot da Furia. Você pode perguntar sobre
              jogos, jogadores,itens da nossa loja, ou qualquer informação relacionada à equipe.
            </p>
          </div>
        ) : (
          messages.map((message, index) => (
            <Mensagers key={index} text={message.text} isUser={message.isUser} time={message.time} />
          ))
        )}
        {isLoading && (
          <div className={styles.loadingContainer}>
            <Mensagers text="..." isUser={false} />
          </div>
        )}
      </div>
      <div className={styles.inputContainer}>
        <TextBar onSubmit={handleSubmit} />
      </div>
    </div>
  )
}
