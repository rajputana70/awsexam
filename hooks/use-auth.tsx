"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"

interface User {
  id: string
  name: string
  email: string
  createdAt: Date
  examHistory: ExamResult[]
  preferences: UserPreferences
}

interface ExamResult {
  id: string
  examType: string
  score: number
  totalQuestions: number
  timeSpent: number
  completedAt: Date
  domainScores: Record<string, number>
}

interface UserPreferences {
  theme: "light" | "dark"
  notifications: boolean
  studyReminders: boolean
}

interface AuthContextType {
  user: User | null
  loading: boolean
  signIn: (email: string, password: string) => Promise<void>
  signUp: (name: string, email: string, password: string) => Promise<void>
  signOut: () => void
  updateUser: (updates: Partial<User>) => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate checking for existing session
    const savedUser = localStorage.getItem("aws-exam-user")
    if (savedUser) {
      setUser(JSON.parse(savedUser))
    }
    setLoading(false)
  }, [])

  const signIn = async (email: string, password: string) => {
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000))

    const mockUser: User = {
      id: "1",
      name: "John Doe",
      email,
      createdAt: new Date(),
      examHistory: [
        {
          id: "1",
          examType: "SAA-C03",
          score: 85,
          totalQuestions: 100,
          timeSpent: 7200,
          completedAt: new Date(Date.now() - 86400000),
          domainScores: {
            "Design Resilient Architectures": 90,
            "Design High-Performing Architectures": 85,
            "Design Secure Applications": 80,
            "Design Cost-Optimized Architectures": 85,
          },
        },
      ],
      preferences: {
        theme: "light",
        notifications: true,
        studyReminders: true,
      },
    }

    setUser(mockUser)
    localStorage.setItem("aws-exam-user", JSON.stringify(mockUser))
  }

  const signUp = async (name: string, email: string, password: string) => {
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000))

    const mockUser: User = {
      id: "1",
      name,
      email,
      createdAt: new Date(),
      examHistory: [],
      preferences: {
        theme: "light",
        notifications: true,
        studyReminders: true,
      },
    }

    setUser(mockUser)
    localStorage.setItem("aws-exam-user", JSON.stringify(mockUser))
  }

  const signOut = () => {
    setUser(null)
    localStorage.removeItem("aws-exam-user")
  }

  const updateUser = (updates: Partial<User>) => {
    if (user) {
      const updatedUser = { ...user, ...updates }
      setUser(updatedUser)
      localStorage.setItem("aws-exam-user", JSON.stringify(updatedUser))
    }
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        signIn,
        signUp,
        signOut,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
