export interface QuestionOption {
  id: string
  text: string
}

export interface Question {
  id: number
  question: string
  options: QuestionOption[]
  correctAnswer: string
  explanation: string
  domain: string
  difficulty: "Easy" | "Medium" | "Hard"
}
