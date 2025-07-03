"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Clock, BookOpen, Target, Play, Brain, Star, Users } from "lucide-react"
import ExamInterface from "@/components/exam-interface"
import PracticeInterface from "@/components/practice-interface"
import { examQuestions } from "@/data/questions"
import { allExamData } from "@/data/all-exams"

interface ExamSelectionProps {
  mode: "exam" | "practice"
}

export default function ExamSelection({ mode }: ExamSelectionProps) {
  const [selectedExam, setSelectedExam] = useState<string | null>(null)
  const [examStarted, setExamStarted] = useState(false)

  if (examStarted && selectedExam) {
    const examData = allExamData[selectedExam] || examQuestions

    if (mode === "practice") {
      return (
        <PracticeInterface
          questions={examData}
          examType={selectedExam}
          onExit={() => {
            setExamStarted(false)
            setSelectedExam(null)
          }}
        />
      )
    } else {
      return (
        <ExamInterface
          questions={examData}
          examType={selectedExam}
          onExit={() => {
            setExamStarted(false)
            setSelectedExam(null)
          }}
        />
      )
    }
  }

  const certifications = [
    {
      id: "SAA-C03",
      title: "Solutions Architect Associate",
      code: "SAA-C03",
      questions: 100,
      duration: "130 min",
      difficulty: "Intermediate",
      passingScore: 72,
      color: "from-blue-500 to-indigo-600",
      description: "Design resilient, high-performing, secure, and cost-optimized architectures",
      domains: [
        "Design Resilient Architectures (30%)",
        "Design High-Performing Architectures (28%)",
        "Design Secure Applications (24%)",
        "Design Cost-Optimized Architectures (18%)",
      ],
      popularity: 95,
    },
    {
      id: "DVA-C01",
      title: "Developer Associate",
      code: "DVA-C01",
      questions: 65,
      duration: "130 min",
      difficulty: "Intermediate",
      passingScore: 72,
      color: "from-green-500 to-emerald-600",
      description: "Develop and maintain applications on AWS platform",
      domains: [
        "Development with AWS Services (32%)",
        "Security (26%)",
        "Deployment (24%)",
        "Troubleshooting and Optimization (18%)",
      ],
      popularity: 85,
    },
    {
      id: "SOA-C02",
      title: "SysOps Administrator",
      code: "SOA-C02",
      questions: 65,
      duration: "130 min",
      difficulty: "Intermediate",
      passingScore: 72,
      color: "from-purple-500 to-violet-600",
      description: "Deploy, manage, and operate scalable systems on AWS",
      domains: [
        "Monitoring, Logging, and Remediation (20%)",
        "Reliability and Business Continuity (16%)",
        "Deployment, Provisioning, and Automation (18%)",
        "Security and Compliance (16%)",
        "Networking and Content Delivery (18%)",
        "Cost and Performance Optimization (12%)",
      ],
      popularity: 75,
    },
    {
      id: "SAP-C02",
      title: "Solutions Architect Professional",
      code: "SAP-C02",
      questions: 75,
      duration: "180 min",
      difficulty: "Advanced",
      passingScore: 75,
      color: "from-red-500 to-rose-600",
      description: "Design and deploy dynamically scalable, highly available applications",
      domains: [
        "Design Solutions for Organizational Complexity (26%)",
        "Design for New Solutions (29%)",
        "Continuous Improvement for Existing Solutions (25%)",
        "Accelerate Workload Migration and Modernization (20%)",
      ],
      popularity: 90,
    },
    {
      id: "DOP-C02",
      title: "DevOps Engineer Professional",
      code: "DOP-C02",
      questions: 75,
      duration: "180 min",
      difficulty: "Advanced",
      passingScore: 75,
      color: "from-orange-500 to-amber-600",
      description: "Implement and manage continuous delivery systems",
      domains: [
        "SDLC Automation (22%)",
        "Configuration Management and IaC (19%)",
        "Monitoring and Logging (15%)",
        "Policies and Standards Automation (10%)",
        "Incident and Event Response (18%)",
        "High Availability, Fault Tolerance, and Disaster Recovery (16%)",
      ],
      popularity: 70,
    },
    {
      id: "CLF-C01",
      title: "Cloud Practitioner",
      code: "CLF-C01",
      questions: 65,
      duration: "90 min",
      difficulty: "Foundational",
      passingScore: 70,
      color: "from-teal-500 to-cyan-600",
      description: "Foundational understanding of AWS Cloud",
      domains: [
        "Cloud Concepts (26%)",
        "Security and Compliance (25%)",
        "Technology (33%)",
        "Billing and Pricing (16%)",
      ],
      popularity: 80,
    },
  ]

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          {mode === "exam" ? "Practice Exams" : "Practice Mode"}
        </h2>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          {mode === "exam"
            ? "Take full-length practice exams that simulate the real AWS certification experience"
            : "Practice individual questions with immediate feedback and explanations"}
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {certifications.map((cert) => (
          <Card
            key={cert.id}
            className="border-0 shadow-xl bg-white/90 backdrop-blur-sm hover:shadow-2xl transition-all duration-300"
          >
            <CardHeader>
              <div className={`w-full h-3 bg-gradient-to-r ${cert.color} rounded-full mb-4`}></div>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-xl mb-2">{cert.title}</CardTitle>
                  <CardDescription className="text-lg font-semibold text-gray-700 mb-2">{cert.code}</CardDescription>
                  <p className="text-sm text-gray-600 mb-4">{cert.description}</p>
                </div>
                <div className="flex items-center space-x-1 ml-4">
                  <Users className="w-4 h-4 text-gray-500" />
                  <span className="text-sm text-gray-600">{cert.popularity}%</span>
                </div>
              </div>
            </CardHeader>

            <CardContent className="space-y-6">
              {/* Exam Details */}
              <div className="grid grid-cols-2 gap-4">
                <div className="flex items-center space-x-2 text-sm">
                  <BookOpen className="w-4 h-4 text-gray-500" />
                  <span>{cert.questions} Questions</span>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <Clock className="w-4 h-4 text-gray-500" />
                  <span>{cert.duration}</span>
                </div>
                <div className="flex items-center space-x-2 text-sm">
                  <Target className="w-4 h-4 text-gray-500" />
                  <span>{cert.passingScore}% to pass</span>
                </div>
                <Badge variant="secondary" className="justify-center py-1">
                  {cert.difficulty}
                </Badge>
              </div>

              {/* Domains */}
              <div>
                <h4 className="font-semibold text-gray-800 mb-3">Exam Domains:</h4>
                <div className="space-y-2">
                  {cert.domains.map((domain, index) => (
                    <div key={index} className="text-sm text-gray-600 bg-gray-50 px-3 py-2 rounded-lg">
                      {domain}
                    </div>
                  ))}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex space-x-3">
                <Button
                  onClick={() => {
                    setSelectedExam(cert.id)
                    setExamStarted(true)
                  }}
                  className={`flex-1 bg-gradient-to-r ${cert.color} hover:opacity-90 text-white`}
                >
                  {mode === "exam" ? (
                    <>
                      <Play className="w-4 h-4 mr-2" />
                      Start Exam
                    </>
                  ) : (
                    <>
                      <Brain className="w-4 h-4 mr-2" />
                      Practice
                    </>
                  )}
                </Button>

                <Button variant="outline" className="px-4 bg-transparent">
                  <Star className="w-4 h-4" />
                </Button>
              </div>

              {/* Quick Stats */}
              <div className="flex justify-between text-xs text-gray-500 pt-2 border-t">
                <span>Updated recently</span>
                <span>Based on latest exam guide</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
