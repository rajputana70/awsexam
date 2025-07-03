"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { Clock, ChevronLeft, ChevronRight, Flag, CheckCircle, ArrowLeft } from "lucide-react"
import type { Question } from "@/types/question"
import ExamResults from "@/components/exam-results"

interface ExamInterfaceProps {
  questions: Question[]
  examType: string
  onExit: () => void
}

export default function ExamInterface({ questions, examType, onExit }: ExamInterfaceProps) {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<Record<number, string>>({})
  const [timeRemaining, setTimeRemaining] = useState(130 * 60) // 130 minutes in seconds
  const [examCompleted, setExamCompleted] = useState(false)
  const [flaggedQuestions, setFlaggedQuestions] = useState<Set<number>>(new Set())

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeRemaining((prev) => {
        if (prev <= 1) {
          setExamCompleted(true)
          return 0
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = seconds % 60
    return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`
  }

  const handleAnswerChange = (value: string) => {
    setAnswers({ ...answers, [currentQuestion]: value })
  }

  const toggleFlag = () => {
    const newFlagged = new Set(flaggedQuestions)
    if (newFlagged.has(currentQuestion)) {
      newFlagged.delete(currentQuestion)
    } else {
      newFlagged.add(currentQuestion)
    }
    setFlaggedQuestions(newFlagged)
  }

  const progress = ((currentQuestion + 1) / questions.length) * 100
  const answeredCount = Object.keys(answers).length

  if (examCompleted) {
    return (
      <ExamResults
        examType={examType}
        questions={questions}
        answers={answers}
        timeSpent={130 * 60 - timeRemaining}
        onRetake={() => {
          setCurrentQuestion(0)
          setAnswers({})
          setTimeRemaining(130 * 60)
          setExamCompleted(false)
          setFlaggedQuestions(new Set())
        }}
        onExit={onExit}
      />
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white shadow-lg sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <Button variant="ghost" onClick={onExit} className="text-white hover:bg-white/10">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Exit Exam
              </Button>
              <div className="border-l border-white/20 pl-4">
                <h1 className="text-xl font-bold">{examType} Practice Exam</h1>
                <Badge variant="secondary" className="bg-white/20 text-white mt-1">
                  Question {currentQuestion + 1} of {questions.length}
                </Badge>
              </div>
            </div>
            <div className="flex items-center space-x-6">
              <div className="flex items-center space-x-2">
                <Clock className="w-5 h-5" />
                <span className="font-mono text-lg">{formatTime(timeRemaining)}</span>
              </div>
              <div className="text-sm">
                Answered: {answeredCount}/{questions.length}
              </div>
            </div>
          </div>
          <div className="mt-3">
            <Progress value={progress} className="h-2 bg-white/20" />
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Question Navigation Sidebar */}
          <div className="lg:col-span-1">
            <Card className="border-0 shadow-xl bg-white/80 backdrop-blur-sm sticky top-24">
              <CardHeader>
                <CardTitle className="text-lg">Question Navigator</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-5 gap-2 mb-4">
                  {questions.map((_, index) => (
                    <Button
                      key={index}
                      variant={currentQuestion === index ? "default" : "outline"}
                      size="sm"
                      className={`relative ${
                        answers[index]
                          ? "bg-green-100 border-green-300 text-green-800 hover:bg-green-200"
                          : flaggedQuestions.has(index)
                            ? "bg-yellow-100 border-yellow-300 text-yellow-800 hover:bg-yellow-200"
                            : ""
                      }`}
                      onClick={() => setCurrentQuestion(index)}
                    >
                      {index + 1}
                      {answers[index] && <CheckCircle className="w-3 h-3 absolute -top-1 -right-1 text-green-600" />}
                      {flaggedQuestions.has(index) && (
                        <Flag className="w-3 h-3 absolute -top-1 -right-1 text-yellow-600" />
                      )}
                    </Button>
                  ))}
                </div>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-green-100 border border-green-300 rounded"></div>
                    <span>Answered</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-yellow-100 border border-yellow-300 rounded"></div>
                    <span>Flagged</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-white border border-gray-300 rounded"></div>
                    <span>Not answered</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Main Question Area */}
          <div className="lg:col-span-3">
            <Card className="border-0 shadow-2xl bg-white/90 backdrop-blur-sm">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                        {questions[currentQuestion].domain}
                      </Badge>
                      <Badge variant="outline" className="bg-purple-50 text-purple-700 border-purple-200">
                        {questions[currentQuestion].difficulty}
                      </Badge>
                    </div>
                    <CardTitle className="text-xl leading-relaxed">{questions[currentQuestion].question}</CardTitle>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={toggleFlag}
                    className={flaggedQuestions.has(currentQuestion) ? "bg-yellow-50 border-yellow-300" : ""}
                  >
                    <Flag className={`w-4 h-4 ${flaggedQuestions.has(currentQuestion) ? "text-yellow-600" : ""}`} />
                  </Button>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                <RadioGroup
                  value={answers[currentQuestion] || ""}
                  onValueChange={handleAnswerChange}
                  className="space-y-4"
                >
                  {questions[currentQuestion].options.map((option, index) => (
                    <div
                      key={index}
                      className={`flex items-start space-x-3 p-4 rounded-lg border transition-all duration-200 cursor-pointer hover:bg-gray-50 ${
                        answers[currentQuestion] === option.id ? "bg-blue-50 border-blue-300" : "border-gray-200"
                      }`}
                      onClick={() => handleAnswerChange(option.id)}
                    >
                      <RadioGroupItem value={option.id} id={option.id} className="mt-1" />
                      <Label htmlFor={option.id} className="flex-1 cursor-pointer text-base leading-relaxed">
                        <span className="font-semibold text-gray-700 mr-2">{option.id.toUpperCase()}.</span>
                        {option.text}
                      </Label>
                    </div>
                  ))}
                </RadioGroup>

                {/* Navigation Buttons */}
                <div className="flex justify-between items-center pt-6 border-t">
                  <Button
                    variant="outline"
                    onClick={() => setCurrentQuestion(Math.max(0, currentQuestion - 1))}
                    disabled={currentQuestion === 0}
                    className="flex items-center space-x-2"
                  >
                    <ChevronLeft className="w-4 h-4" />
                    <span>Previous</span>
                  </Button>

                  <div className="flex space-x-3">
                    {currentQuestion === questions.length - 1 ? (
                      <Button
                        onClick={() => setExamCompleted(true)}
                        className="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white px-8"
                      >
                        Submit Exam
                      </Button>
                    ) : (
                      <Button
                        onClick={() => setCurrentQuestion(Math.min(questions.length - 1, currentQuestion + 1))}
                        className="flex items-center space-x-2 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white"
                      >
                        <span>Next</span>
                        <ChevronRight className="w-4 h-4" />
                      </Button>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
