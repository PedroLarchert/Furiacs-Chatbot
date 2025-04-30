import styles from "./page.module.css"
import Image from "next/image"

export function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.logo}>
        <Image src="/images/ImageFuria.svg" width={40} height={40} alt="Furia Logo" />
        <h1 className={styles.h1Header}>FuriaCS</h1>
      </div>
    </header>
  )
}
