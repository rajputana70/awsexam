import type { Question } from "@/types/question"
import { examQuestions } from "./questions"

// Developer Associate Questions
const dvaQuestions: Question[] = [
  {
    id: 1,
    question:
      "A developer is building a serverless web application using AWS Lambda and needs to store user session data. Which AWS service would be most appropriate for this use case?",
    options: [
      { id: "a", text: "Amazon RDS" },
      { id: "b", text: "Amazon DynamoDB" },
      { id: "c", text: "Amazon S3" },
      { id: "d", text: "Amazon EFS" },
    ],
    correctAnswer: "b",
    explanation:
      "DynamoDB is ideal for serverless applications as it provides fast, predictable performance with seamless scaling, making it perfect for storing session data in Lambda functions.",
    domain: "Development with AWS Services",
    difficulty: "Easy",
  },
  {
    id: 2,
    question:
      "A developer needs to deploy a Node.js application that can automatically scale based on demand. Which AWS service would require the least operational overhead?",
    options: [
      { id: "a", text: "Amazon EC2 with Auto Scaling" },
      { id: "b", text: "AWS Elastic Beanstalk" },
      { id: "c", text: "Amazon ECS" },
      { id: "d", text: "AWS Lambda" },
    ],
    correctAnswer: "b",
    explanation:
      "Elastic Beanstalk handles deployment, monitoring, and scaling automatically while allowing developers to focus on writing code rather than managing infrastructure.",
    domain: "Deployment",
    difficulty: "Easy",
  },
  // Add more DVA questions here...
]

// SysOps Administrator Questions
const soaQuestions: Question[] = [
  {
    id: 1,
    question:
      "A SysOps administrator needs to monitor EC2 instances and receive alerts when CPU utilization exceeds 80%. Which AWS services should be used?",
    options: [
      { id: "a", text: "CloudWatch + SNS" },
      { id: "b", text: "CloudTrail + SES" },
      { id: "c", text: "Config + Lambda" },
      { id: "d", text: "X-Ray + SQS" },
    ],
    correctAnswer: "a",
    explanation:
      "CloudWatch monitors metrics like CPU utilization and can trigger alarms, while SNS can send notifications when thresholds are breached.",
    domain: "Monitoring, Logging, and Remediation",
    difficulty: "Easy",
  },
  // Add more SOA questions here...
]

// Cloud Practitioner Questions
const clfQuestions: Question[] = [
  {
    id: 1,
    question: "Which AWS service provides a fully managed NoSQL database?",
    options: [
      { id: "a", text: "Amazon RDS" },
      { id: "b", text: "Amazon DynamoDB" },
      { id: "c", text: "Amazon Redshift" },
      { id: "d", text: "Amazon Aurora" },
    ],
    correctAnswer: "b",
    explanation:
      "Amazon DynamoDB is a fully managed NoSQL database service that provides fast and predictable performance with seamless scalability.",
    domain: "Technology",
    difficulty: "Easy",
  },
  // Add more CLF questions here...
]

// Professional Level Questions
const sapQuestions: Question[] = [
  {
    id: 1,
    question:
      "A large enterprise needs to implement a multi-account strategy with centralized billing and governance. They require different environments for development, staging, and production across multiple business units. Which AWS service combination would best address these requirements?",
    options: [
      { id: "a", text: "AWS Organizations + AWS Control Tower + AWS Config" },
      { id: "b", text: "AWS IAM + AWS CloudFormation + AWS Trusted Advisor" },
      { id: "c", text: "AWS Directory Service + AWS SSO + AWS Systems Manager" },
      { id: "d", text: "AWS Resource Groups + AWS Cost Explorer + AWS Budgets" },
    ],
    correctAnswer: "a",
    explanation:
      "AWS Organizations provides centralized account management and billing, Control Tower offers governance guardrails, and Config ensures compliance across all accounts.",
    domain: "Design Solutions for Organizational Complexity",
    difficulty: "Hard",
  },
  // Add more SAP questions here...
]

const dopQuestions: Question[] = [
  {
    id: 1,
    question:
      "A DevOps team needs to implement a CI/CD pipeline that automatically tests code, builds Docker images, and deploys to multiple environments with approval gates. Which AWS services would provide the most comprehensive solution?",
    options: [
      { id: "a", text: "CodeCommit + CodeBuild + CodeDeploy + CodePipeline" },
      { id: "b", text: "GitHub + Jenkins + Docker Hub + ECS" },
      { id: "c", text: "GitLab + AWS Batch + ECR + EKS" },
      { id: "d", text: "Bitbucket + CodeStar + Lambda + API Gateway" },
    ],
    correctAnswer: "a",
    explanation:
      "AWS CodePipeline orchestrates the entire CI/CD workflow, integrating with CodeCommit for source control, CodeBuild for testing and building, and CodeDeploy for deployment with built-in approval mechanisms.",
    domain: "SDLC Automation",
    difficulty: "Medium",
  },
  // Add more DOP questions here...
]

export const allExamData: Record<string, Question[]> = {
  "SAA-C03": examQuestions,
  "DVA-C01": dvaQuestions,
  "SOA-C02": soaQuestions,
  "CLF-C01": clfQuestions,
  "SAP-C02": sapQuestions,
  "DOP-C02": dopQuestions,
}
