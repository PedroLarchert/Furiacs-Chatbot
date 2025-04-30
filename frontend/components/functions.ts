import axios from "axios"

class functions {
  public static async submit(text: string) {
    try {
      const response = await this.sendBack(text)

      // Handle the response format - expecting a simple string
      if (typeof response === "string") {
        return response
      } else if (response && typeof response === "object") {
        // If it's an object with a result property
        return response.reply || "Não foi possível processar a resposta."
      }

      return "Resposta recebida em formato desconhecido."
    } catch (error) {
      console.error("Error in submit function:", error)
      return "Ocorreu um erro ao processar sua mensagem. Por favor, tente novamente."
    }
  }

  private static async sendBack(text: string) {
    try {
      const response = await axios.post("http://127.0.0.1:8000/chatresponse", {
        text: text,
      })

      // Return the data directly, the calling function will handle formatting
      return response.data
    } catch (error: any) {
      console.error("Error in API call:", error)
      if (error.response) {
        console.error("Response data:", error.response.data)
        console.error("Response status:", error.response.status)
      }
      return "Aconteceu um erro ao conectar com o servidor."
    }
  }
}

export default functions
