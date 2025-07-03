"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Button } from "@/components/ui/button"
import { BarChart3, TrendingUp, Clock, Target, Award, BookOpen, Calendar, Star } from "lucide-react"
import { useAuth } from "@/hooks/use-auth"

export default function Dashboard() {
  const { user } = useAuth()

  if (!user) return null

  const recentExam = user.examHistory[0]
  const totalExams = user.examHistory.length
  const averageScore = user.examHistory.reduce((acc, exam) => acc + exam.score, 0) / totalExams || 0

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <Card className="border-0 shadow-xl bg-gradient-to-r from-blue-500 to-indigo-600 text-white">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold mb-2">Welcome back, {user.name}!</h2>
              <p className="text-blue-100">Continue your AWS certification journey</p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold">{totalExams}</div>
              <div className="text-blue-100">Exams Taken</div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="border-0 shadow-lg">
          <CardContent className="p-6">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <Target className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <div className="text-2xl font-bold text-green-600">{averageScore.toFixed(0)}%</div>
                <div className="text-sm text-gray-600">Average Score</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-0 shadow-lg">
          <CardContent className="p-6">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Clock className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <div className="text-2xl font-bold text-blue-600">2.5h</div>
                <div className="text-sm text-gray-600">Study Time</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-0 shadow-lg">
          <CardContent className="p-6">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <BookOpen className="w-6 h-6 text-purple-600" />
              </div>
              <div>
                <div className="text-2xl font-bold text-purple-600">450</div>
                <div className="text-sm text-gray-600">Questions Answered</div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-0 shadow-lg">
          <CardContent className="p-6">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-orange-100 rounded-lg">
                <TrendingUp className="w-6 h-6 text-orange-600" />
              </div>
              <div>
                <div className="text-2xl font-bold text-orange-600">+12%</div>
                <div className="text-sm text-gray-600">Improvement</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Performance */}
        <Card className="border-0 shadow-xl">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <BarChart3 className="w-5 h-5" />
              <span>Recent Performance</span>
            </CardTitle>
            <CardDescription>Your latest exam results by domain</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {recentExam ? (
              <>
                <div className="flex items-center justify-between mb-4">
                  <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                    {recentExam.examType}
                  </Badge>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-green-600">{recentExam.score}%</div>
                    <div className="text-sm text-gray-600">Overall Score</div>
                  </div>
                </div>

                {Object.entries(recentExam.domainScores).map(([domain, score]) => (
                  <div key={domain} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="font-medium">{domain}</span>
                      <span className="text-gray-600">{score}%</span>
                    </div>
                    <Progress value={score} className="h-2" />
                  </div>
                ))}
              </>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <BookOpen className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>No exams taken yet. Start your first practice exam!</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Study Plan */}
        <Card className="border-0 shadow-xl">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Calendar className="w-5 h-5" />
              <span>Study Plan</span>
            </CardTitle>
            <CardDescription>Recommended next steps</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <div className="flex items-center space-x-3 p-3 bg-blue-50 rounded-lg">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <div className="flex-1">
                  <div className="font-medium">Practice EC2 & VPC Questions</div>
                  <div className="text-sm text-gray-600">Focus on networking concepts</div>
                </div>
                <Badge variant="secondary">Today</Badge>
              </div>

              <div className="flex items-center space-x-3 p-3 bg-green-50 rounded-lg">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <div className="flex-1">
                  <div className="font-medium">Review Security Best Practices</div>
                  <div className="text-sm text-gray-600">IAM, KMS, and encryption</div>
                </div>
                <Badge variant="secondary">Tomorrow</Badge>
              </div>

              <div className="flex items-center space-x-3 p-3 bg-purple-50 rounded-lg">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                <div className="flex-1">
                  <div className="font-medium">Take Full Practice Exam</div>
                  <div className="text-sm text-gray-600">SAA-C03 simulation</div>
                </div>
                <Badge variant="secondary">This Week</Badge>
              </div>
            </div>

            <Button className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700">
              Start Today's Study Session
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Achievements */}
      <Card className="border-0 shadow-xl">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Award className="w-5 h-5" />
            <span>Achievements</span>
          </CardTitle>
          <CardDescription>Your learning milestones</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center space-x-3 p-4 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg border border-yellow-200">
              <div className="p-2 bg-yellow-100 rounded-full">
                <Star className="w-6 h-6 text-yellow-600" />
              </div>
              <div>
                <div className="font-semibold text-yellow-800">First Exam</div>
                <div className="text-sm text-yellow-600">Completed your first practice exam</div>
              </div>
            </div>

            <div className="flex items-center space-x-3 p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-200">
              <div className="p-2 bg-green-100 rounded-full">
                <Target className="w-6 h-6 text-green-600" />
              </div>
              <div>
                <div className="font-semibold text-green-800">High Scorer</div>
                <div className="text-sm text-green-600">Scored above 80% on an exam</div>
              </div>
            </div>

            <div className="flex items-center space-x-3 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200 opacity-50">
              <div className="p-2 bg-blue-100 rounded-full">
                <BookOpen className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <div className="font-semibold text-blue-800">Study Streak</div>
                <div className="text-sm text-blue-600">Study for 7 days in a row</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
