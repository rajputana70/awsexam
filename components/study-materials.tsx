"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { BookOpen, Video, FileText, ExternalLink, Download, Clock, Star, Users, Play } from "lucide-react"

export default function StudyMaterials() {
  const studyResources = [
    {
      id: 1,
      title: "AWS Solutions Architect Complete Guide",
      type: "PDF",
      description: "Comprehensive 500-page guide covering all SAA-C03 exam topics",
      duration: "8-10 hours read",
      rating: 4.8,
      downloads: 15420,
      icon: FileText,
      color: "from-blue-500 to-indigo-600",
    },
    {
      id: 2,
      title: "EC2 and VPC Deep Dive Video Series",
      type: "Video",
      description: "12-part video series explaining AWS compute and networking",
      duration: "6 hours",
      rating: 4.9,
      downloads: 8930,
      icon: Video,
      color: "from-red-500 to-rose-600",
    },
    {
      id: 3,
      title: "AWS Security Best Practices Whitepaper",
      type: "PDF",
      description: "Official AWS security guidelines and implementation strategies",
      duration: "2-3 hours read",
      rating: 4.7,
      downloads: 12100,
      icon: FileText,
      color: "from-green-500 to-emerald-600",
    },
    {
      id: 4,
      title: "Hands-on Labs: Building on AWS",
      type: "Interactive",
      description: "Step-by-step labs for practical AWS experience",
      duration: "15 hours",
      rating: 4.9,
      downloads: 6750,
      icon: Play,
      color: "from-purple-500 to-violet-600",
    },
  ]

  const examGuides = [
    {
      exam: "SAA-C03",
      title: "Solutions Architect Associate",
      topics: [
        "Design Resilient Architectures",
        "Design High-Performing Architectures",
        "Design Secure Applications",
        "Design Cost-Optimized Architectures",
      ],
      resources: 45,
      color: "from-blue-500 to-indigo-600",
    },
    {
      exam: "DVA-C01",
      title: "Developer Associate",
      topics: ["Development with AWS Services", "Security", "Deployment", "Troubleshooting and Optimization"],
      resources: 38,
      color: "from-green-500 to-emerald-600",
    },
    {
      exam: "SOA-C02",
      title: "SysOps Administrator",
      topics: [
        "Monitoring, Logging, and Remediation",
        "Reliability and Business Continuity",
        "Deployment and Automation",
        "Security and Compliance",
      ],
      resources: 32,
      color: "from-purple-500 to-violet-600",
    },
    {
      exam: "SAP-C02",
      title: "Solutions Architect Professional",
      topics: [
        "Design Solutions for Organizational Complexity",
        "Design for New Solutions",
        "Continuous Improvement",
        "Accelerate Workload Migration",
      ],
      resources: 28,
      color: "from-red-500 to-rose-600",
    },
  ]

  const cheatSheets = [
    {
      title: "AWS Services Quick Reference",
      description: "One-page overview of all major AWS services",
      category: "General",
      downloads: 25000,
    },
    {
      title: "EC2 Instance Types Comparison",
      description: "Complete comparison of all EC2 instance families",
      category: "Compute",
      downloads: 18500,
    },
    {
      title: "S3 Storage Classes Decision Tree",
      description: "Visual guide to choosing the right S3 storage class",
      category: "Storage",
      downloads: 22000,
    },
    {
      title: "VPC Networking Essentials",
      description: "Subnets, routing, and security groups explained",
      category: "Networking",
      downloads: 19800,
    },
    {
      title: "IAM Policies and Permissions",
      description: "Understanding AWS identity and access management",
      category: "Security",
      downloads: 21200,
    },
    {
      title: "CloudFormation Template Examples",
      description: "Common infrastructure patterns as code",
      category: "DevOps",
      downloads: 16700,
    },
  ]

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Study Materials</h2>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Comprehensive resources to help you master AWS concepts and pass your certification exams
        </p>
      </div>

      <Tabs defaultValue="resources" className="space-y-6">
        <TabsList className="grid w-full grid-cols-3 bg-white/80 backdrop-blur-sm">
          <TabsTrigger value="resources">Study Resources</TabsTrigger>
          <TabsTrigger value="guides">Exam Guides</TabsTrigger>
          <TabsTrigger value="cheatsheets">Cheat Sheets</TabsTrigger>
        </TabsList>

        <TabsContent value="resources" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {studyResources.map((resource) => (
              <Card
                key={resource.id}
                className="border-0 shadow-xl bg-white/90 backdrop-blur-sm hover:shadow-2xl transition-all duration-300"
              >
                <CardHeader>
                  <div className={`w-full h-2 bg-gradient-to-r ${resource.color} rounded-full mb-4`}></div>
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`p-2 bg-gradient-to-r ${resource.color} rounded-lg`}>
                        <resource.icon className="w-6 h-6 text-white" />
                      </div>
                      <div>
                        <CardTitle className="text-lg">{resource.title}</CardTitle>
                        <Badge variant="secondary" className="mt-1">
                          {resource.type}
                        </Badge>
                      </div>
                    </div>
                  </div>
                </CardHeader>

                <CardContent className="space-y-4">
                  <CardDescription className="text-base">{resource.description}</CardDescription>

                  <div className="flex items-center justify-between text-sm text-gray-600">
                    <div className="flex items-center space-x-1">
                      <Clock className="w-4 h-4" />
                      <span>{resource.duration}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Star className="w-4 h-4 text-yellow-500" />
                      <span>{resource.rating}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Users className="w-4 h-4" />
                      <span>{resource.downloads.toLocaleString()}</span>
                    </div>
                  </div>

                  <div className="flex space-x-2">
                    <Button className={`flex-1 bg-gradient-to-r ${resource.color} hover:opacity-90 text-white`}>
                      <Download className="w-4 h-4 mr-2" />
                      Download
                    </Button>
                    <Button variant="outline" size="sm">
                      <ExternalLink className="w-4 h-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="guides" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {examGuides.map((guide, index) => (
              <Card key={index} className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
                <CardHeader>
                  <div className={`w-full h-3 bg-gradient-to-r ${guide.color} rounded-full mb-4`}></div>
                  <CardTitle className="text-xl">{guide.title}</CardTitle>
                  <CardDescription className="text-lg font-semibold text-gray-700">{guide.exam}</CardDescription>
                </CardHeader>

                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-semibold text-gray-800 mb-3">Key Topics:</h4>
                    <div className="space-y-2">
                      {guide.topics.map((topic, topicIndex) => (
                        <div key={topicIndex} className="flex items-center space-x-2">
                          <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                          <span className="text-sm text-gray-600">{topic}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-4 border-t">
                    <div className="text-sm text-gray-600">{guide.resources} resources available</div>
                    <Button className={`bg-gradient-to-r ${guide.color} hover:opacity-90 text-white`}>
                      <BookOpen className="w-4 h-4 mr-2" />
                      View Guide
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="cheatsheets" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {cheatSheets.map((sheet, index) => (
              <Card
                key={index}
                className="border-0 shadow-lg bg-white/90 backdrop-blur-sm hover:shadow-xl transition-all duration-300"
              >
                <CardHeader>
                  <CardTitle className="text-lg">{sheet.title}</CardTitle>
                  <CardDescription>{sheet.description}</CardDescription>
                </CardHeader>

                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <Badge variant="outline">{sheet.category}</Badge>
                    <div className="flex items-center space-x-1 text-sm text-gray-600">
                      <Download className="w-4 h-4" />
                      <span>{sheet.downloads.toLocaleString()}</span>
                    </div>
                  </div>

                  <Button className="w-full bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white">
                    <Download className="w-4 h-4 mr-2" />
                    Download PDF
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
