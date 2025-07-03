"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Award,
  Clock,
  Target,
  TrendingUp,
  CheckCircle,
  XCircle,
  BarChart3,
  RefreshCw,
  ArrowLeft,
  Download,
  Share,
} from "lucide-react"
import type { Question } from "@/types/question"

interface ExamResultsProps {
  examType: string
  questions: Question[]
  answers: Record<number, string>
  timeSpent: number
  onRetake: () => void
  onExit: () => void
}

export default function ExamResults({ examType, questions, answers, timeSpent, onRetake, onExit }: ExamResultsProps) {
  const totalQuestions = questions.length
  const answeredQuestions = Object.keys(answers).length
  const correctAnswers = questions.filter((q, index) => answers[index] === q.correctAnswer).length
  const percentage = Math.round((correctAnswers / totalQuestions) * 100)
  const passed = percentage >= 72

  // Calculate domain scores
  const domainScores: Record<string, { correct: number; total: number }> = {}
  questions.forEach((question, index) => {
    if (!domainScores[question.domain]) {
      domainScores[question.domain] = { correct: 0, total: 0 }
    }
    domainScores[question.domain].total++
    if (answers[index] === question.correctAnswer) {
      domainScores[question.domain].correct++
    }
  })

  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return `${hours}h ${minutes}m`
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <Card className="border-0 shadow-2xl bg-white/80 backdrop-blur-sm mb-6">
          <CardHeader className="text-center pb-8">
            <div
              className={`mx-auto w-20 h-20 rounded-full flex items-center justify-center mb-4 ${
                passed ? "bg-gradient-to-r from-green-400 to-emerald-500" : "bg-gradient-to-r from-red-400 to-rose-500"
              }`}
            >
              <Award className="w-10 h-10 text-white" />
            </div>
            <CardTitle className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Exam Completed!
            </CardTitle>
            <CardDescription className="text-lg text-gray-600">{examType} Practice Exam Results</CardDescription>
          </CardHeader>

          <CardContent className="space-y-6">
            <div className="text-center">
              <div className={`text-6xl font-bold mb-2 ${passed ? "text-green-500" : "text-red-500"}`}>
                {percentage}%
              </div>
              <Badge variant={passed ? "default" : "destructive"} className="text-lg px-4 py-2">
                {passed ? "PASSED" : "FAILED"}
              </Badge>
              <p className="text-gray-600 mt-2">
                {passed ? "Congratulations! You're ready for the real exam." : "Keep studying and try again."}
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card className="bg-gradient-to-r from-blue-500 to-blue-600 text-white">
                <CardContent className="p-4 text-center">
                  <Target className="w-8 h-8 mx-auto mb-2" />
                  <div className="text-2xl font-bold">{correctAnswers}</div>
                  <div className="text-sm opacity-90">Correct Answers</div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-r from-green-500 to-green-600 text-white">
                <CardContent className="p-4 text-center">
                  <CheckCircle className="w-8 h-8 mx-auto mb-2" />
                  <div className="text-2xl font-bold">{totalQuestions}</div>
                  <div className="text-sm opacity-90">Total Questions</div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-r from-purple-500 to-purple-600 text-white">
                <CardContent className="p-4 text-center">
                  <Clock className="w-8 h-8 mx-auto mb-2" />
                  <div className="text-2xl font-bold">{formatTime(timeSpent)}</div>
                  <div className="text-sm opacity-90">Time Spent</div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-r from-orange-500 to-orange-600 text-white">
                <CardContent className="p-4 text-center">
                  <TrendingUp className="w-8 h-8 mx-auto mb-2" />
                  <div className="text-2xl font-bold">72%</div>
                  <div className="text-sm opacity-90">Passing Score</div>
                </CardContent>
              </Card>
            </div>

            <div className="flex justify-center space-x-4">
              <Button
                onClick={onRetake}
                className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-8 py-3"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                Retake Exam
              </Button>
              <Button onClick={onExit} variant="outline" className="px-8 py-3 bg-transparent">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Dashboard
              </Button>
              <Button variant="outline" className="px-4 py-3 bg-transparent">
                <Download className="w-4 h-4" />
              </Button>
              <Button variant="outline" className="px-4 py-3 bg-transparent">
                <Share className="w-4 h-4" />
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Detailed Results */}
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3 bg-white/80 backdrop-blur-sm">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="domains">Domain Analysis</TabsTrigger>
            <TabsTrigger value="review">Question Review</TabsTrigger>
          </TabsList>

          <TabsContent value="overview">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <BarChart3 className="w-5 h-5" />
                    <span>Performance Summary</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm font-medium">Overall Score</span>
                      <span className="text-sm text-gray-600">{percentage}%</span>
                    </div>
                    <Progress value={percentage} className="h-3" />
                  </div>

                  <div className="grid grid-cols-2 gap-4 pt-4">
                    <div className="text-center p-3 bg-green-50 rounded-lg">
                      <div className="text-2xl font-bold text-green-600">{correctAnswers}</div>
                      <div className="text-sm text-green-700">Correct</div>
                    </div>
                    <div className="text-center p-3 bg-red-50 rounded-lg">
                      <div className="text-2xl font-bold text-red-600">{totalQuestions - correctAnswers}</div>
                      <div className="text-sm text-red-700">Incorrect</div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle>Recommendations</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {passed ? (
                    <div className="space-y-3">
                      <div className="flex items-center space-x-2 text-green-700">
                        <CheckCircle className="w-5 h-5" />
                        <span className="font-medium">Great job! You're exam-ready.</span>
                      </div>
                      <ul className="space-y-2 text-sm text-gray-600 ml-7">
                        <li>• Schedule your official AWS exam</li>
                        <li>• Review any missed questions</li>
                        <li>• Take one more practice exam before the real test</li>
                      </ul>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      <div className="flex items-center space-x-2 text-orange-700">
                        <XCircle className="w-5 h-5" />
                        <span className="font-medium">More study needed</span>
                      </div>
                      <ul className="space-y-2 text-sm text-gray-600 ml-7">
                        <li>• Focus on domains with low scores</li>
                        <li>• Review AWS documentation</li>
                        <li>• Take more practice exams</li>
                        <li>• Consider additional study materials</li>
                      </ul>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="domains">
            <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
              <CardHeader>
                <CardTitle>Domain Performance Analysis</CardTitle>
                <CardDescription>Your performance across different exam domains</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {Object.entries(domainScores).map(([domain, scores]) => {
                  const domainPercentage = Math.round((scores.correct / scores.total) * 100)
                  return (
                    <div key={domain} className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="font-medium text-gray-800">{domain}</span>
                        <div className="flex items-center space-x-2">
                          <span className="text-sm text-gray-600">
                            {scores.correct}/{scores.total}
                          </span>
                          <Badge variant={domainPercentage >= 70 ? "default" : "destructive"}>
                            {domainPercentage}%
                          </Badge>
                        </div>
                      </div>
                      <Progress value={domainPercentage} className="h-2" />
                    </div>
                  )
                })}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="review">
            <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
              <CardHeader>
                <CardTitle>Question Review</CardTitle>
                <CardDescription>Review your answers and explanations</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  {questions.map((question, index) => {
                    const userAnswer = answers[index]
                    const isCorrect = userAnswer === question.correctAnswer

                    return (
                      <div
                        key={index}
                        className={`p-4 rounded-lg border ${
                          isCorrect ? "bg-green-50 border-green-200" : "bg-red-50 border-red-200"
                        }`}
                      >
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex items-center space-x-2">
                            <Badge variant="outline">Q{index + 1}</Badge>
                            <Badge variant="outline">{question.domain}</Badge>
                          </div>
                          {isCorrect ? (
                            <CheckCircle className="w-5 h-5 text-green-600" />
                          ) : (
                            <XCircle className="w-5 h-5 text-red-600" />
                          )}
                        </div>

                        <h4 className="font-medium text-gray-900 mb-3">{question.question}</h4>

                        <div className="space-y-2 mb-4">
                          {question.options.map((option) => (
                            <div
                              key={option.id}
                              className={`p-2 rounded text-sm ${
                                option.id === question.correctAnswer
                                  ? "bg-green-100 text-green-800 font-medium"
                                  : option.id === userAnswer && !isCorrect
                                    ? "bg-red-100 text-red-800"
                                    : "text-gray-600"
                              }`}
                            >
                              <span className="font-semibold mr-2">{option.id.toUpperCase()}.</span>
                              {option.text}
                              {option.id === question.correctAnswer && (
                                <span className="ml-2 text-green-600">✓ Correct</span>
                              )}
                              {option.id === userAnswer && !isCorrect && (
                                <span className="ml-2 text-red-600">✗ Your answer</span>
                              )}
                            </div>
                          ))}
                        </div>

                        <div className="bg-blue-50 p-3 rounded border border-blue-200">
                          <div className="flex items-start space-x-2">
                            <div className="w-5 h-5 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                              <span className="text-blue-600 text-xs font-bold">i</span>
                            </div>
                            <div>
                              <h5 className="font-medium text-blue-900 mb-1">Explanation</h5>
                              <p className="text-blue-800 text-sm">{question.explanation}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
