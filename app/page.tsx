"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Clock, BookOpen, Award, Target, Star, Play, Brain, BarChart3 } from "lucide-react"
import { useAuth } from "@/hooks/use-auth"
import AuthModal from "@/components/auth-modal"
import ExamSelection from "@/components/exam-selection"
import Dashboard from "@/components/dashboard"
import StudyMaterials from "@/components/study-materials"

export default function HomePage() {
  const { user, loading } = useAuth()
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [activeTab, setActiveTab] = useState("exams")

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    return (
      <>
        <div className="min-h-screen bg-gradient-to-br from-orange-50 via-red-50 to-pink-50">
          {/* Header */}
          <header className="bg-gradient-to-r from-orange-500 to-red-600 text-white shadow-lg">
            <div className="max-w-7xl mx-auto px-4 py-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
                    <Award className="w-8 h-8" />
                  </div>
                  <div>
                    <h1 className="text-2xl font-bold">AWS Certification Hub</h1>
                    <p className="text-orange-100">Master AWS with Comprehensive Practice Exams</p>
                  </div>
                </div>
                <Button onClick={() => setShowAuthModal(true)} className="bg-white text-orange-600 hover:bg-orange-50">
                  Sign In / Sign Up
                </Button>
              </div>
            </div>
          </header>

          <div className="max-w-7xl mx-auto p-6">
            {/* Hero Section */}
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">Ace Your AWS Certification</h2>
              <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                Practice with thousands of real exam questions, track your progress, and get certified faster with our
                comprehensive AWS training platform.
              </p>
              <div className="flex justify-center space-x-4">
                <Button
                  onClick={() => setShowAuthModal(true)}
                  className="bg-gradient-to-r from-orange-500 to-red-600 hover:from-orange-600 hover:to-red-700 text-white px-8 py-3 text-lg"
                >
                  Start Free Trial
                </Button>
                <Button
                  variant="outline"
                  className="border-orange-300 text-orange-600 hover:bg-orange-50 px-8 py-3 text-lg bg-transparent"
                >
                  View Demo
                </Button>
              </div>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
              <Card className="border-0 shadow-xl bg-gradient-to-br from-blue-500 to-blue-600 text-white">
                <CardContent className="p-6 text-center">
                  <BookOpen className="w-12 h-12 mx-auto mb-4" />
                  <h3 className="text-xl font-bold mb-2">2000+ Questions</h3>
                  <p className="text-blue-100">Comprehensive question banks for all AWS certifications</p>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-xl bg-gradient-to-br from-green-500 to-green-600 text-white">
                <CardContent className="p-6 text-center">
                  <Target className="w-12 h-12 mx-auto mb-4" />
                  <h3 className="text-xl font-bold mb-2">Real Exam Simulation</h3>
                  <p className="text-green-100">Authentic exam experience with timed tests</p>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-xl bg-gradient-to-br from-purple-500 to-purple-600 text-white">
                <CardContent className="p-6 text-center">
                  <BarChart3 className="w-12 h-12 mx-auto mb-4" />
                  <h3 className="text-xl font-bold mb-2">Performance Analytics</h3>
                  <p className="text-purple-100">Track progress and identify weak areas</p>
                </CardContent>
              </Card>

              <Card className="border-0 shadow-xl bg-gradient-to-br from-pink-500 to-pink-600 text-white">
                <CardContent className="p-6 text-center">
                  <Brain className="w-12 h-12 mx-auto mb-4" />
                  <h3 className="text-xl font-bold mb-2">Smart Learning</h3>
                  <p className="text-pink-100">AI-powered recommendations and study plans</p>
                </CardContent>
              </Card>
            </div>

            {/* Certification Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                {
                  title: "Solutions Architect Associate",
                  code: "SAA-C03",
                  questions: 100,
                  duration: "130 min",
                  difficulty: "Intermediate",
                  color: "from-blue-500 to-indigo-600",
                },
                {
                  title: "Developer Associate",
                  code: "DVA-C01",
                  questions: 65,
                  duration: "130 min",
                  difficulty: "Intermediate",
                  color: "from-green-500 to-emerald-600",
                },
                {
                  title: "SysOps Administrator",
                  code: "SOA-C02",
                  questions: 65,
                  duration: "130 min",
                  difficulty: "Intermediate",
                  color: "from-purple-500 to-violet-600",
                },
                {
                  title: "Solutions Architect Professional",
                  code: "SAP-C02",
                  questions: 75,
                  duration: "180 min",
                  difficulty: "Advanced",
                  color: "from-red-500 to-rose-600",
                },
                {
                  title: "DevOps Engineer Professional",
                  code: "DOP-C02",
                  questions: 75,
                  duration: "180 min",
                  difficulty: "Advanced",
                  color: "from-orange-500 to-amber-600",
                },
                {
                  title: "Cloud Practitioner",
                  code: "CLF-C01",
                  questions: 65,
                  duration: "90 min",
                  difficulty: "Foundational",
                  color: "from-teal-500 to-cyan-600",
                },
              ].map((cert, index) => (
                <Card
                  key={index}
                  className="border-0 shadow-xl bg-white/80 backdrop-blur-sm hover:shadow-2xl transition-all duration-300"
                >
                  <CardHeader>
                    <div className={`w-full h-2 bg-gradient-to-r ${cert.color} rounded-full mb-4`}></div>
                    <CardTitle className="text-xl">{cert.title}</CardTitle>
                    <CardDescription className="text-lg font-semibold text-gray-700">{cert.code}</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div className="flex items-center space-x-2">
                        <BookOpen className="w-4 h-4 text-gray-500" />
                        <span>{cert.questions} Questions</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Clock className="w-4 h-4 text-gray-500" />
                        <span>{cert.duration}</span>
                      </div>
                    </div>
                    <Badge variant="secondary" className="w-full justify-center py-2">
                      {cert.difficulty}
                    </Badge>
                    <Button
                      onClick={() => setShowAuthModal(true)}
                      className={`w-full bg-gradient-to-r ${cert.color} hover:opacity-90 text-white`}
                    >
                      Start Practice
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </div>
        <AuthModal open={showAuthModal} onClose={() => setShowAuthModal(false)} />
      </>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
                <Award className="w-6 h-6" />
              </div>
              <div>
                <h1 className="text-xl font-bold">AWS Certification Hub</h1>
                <p className="text-blue-100 text-sm">Welcome back, {user.name}!</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="secondary" className="bg-white/20 text-white">
                <Star className="w-4 h-4 mr-1" />
                Pro Member
              </Badge>
              <Button
                variant="outline"
                className="border-white/20 text-white hover:bg-white/10 bg-transparent"
                onClick={() => {
                  /* logout logic */
                }}
              >
                Sign Out
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto p-6">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 bg-white/80 backdrop-blur-sm">
            <TabsTrigger value="dashboard" className="flex items-center space-x-2">
              <BarChart3 className="w-4 h-4" />
              <span>Dashboard</span>
            </TabsTrigger>
            <TabsTrigger value="exams" className="flex items-center space-x-2">
              <Play className="w-4 h-4" />
              <span>Exams</span>
            </TabsTrigger>
            <TabsTrigger value="practice" className="flex items-center space-x-2">
              <Brain className="w-4 h-4" />
              <span>Practice</span>
            </TabsTrigger>
            <TabsTrigger value="study" className="flex items-center space-x-2">
              <BookOpen className="w-4 h-4" />
              <span>Study Materials</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="dashboard">
            <Dashboard />
          </TabsContent>

          <TabsContent value="exams">
            <ExamSelection mode="exam" />
          </TabsContent>

          <TabsContent value="practice">
            <ExamSelection mode="practice" />
          </TabsContent>

          <TabsContent value="study">
            <StudyMaterials />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
