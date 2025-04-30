"use client"
import { useState, useEffect } from "react"
import styles from "./page.module.css"
import { Chat } from "@/components/chat/page"
import { Agenda } from "@/components/agenda/page"
import { Social } from "@/components/social/page"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { useMobile } from "@/hooks/use-mobile"

export default function Home() {
  const [leftSidebarOpen, setLeftSidebarOpen] = useState(true)
  const [rightSidebarOpen, setRightSidebarOpen] = useState(true)
  const isMobile = useMobile(768)
  const isTablet = useMobile(1024)

  // Set initial sidebar states based on screen size
  useEffect(() => {
    if (isMobile) {
      setLeftSidebarOpen(false)
      setRightSidebarOpen(false)
    } else if (isTablet) {
      setRightSidebarOpen(false)
    } else {
      setLeftSidebarOpen(true)
      setRightSidebarOpen(true)
    }
  }, [isMobile, isTablet])

  const toggleLeftSidebar = () => {
    setLeftSidebarOpen(!leftSidebarOpen)
  }

  const toggleRightSidebar = () => {
    setRightSidebarOpen(!rightSidebarOpen)
  }

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        {/* Left Sidebar */}
        <div className={`${styles.sidebar} ${styles.leftSidebar} ${!leftSidebarOpen ? styles.sidebarHidden : ""}`}>
          <div className={styles.sidebarHeader}>
            <h2>Agenda de Jogos</h2>
            {isMobile && (
              <button className={styles.mobileToggle} onClick={toggleLeftSidebar} aria-label="Close agenda">
                <ChevronLeft />
              </button>
            )}
          </div>
          <Agenda />
        </div>

        {/* Left Sidebar Toggle Button (Mobile Only) */}
        {isMobile && !leftSidebarOpen && (
          <button
            className={`${styles.toggleButton} ${styles.leftToggle}`}
            onClick={toggleLeftSidebar}
            aria-label="Open agenda"
          >
            <ChevronRight />
          </button>
        )}

        {/* Main Chat Area */}
        <div className={styles.chatContainer}>
          <Chat />
        </div>

        {/* Right Sidebar */}
        <div className={`${styles.sidebar} ${styles.rightSidebar} ${!rightSidebarOpen ? styles.sidebarHidden : ""}`}>
          <div className={styles.sidebarHeader}>
            <h2>Nossas redes sociais</h2>
            {isMobile && (
              <button className={styles.mobileToggle} onClick={toggleRightSidebar} aria-label="Close social">
                <ChevronRight />
              </button>
            )}
          </div>
          <Social />
        </div>

        {/* Right Sidebar Toggle Button (Mobile Only) */}
        {isMobile && !rightSidebarOpen && (
          <button
            className={`${styles.toggleButton} ${styles.rightToggle}`}
            onClick={toggleRightSidebar}
            aria-label="Open social"
          >
            <ChevronLeft />
          </button>
        )}
      </div>
    </main>
  )
}
