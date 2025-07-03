"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { ChevronLeft, ChevronRight, CheckCircle, XCircle, Lightbulb, ArrowLeft, Shuffle } from "lucide-react"
import type { Question } from "@/types/question"

interface PracticeInterfaceProps {
  questions: Question[]
  examType: string
  onExit: () => void
}

export default function PracticeInterface({ questions, examType, onExit }: PracticeInterfaceProps) {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<string>("")
  const [showExplanation, setShowExplanation] = useState(false)
  const [answeredQuestions, setAnsweredQuestions] = useState<Set<number>>(new Set())
  const [correctAnswers, setCorrectAnswers] = useState<Set<number>>(new Set())
  const [shuffledQuestions, setShuffledQuestions] = useState(questions)

  useEffect(() => {
    // Shuffle questions for practice mode
    const shuffled = [...questions].sort(() => Math.random() - 0.5)
    setShuffledQuestions(shuffled)
  }, [questions])

  const currentQ = shuffledQuestions[currentQuestion]
  const isAnswered = answeredQuestions.has(currentQuestion)
  const isCorrect = correctAnswers.has(currentQuestion)

  const handleAnswerSubmit = () => {
    if (!selectedAnswer) return

    const newAnsweredQuestions = new Set(answeredQuestions)
    newAnsweredQuestions.add(currentQuestion)
    setAnsweredQuestions(newAnsweredQuestions)

    if (selectedAnswer === currentQ.correctAnswer) {
      const newCorrectAnswers = new Set(correctAnswers)
      newCorrectAnswers.add(currentQuestion)
      setCorrectAnswers(newCorrectAnswers)
    }

    setShowExplanation(true)
  }

  const handleNextQuestion = () => {
    if (currentQuestion < shuffledQuestions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
      setSelectedAnswer("")
      setShowExplanation(false)
    }
  }

  const handlePreviousQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1)
      setSelectedAnswer("")
      setShowExplanation(false)
    }
  }

  const shuffleQuestions = () => {
    const shuffled = [...shuffledQuestions].sort(() => Math.random() - 0.5)
    setShuffledQuestions(shuffled)
    setCurrentQuestion(0)
    setSelectedAnswer("")
    setShowExplanation(false)
    setAnsweredQuestions(new Set())
    setCorrectAnswers(new Set())
  }

  const accuracy = answeredQuestions.size > 0 ? (correctAnswers.size / answeredQuestions.size) * 100 : 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-green-600 to-emerald-700 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button variant="ghost" onClick={onExit} className="text-white hover:bg-white/10">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Exit Practice
              </Button>
              <div className="border-l border-white/20 pl-4">
                <h1 className="text-xl font-bold">{examType} Practice Mode</h1>
                <p className="text-green-100 text-sm">
                  Question {currentQuestion + 1} of {shuffledQuestions.length}
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-6">
              <div className="text-center">
                <div className="text-2xl font-bold">
                  {correctAnswers.size}/{answeredQuestions.size}
                </div>
                <div className="text-green-100 text-sm">Correct</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">{accuracy.toFixed(0)}%</div>
                <div className="text-green-100 text-sm">Accuracy</div>
              </div>
              <Button
                variant="outline"
                onClick={shuffleQuestions}
                className="border-white/20 text-white hover:bg-white/10 bg-transparent"
              >
                <Shuffle className="w-4 h-4 mr-2" />
                Shuffle
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Question Navigation */}
          <div className="lg:col-span-1">
            <Card className="border-0 shadow-xl bg-white/80 backdrop-blur-sm sticky top-6">
              <CardHeader>
                <CardTitle className="text-lg">Progress</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-5 gap-2 mb-4">
                  {shuffledQuestions.slice(0, 25).map((_, index) => (
                    <Button
                      key={index}
                      variant={currentQuestion === index ? "default" : "outline"}
                      size="sm"
                      className={`relative ${
                        answeredQuestions.has(index)
                          ? correctAnswers.has(index)
                            ? "bg-green-100 border-green-300 text-green-800 hover:bg-green-200"
                            : "bg-red-100 border-red-300 text-red-800 hover:bg-red-200"
                          : ""
                      }`}
                      onClick={() => {
                        setCurrentQuestion(index)
                        setSelectedAnswer("")
                        setShowExplanation(false)
                      }}
                    >
                      {index + 1}
                      {answeredQuestions.has(index) &&
                        (correctAnswers.has(index) ? (
                          <CheckCircle className="w-3 h-3 absolute -top-1 -right-1 text-green-600" />
                        ) : (
                          <XCircle className="w-3 h-3 absolute -top-1 -right-1 text-red-600" />
                        ))}
                    </Button>
                  ))}
                </div>

                <div className="space-y-2 text-sm">
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-green-100 border border-green-300 rounded"></div>
                    <span>Correct ({correctAnswers.size})</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-red-100 border border-red-300 rounded"></div>
                    <span>Incorrect ({answeredQuestions.size - correctAnswers.size})</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-white border border-gray-300 rounded"></div>
                    <span>Not answered ({shuffledQuestions.length - answeredQuestions.size})</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Main Question Area */}
          <div className="lg:col-span-3">
            <Card className="border-0 shadow-2xl bg-white/90 backdrop-blur-sm">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                      {currentQ.domain}
                    </Badge>
                    <Badge variant="outline" className="bg-purple-50 text-purple-700 border-purple-200">
                      {currentQ.difficulty}
                    </Badge>
                  </div>
                  {isAnswered && (
                    <Badge variant={isCorrect ? "default" : "destructive"}>{isCorrect ? "Correct" : "Incorrect"}</Badge>
                  )}
                </div>
                <CardTitle className="text-xl leading-relaxed mt-4">{currentQ.question}</CardTitle>
              </CardHeader>

              <CardContent className="space-y-6">
                <RadioGroup
                  value={selectedAnswer}
                  onValueChange={setSelectedAnswer}
                  disabled={isAnswered}
                  className="space-y-4"
                >
                  {currentQ.options.map((option, index) => {
                    let optionClass =
                      "flex items-start space-x-3 p-4 rounded-lg border transition-all duration-200 cursor-pointer hover:bg-gray-50"

                    if (isAnswered) {
                      if (option.id === currentQ.correctAnswer) {
                        optionClass += " bg-green-50 border-green-300"
                      } else if (option.id === selectedAnswer && option.id !== currentQ.correctAnswer) {
                        optionClass += " bg-red-50 border-red-300"
                      } else {
                        optionClass += " border-gray-200"
                      }
                    } else if (selectedAnswer === option.id) {
                      optionClass += " bg-blue-50 border-blue-300"
                    } else {
                      optionClass += " border-gray-200"
                    }

                    return (
                      <div
                        key={index}
                        className={optionClass}
                        onClick={() => !isAnswered && setSelectedAnswer(option.id)}
                      >
                        <RadioGroupItem value={option.id} id={option.id} className="mt-1" disabled={isAnswered} />
                        <Label htmlFor={option.id} className="flex-1 cursor-pointer text-base leading-relaxed">
                          <span className="font-semibold text-gray-700 mr-2">{option.id.toUpperCase()}.</span>
                          {option.text}
                        </Label>
                        {isAnswered && option.id === currentQ.correctAnswer && (
                          <CheckCircle className="w-5 h-5 text-green-600 mt-1" />
                        )}
                        {isAnswered && option.id === selectedAnswer && option.id !== currentQ.correctAnswer && (
                          <XCircle className="w-5 h-5 text-red-600 mt-1" />
                        )}
                      </div>
                    )
                  })}
                </RadioGroup>

                {/* Submit Button */}
                {!isAnswered && (
                  <Button
                    onClick={handleAnswerSubmit}
                    disabled={!selectedAnswer}
                    className="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white py-3"
                  >
                    Submit Answer
                  </Button>
                )}

                {/* Explanation */}
                {showExplanation && (
                  <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
                    <CardContent className="p-4">
                      <div className="flex items-start space-x-3">
                        <Lightbulb className="w-6 h-6 text-blue-600 mt-1 flex-shrink-0" />
                        <div>
                          <h4 className="font-semibold text-blue-900 mb-2">Explanation</h4>
                          <p className="text-blue-800 leading-relaxed">{currentQ.explanation}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* Navigation */}
                <div className="flex justify-between items-center pt-6 border-t">
                  <Button
                    variant="outline"
                    onClick={handlePreviousQuestion}
                    disabled={currentQuestion === 0}
                    className="flex items-center space-x-2 bg-transparent"
                  >
                    <ChevronLeft className="w-4 h-4" />
                    <span>Previous</span>
                  </Button>

                  <div className="text-center">
                    <div className="text-sm text-gray-600">
                      Question {currentQuestion + 1} of {shuffledQuestions.length}
                    </div>
                  </div>

                  <Button
                    onClick={handleNextQuestion}
                    disabled={currentQuestion === shuffledQuestions.length - 1}
                    className="flex items-center space-x-2 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white"
                  >
                    <span>Next</span>
                    <ChevronRight className="w-4 h-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
