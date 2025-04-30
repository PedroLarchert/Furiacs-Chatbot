"use client"

import { useState, useEffect } from "react"
import axios from "axios"
import styles from "./page.module.css"

interface Game {
  evento: string
  data: string
  time1: string
  score1: string
  time2: string
  score2: string
}

export function Agenda() {
  const [futureGames, setFutureGames] = useState<Game[]>([])
  const [pastGames, setPastGames] = useState<Game[]>([])

  useEffect(() => {
    async function fetchGames() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/matches")

        if (response.data && Array.isArray(response.data.passados) && Array.isArray(response.data.futuros)) {
          setPastGames(response.data.passados)
          setFutureGames(response.data.futuros)
        } else {
          console.warn("Resposta inesperada da API:", response.data)
          setPastGames([])
          setFutureGames([])
        }
      } catch (error) {
        console.log("Erro na API, usando mock")
        const mockGames: Game[] = [
          {
            evento: "Campeonato Nacional",
            data: "--/--/----",
            time1: "Furia",
            score1: "-",
            time2: "Adversário",
            score2: "-",
          },
        ]
        setPastGames(mockGames)
        setFutureGames([])
      }
    }

    fetchGames()
  }, [])

  return (
    <div className={styles.agendaContent}>
      <div className={styles.section}>
        <h3 className={styles.subtitle}>Jogos Futuros:</h3>
        <ul className={styles.list}>
          {futureGames.length > 0 ? (
            futureGames.map((game, index) => (
              <li key={index} className={styles.listItem}>
                {game.data} - {game.time1} vs {game.time2}
              </li>
            ))
          ) : (
            <li className={styles.listItem}>Nenhum jogo futuro agendado</li>
          )}
        </ul>
      </div>

      <div className={styles.section}>
        <h3 className={styles.subtitle}>Jogos Passados:</h3>
        <ul className={styles.list}>
          {pastGames.length > 0 ? (
            pastGames.map((game, index) => (
              <li key={index} className={styles.listItem}>
                {game.data} - {game.time1} {game.score1} x {game.score2} {game.time2}
              </li>
            ))
          ) : (
            <li className={styles.listItem}>Nenhum jogo passado registrado</li>
          )}
        </ul>
      </div>
    </div>
  )
}
