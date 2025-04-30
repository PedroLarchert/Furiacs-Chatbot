"use client"
import { useState, useRef, useEffect } from "react"
import type React from "react"

import styles from "./page.module.css"

interface TextBarProps {
  onSubmit?: (text: string) => void
}

export function TextBar({ onSubmit }: TextBarProps = {}) {
  const [text, setText] = useState<string>("")
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleSubmit = () => {
    if (text.trim() && onSubmit) {
      onSubmit(text.trim())
      setText("")
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  // Auto-resize textarea based on content
  useEffect(() => {
    const textarea = textareaRef.current
    if (textarea) {
      textarea.style.height = "auto"
      const newHeight = Math.min(textarea.scrollHeight, 100)
      textarea.style.height = `${newHeight}px`
    }
  }, [text])

  return (
    <div className={styles.textBar}>
      <div className={styles.textBarUpper}>
        <textarea
          ref={textareaRef}
          className={styles.inputTextBar}
          placeholder="Digite aqui"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
        />
        <div className={styles.imageButton} onClick={handleSubmit}>
          <svg width="24" height="24" viewBox="0 0 40 41" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
              d="M2.44354 6.57528C2.44354 7.14121 3.40127 10.2321 4.48961 13.4536L6.53568 19.3306L22.2077 19.4612C30.8273 19.5047 37.6621 19.3741 37.4444 19.2C37.1832 18.9823 34.963 18.0246 32.4381 17.0233C23.7749 13.6712 10.889 8.57781 7.14515 7.09768C2.70474 5.35634 2.40001 5.31281 2.44354 6.57528Z"
              fill="white"
            />
            <path
              d="M6.318 22.3779C5.4038 24.8157 2.39999 34.219 2.39999 34.6978C2.39999 35.7862 3.00946 35.5685 22.8607 27.5148C27.3011 25.7299 32.3945 23.6839 34.1794 22.9438C35.9643 22.2037 37.5315 21.5507 37.6185 21.4637C37.7056 21.3766 30.8273 21.2895 22.2512 21.2895H6.75334L6.318 22.3779Z"
              fill="white"
            />
          </svg>
        </div>
      </div>
      <div className={styles.textBarDown}>
        <p className={styles.pTextBarDown}>Projeto de Chatbot para processo seletivo da @furiagg</p>
        <p className={styles.pTextBarDown}>Por Favor envie uma mensagem por vez!</p>
      </div>
    </div>
  )
}
