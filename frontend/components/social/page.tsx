"use client"

import { useState, useEffect } from "react"
import axios from "axios"
import styles from "./page.module.css"
import { Twitter, Instagram, Facebook, Youtube, Twitch } from "lucide-react"
import { TwitterTweetEmbed } from "react-twitter-embed"

interface Tweet {
  id: string
  url: string
}

export function Social() {
  const [tweets, setTweets] = useState<Tweet[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchTweets() {
      try {
        setLoading(true)
        const response = await axios.get<Tweet[]>("http://127.0.0.1:8000/tweets")
        setTweets(response.data)
        setError(null)
      } catch (err) {
        console.error("Erro ao buscar tweets:", err)
        setError("Falha ao carregar os tweets. Tente novamente mais tarde.")
        // Dados mock para fallback
        setTweets([
          {
            id: "1647248589191000064",
            url: "https://twitter.com/Example/status/1647248589191000064"
          }
        ])
      } finally {
        setLoading(false)
      }
    }

    fetchTweets()
  }, [])

  return (
    <div className={styles.socialContent}>
      <div className={styles.section}>
        <div className={styles.socialIcons}>
          <a href="https://twitter.com/FURIA" target="_blank" rel="noopener noreferrer" className={styles.socialIcon}>
            <Twitter size={24} />
          </a>
          <a href="https://www.instagram.com/furiagg/" target="_blank" rel="noopener noreferrer" className={styles.socialIcon}>
            <Instagram size={24} />
          </a>
          <a href="https://www.facebook.com/furiagg" target="_blank" rel="noopener noreferrer" className={styles.socialIcon}>
            <Facebook size={24} />
          </a>
          <a href="https://www.youtube.com/furiagg" target="_blank" rel="noopener noreferrer" className={styles.socialIcon}>
            <Youtube size={24} />
          </a>
          <a href="https://www.twitch.tv/furiatv" target="_blank" rel="noopener noreferrer" className={styles.socialIcon}>
            <Twitch size={24} />
          </a>
        </div>
      </div>

      <h2 className={styles.title}>Últimas publicações no X</h2>

      <div className={styles.tweetsContainer}>
        {loading ? (
          <div className={styles.loading}>Carregando tweets...</div>
        ) : error ? (
          <div className={styles.error}>{error}</div>
        ) : tweets.length > 0 ? (
          tweets.map((tweet) => (
            <div key={tweet.id} className={styles.tweetWrapper}>
              <TwitterTweetEmbed
                  tweetId={tweet.id}
                  options={{
                    width: "100%",
                    align: "center",
                    conversation: "none", // Hide conversation
                    cards: "hidden", // Hide cards
                    theme: "dark",
                    dnt: true,
                  }}
                />
            </div>
          ))
        ) : (
          <div className={styles.noTweets}>Nenhum tweet disponível</div>
        )}
      </div>
    </div>
  )
}
