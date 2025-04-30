"use client"

import Image from "next/image"
import styles from "./page.module.css"
import ReactMarkdown from "react-markdown"

interface MensagersProps {
  text: string
  isUser: boolean
  time?: string
}

export function Mensagers({ text, isUser, time }: MensagersProps) {
  return (
    <section className={`${styles.mensagers} ${isUser ? styles.right : styles.left}`}>
      <div>
        <Image
          src={isUser ? "/images/imageMyProfile.svg" : "/images/ImageFuria.svg"}
          width={40}
          height={40}
          alt={isUser ? "My profile image" : "Furia image"}
        />
      </div>
      <div className={styles.text}>
        {!isUser && <h2>Furia</h2>}
        <div className={styles.messageContent}>
          {text === "..." ? (
            <div className={styles.loadingDots}>
              <div className={styles.dot}></div>
              <div className={styles.dot}></div>
              <div className={styles.dot}></div>
            </div>
          ) : (
            <ReactMarkdown>{text}</ReactMarkdown>
          )}
          {time && <div className={styles.messageTime}>{time}</div>}
        </div>
      </div>
    </section>
  )
}
