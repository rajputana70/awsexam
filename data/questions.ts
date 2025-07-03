import type { Question } from "@/types/question"

export const examQuestions: Question[] = [
  {
    id: 1,
    question:
      "A company needs to store frequently accessed data with high durability and availability. The data size is expected to grow to several terabytes. Which AWS storage service would be the most cost-effective solution?",
    options: [
      { id: "a", text: "Amazon EBS with General Purpose SSD (gp3)" },
      { id: "b", text: "Amazon S3 Standard" },
      { id: "c", text: "Amazon EFS" },
      { id: "d", text: "Amazon FSx for Windows File Server" },
    ],
    correctAnswer: "b",
    explanation:
      "Amazon S3 Standard provides high durability (99.999999999%) and availability, with virtually unlimited storage capacity and cost-effective pricing for frequently accessed data.",
    domain: "Design Resilient Architectures",
    difficulty: "Easy",
  },
  {
    id: 2,
    question:
      "An application running on EC2 instances needs to access AWS services securely without storing credentials in the application code. What is the best practice to achieve this?",
    options: [
      { id: "a", text: "Store AWS credentials in environment variables" },
      { id: "b", text: "Use IAM roles attached to EC2 instances" },
      { id: "c", text: "Hardcode AWS credentials in the application" },
      { id: "d", text: "Use AWS Systems Manager Parameter Store for credentials" },
    ],
    correctAnswer: "b",
    explanation:
      "IAM roles provide temporary credentials to EC2 instances, eliminating the need to store long-term credentials and following AWS security best practices.",
    domain: "Design Secure Applications",
    difficulty: "Easy",
  },
  {
    id: 3,
    question:
      "A web application experiences variable traffic with occasional spikes. Which AWS service combination would provide the most cost-effective auto-scaling solution?",
    options: [
      { id: "a", text: "Application Load Balancer + EC2 Auto Scaling + CloudWatch" },
      { id: "b", text: "Network Load Balancer + EC2 instances + CloudTrail" },
      { id: "c", text: "Classic Load Balancer + Reserved Instances + CloudFormation" },
      { id: "d", text: "API Gateway + Lambda functions + X-Ray" },
    ],
    correctAnswer: "a",
    explanation:
      "Application Load Balancer distributes traffic, EC2 Auto Scaling adjusts capacity based on demand, and CloudWatch provides monitoring metrics for scaling decisions.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 4,
    question:
      "A company wants to migrate their on-premises database to AWS with minimal downtime. The database is currently 2TB in size and growing. Which migration strategy would be most appropriate?",
    options: [
      { id: "a", text: "AWS Database Migration Service (DMS) with ongoing replication" },
      { id: "b", text: "Export database to S3 and import to RDS" },
      { id: "c", text: "Use AWS DataSync to copy database files" },
      { id: "d", text: "Create manual database backups and restore to RDS" },
    ],
    correctAnswer: "a",
    explanation:
      "AWS DMS provides continuous replication with minimal downtime, making it ideal for large database migrations while maintaining data consistency.",
    domain: "Design Resilient Architectures",
    difficulty: "Medium",
  },
  {
    id: 5,
    question:
      "An e-commerce application needs to process orders asynchronously to handle traffic spikes during sales events. Which AWS services would provide the best decoupled architecture?",
    options: [
      { id: "a", text: "Amazon SQS + AWS Lambda" },
      { id: "b", text: "Amazon SNS + Amazon EC2" },
      { id: "c", text: "Amazon Kinesis + Amazon EMR" },
      { id: "d", text: "AWS Step Functions + Amazon ECS" },
    ],
    correctAnswer: "a",
    explanation:
      "Amazon SQS provides reliable message queuing for decoupling, while Lambda offers serverless processing that automatically scales with demand.",
    domain: "Design Resilient Architectures",
    difficulty: "Medium",
  },
  {
    id: 6,
    question:
      "A company needs to ensure their multi-tier web application can survive the failure of an entire Availability Zone. What architectural approach should they implement?",
    options: [
      { id: "a", text: "Deploy all resources in a single AZ with backup instances" },
      { id: "b", text: "Deploy resources across multiple AZs with load balancing" },
      { id: "c", text: "Use only managed services that handle AZ failures automatically" },
      { id: "d", text: "Implement cross-region replication for all components" },
    ],
    correctAnswer: "b",
    explanation:
      "Deploying across multiple AZs with load balancing ensures high availability and fault tolerance at the AZ level, which is a fundamental AWS best practice.",
    domain: "Design Resilient Architectures",
    difficulty: "Easy",
  },
  {
    id: 7,
    question:
      "A media company needs to store and serve video content globally with low latency. Which combination of AWS services would be most effective?",
    options: [
      { id: "a", text: "Amazon S3 + Amazon CloudFront" },
      { id: "b", text: "Amazon EBS + Amazon EC2" },
      { id: "c", text: "Amazon EFS + Application Load Balancer" },
      { id: "d", text: "Amazon Glacier + Amazon Route 53" },
    ],
    correctAnswer: "a",
    explanation:
      "S3 provides durable storage for video content, while CloudFront's global edge locations ensure low-latency content delivery worldwide.",
    domain: "Design High-Performing Architectures",
    difficulty: "Easy",
  },
  {
    id: 8,
    question:
      "A financial services company requires encryption of data at rest and in transit for compliance. Which AWS service features should they prioritize?",
    options: [
      { id: "a", text: "AWS KMS for key management and SSL/TLS for data in transit" },
      { id: "b", text: "Amazon S3 server-side encryption only" },
      { id: "c", text: "VPC security groups and NACLs" },
      { id: "d", text: "AWS CloudTrail for audit logging" },
    ],
    correctAnswer: "a",
    explanation:
      "AWS KMS provides centralized key management for encryption at rest, while SSL/TLS ensures data is encrypted during transmission.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 9,
    question:
      "A startup wants to minimize costs while running a web application with unpredictable traffic patterns. Which EC2 pricing model would be most cost-effective?",
    options: [
      { id: "a", text: "On-Demand Instances only" },
      { id: "b", text: "Reserved Instances for all capacity" },
      { id: "c", text: "Spot Instances with Auto Scaling" },
      { id: "d", text: "A mix of Reserved, On-Demand, and Spot Instances" },
    ],
    correctAnswer: "d",
    explanation:
      "A mixed pricing strategy uses Reserved Instances for baseline capacity, On-Demand for predictable spikes, and Spot Instances for additional cost savings on flexible workloads.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Medium",
  },
  {
    id: 10,
    question:
      "An application needs to store session data that can be accessed by multiple EC2 instances. The data should persist beyond instance termination. Which service is most appropriate?",
    options: [
      { id: "a", text: "Amazon ElastiCache" },
      { id: "b", text: "Amazon EBS" },
      { id: "c", text: "Instance store volumes" },
      { id: "d", text: "Amazon S3" },
    ],
    correctAnswer: "a",
    explanation:
      "ElastiCache provides in-memory storage that can be shared across multiple instances and persists beyond individual instance lifecycles.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 11,
    question:
      "A company wants to implement a disaster recovery solution with an RTO of 4 hours and RPO of 1 hour. Which AWS disaster recovery strategy would meet these requirements most cost-effectively?",
    options: [
      { id: "a", text: "Backup and Restore" },
      { id: "b", text: "Pilot Light" },
      { id: "c", text: "Warm Standby" },
      { id: "d", text: "Multi-Site Active/Active" },
    ],
    correctAnswer: "b",
    explanation:
      "Pilot Light strategy maintains critical components running in AWS, allowing for recovery within hours while being more cost-effective than warm standby or multi-site approaches.",
    domain: "Design Resilient Architectures",
    difficulty: "Hard",
  },
  {
    id: 12,
    question:
      "A mobile application backend needs to handle authentication and provide secure API access. Which AWS services would provide a complete serverless authentication solution?",
    options: [
      { id: "a", text: "Amazon Cognito + API Gateway + Lambda" },
      { id: "b", text: "AWS IAM + EC2 + Application Load Balancer" },
      { id: "c", text: "AWS Directory Service + CloudFront + S3" },
      { id: "d", text: "Amazon RDS + ElastiCache + Route 53" },
    ],
    correctAnswer: "a",
    explanation:
      "Cognito handles user authentication, API Gateway manages API access with built-in authorization, and Lambda provides serverless compute for backend logic.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 13,
    question:
      "A data analytics company processes large datasets daily. They need a solution that can scale compute resources automatically based on workload demands. Which service combination would be most suitable?",
    options: [
      { id: "a", text: "Amazon EMR with Auto Scaling" },
      { id: "b", text: "Amazon EC2 with manual scaling" },
      { id: "c", text: "AWS Batch with managed compute environments" },
      { id: "d", text: "Amazon ECS with fixed capacity" },
    ],
    correctAnswer: "c",
    explanation:
      "AWS Batch automatically manages compute resources based on job queue demands, making it ideal for variable batch processing workloads.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 14,
    question:
      "A company needs to ensure that their AWS resources comply with specific security policies and automatically remediate non-compliant resources. Which AWS service would best address this requirement?",
    options: [
      { id: "a", text: "AWS Config with remediation actions" },
      { id: "b", text: "AWS CloudTrail with CloudWatch alarms" },
      { id: "c", text: "AWS Security Hub with manual reviews" },
      { id: "d", text: "AWS Inspector with scheduled assessments" },
    ],
    correctAnswer: "a",
    explanation:
      "AWS Config continuously monitors resource configurations against compliance rules and can automatically trigger remediation actions when non-compliance is detected.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 15,
    question:
      "An organization wants to optimize costs for their development and testing environments that are only used during business hours. What approach would provide the most cost savings?",
    options: [
      { id: "a", text: "Use Reserved Instances for all environments" },
      { id: "b", text: "Implement automated start/stop scheduling for resources" },
      { id: "c", text: "Use Spot Instances exclusively" },
      { id: "d", text: "Migrate all workloads to Lambda functions" },
    ],
    correctAnswer: "b",
    explanation:
      "Automated scheduling to start resources during business hours and stop them after hours can provide significant cost savings for non-production environments.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Easy",
  },
  {
    id: 16,
    question:
      "A web application experiences seasonal traffic spikes that are 10x normal load. The application uses a relational database. Which database solution would handle these spikes most effectively?",
    options: [
      { id: "a", text: "Amazon RDS with read replicas" },
      { id: "b", text: "Amazon Aurora Serverless" },
      { id: "c", text: "Amazon DynamoDB with on-demand billing" },
      { id: "d", text: "Amazon Redshift with elastic resize" },
    ],
    correctAnswer: "b",
    explanation:
      "Aurora Serverless automatically scales compute capacity based on demand, making it ideal for applications with unpredictable or intermittent workloads.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 17,
    question:
      "A company needs to share files securely between multiple AWS accounts within their organization. What is the most secure and efficient approach?",
    options: [
      { id: "a", text: "Create public S3 buckets with bucket policies" },
      { id: "b", text: "Use S3 Cross-Account Access with IAM roles" },
      { id: "c", text: "Set up VPN connections between accounts" },
      { id: "d", text: "Use AWS Direct Connect for all accounts" },
    ],
    correctAnswer: "b",
    explanation:
      "S3 Cross-Account Access with IAM roles provides secure, granular access control without exposing data publicly or requiring complex network configurations.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 18,
    question:
      "An application requires a database that can handle both OLTP and OLAP workloads with minimal operational overhead. Which AWS service would be most appropriate?",
    options: [
      { id: "a", text: "Amazon RDS with Multi-AZ deployment" },
      { id: "b", text: "Amazon Aurora with Aurora Analytics" },
      { id: "c", text: "Amazon Redshift with Redshift Spectrum" },
      { id: "d", text: "Amazon DynamoDB with DynamoDB Streams" },
    ],
    correctAnswer: "b",
    explanation:
      "Aurora can handle OLTP workloads efficiently, and Aurora Analytics (parallel query) enables OLAP queries on the same data without impacting transactional performance.",
    domain: "Design High-Performing Architectures",
    difficulty: "Hard",
  },
  {
    id: 19,
    question:
      "A company wants to implement a blue-green deployment strategy for their web application to minimize downtime during updates. Which AWS services would best support this approach?",
    options: [
      { id: "a", text: "AWS CodeDeploy with Auto Scaling Groups" },
      { id: "b", text: "AWS Elastic Beanstalk with environment swapping" },
      { id: "c", text: "Amazon ECS with service updates" },
      { id: "d", text: "All of the above can support blue-green deployments" },
    ],
    correctAnswer: "d",
    explanation:
      "All these services support blue-green deployment patterns: CodeDeploy has built-in blue-green support, Elastic Beanstalk allows environment swapping, and ECS supports rolling updates with blue-green strategies.",
    domain: "Design Resilient Architectures",
    difficulty: "Medium",
  },
  {
    id: 20,
    question:
      "A financial application requires audit trails for all API calls and data access. Which combination of AWS services would provide comprehensive auditing?",
    options: [
      { id: "a", text: "AWS CloudTrail + AWS Config + VPC Flow Logs" },
      { id: "b", text: "Amazon CloudWatch + AWS X-Ray" },
      { id: "c", text: "AWS Security Hub + Amazon GuardDuty" },
      { id: "d", text: "AWS Systems Manager + AWS Trusted Advisor" },
    ],
    correctAnswer: "a",
    explanation:
      "CloudTrail logs API calls, Config tracks resource changes, and VPC Flow Logs capture network traffic, providing comprehensive audit coverage.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 21,
    question:
      "A company needs to process streaming data in real-time and store it for both immediate analysis and long-term archival. Which architecture would be most cost-effective?",
    options: [
      { id: "a", text: "Kinesis Data Streams → Lambda → DynamoDB → S3 Glacier" },
      { id: "b", text: "Kinesis Data Firehose → S3 with lifecycle policies → Athena" },
      { id: "c", text: "SQS → EC2 → RDS → Redshift" },
      { id: "d", text: "MSK → EMR → ElastiCache → Aurora" },
    ],
    correctAnswer: "b",
    explanation:
      "Kinesis Data Firehose automatically delivers data to S3, lifecycle policies move old data to cheaper storage classes, and Athena enables serverless querying.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Hard",
  },
  {
    id: 22,
    question:
      "An application needs to encrypt sensitive data before storing it in a database. The encryption keys must be rotated automatically and access must be logged. Which AWS service provides these capabilities?",
    options: [
      { id: "a", text: "AWS KMS with automatic key rotation" },
      { id: "b", text: "AWS Secrets Manager with Lambda rotation" },
      { id: "c", text: "AWS Systems Manager Parameter Store" },
      { id: "d", text: "AWS Certificate Manager" },
    ],
    correctAnswer: "a",
    explanation:
      "AWS KMS provides automatic key rotation, comprehensive access logging through CloudTrail, and integrates with most AWS services for encryption.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 23,
    question:
      "A global application needs to route users to the nearest healthy endpoint based on geographic location and endpoint health. Which AWS service would provide this functionality?",
    options: [
      { id: "a", text: "Amazon Route 53 with geolocation and health checks" },
      { id: "b", text: "AWS Global Accelerator with endpoint groups" },
      { id: "c", text: "Amazon CloudFront with origin failover" },
      { id: "d", text: "Application Load Balancer with cross-zone load balancing" },
    ],
    correctAnswer: "a",
    explanation:
      "Route 53 geolocation routing directs users to the nearest endpoint, while health checks ensure traffic only goes to healthy endpoints.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 24,
    question:
      "A company wants to analyze their AWS costs and identify opportunities for optimization. Which AWS tools would provide the most comprehensive cost analysis?",
    options: [
      { id: "a", text: "AWS Cost Explorer + AWS Budgets + AWS Trusted Advisor" },
      { id: "b", text: "AWS CloudWatch + AWS Config" },
      { id: "c", text: "AWS Well-Architected Tool + AWS Systems Manager" },
      { id: "d", text: "AWS Security Hub + AWS Inspector" },
    ],
    correctAnswer: "a",
    explanation:
      "Cost Explorer provides detailed cost analysis, Budgets enable cost monitoring and alerts, and Trusted Advisor offers cost optimization recommendations.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Easy",
  },
  {
    id: 25,
    question:
      "An e-commerce platform needs to handle flash sales with sudden traffic spikes of 100x normal load. Which caching strategy would be most effective?",
    options: [
      { id: "a", text: "CloudFront + ElastiCache + Application-level caching" },
      { id: "b", text: "Only database read replicas" },
      { id: "c", text: "Only CloudFront CDN" },
      { id: "d", text: "Only ElastiCache Redis" },
    ],
    correctAnswer: "a",
    explanation:
      "Multi-layer caching with CloudFront for static content, ElastiCache for database queries, and application-level caching provides maximum performance and scalability.",
    domain: "Design High-Performing Architectures",
    difficulty: "Hard",
  },
  {
    id: 26,
    question:
      "A healthcare application must ensure that patient data is encrypted and access is restricted based on user roles. Which AWS services would provide the most comprehensive security solution?",
    options: [
      { id: "a", text: "AWS IAM + AWS KMS + Amazon Cognito + AWS CloudTrail" },
      { id: "b", text: "VPC Security Groups + NACLs" },
      { id: "c", text: "AWS WAF + AWS Shield" },
      { id: "d", text: "Amazon Inspector + AWS Config" },
    ],
    correctAnswer: "a",
    explanation:
      "IAM provides role-based access control, KMS handles encryption, Cognito manages user authentication, and CloudTrail provides audit logging for compliance.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 27,
    question:
      "A company needs to migrate a large amount of data (500TB) from on-premises to AWS with limited internet bandwidth. Which AWS service would be most efficient?",
    options: [
      { id: "a", text: "AWS Direct Connect" },
      { id: "b", text: "AWS Snowball Edge" },
      { id: "c", text: "AWS DataSync over internet" },
      { id: "d", text: "AWS Storage Gateway" },
    ],
    correctAnswer: "b",
    explanation:
      "AWS Snowball Edge is designed for large-scale data migration when internet bandwidth is limited, providing secure offline data transfer.",
    domain: "Design Resilient Architectures",
    difficulty: "Medium",
  },
  {
    id: 28,
    question:
      "An application requires a message queue that can handle millions of messages with exactly-once processing guarantees. Which AWS service would be most appropriate?",
    options: [
      { id: "a", text: "Amazon SQS Standard Queue" },
      { id: "b", text: "Amazon SQS FIFO Queue" },
      { id: "c", text: "Amazon SNS" },
      { id: "d", text: "Amazon Kinesis Data Streams" },
    ],
    correctAnswer: "b",
    explanation:
      "SQS FIFO queues provide exactly-once processing and maintain message order, which is essential for applications requiring guaranteed message delivery.",
    domain: "Design Resilient Architectures",
    difficulty: "Medium",
  },
  {
    id: 29,
    question:
      "A startup wants to minimize upfront costs while ensuring their application can scale. Which combination of AWS services would be most cost-effective for a new application?",
    options: [
      { id: "a", text: "AWS Lambda + API Gateway + DynamoDB" },
      { id: "b", text: "EC2 Reserved Instances + RDS Reserved Instances" },
      { id: "c", text: "ECS Fargate + Aurora Serverless" },
      { id: "d", text: "Elastic Beanstalk + RDS Multi-AZ" },
    ],
    correctAnswer: "a",
    explanation:
      "This serverless combination has no upfront costs, scales automatically, and charges only for actual usage, making it ideal for startups with unpredictable traffic.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Easy",
  },
  {
    id: 30,
    question:
      "A machine learning application needs to process large datasets stored in S3. The processing jobs run infrequently but require significant compute resources. Which solution would be most cost-effective?",
    options: [
      { id: "a", text: "Always-on EC2 instances" },
      { id: "b", text: "AWS Batch with Spot Instances" },
      { id: "c", text: "Amazon EMR with On-Demand instances" },
      { id: "d", text: "AWS Lambda with maximum memory allocation" },
    ],
    correctAnswer: "b",
    explanation:
      "AWS Batch manages the compute resources automatically, and Spot Instances provide significant cost savings for fault-tolerant batch processing workloads.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Medium",
  },
  {
    id: 31,
    question:
      "A company needs to ensure their web application remains available even if an entire AWS region becomes unavailable. What architecture approach should they implement?",
    options: [
      { id: "a", text: "Multi-AZ deployment within a single region" },
      { id: "b", text: "Multi-region deployment with Route 53 health checks" },
      { id: "c", text: "Auto Scaling across multiple AZs" },
      { id: "d", text: "CloudFront with multiple origins in the same region" },
    ],
    correctAnswer: "b",
    explanation:
      "Multi-region deployment ensures availability even during regional outages, while Route 53 health checks automatically route traffic to healthy regions.",
    domain: "Design Resilient Architectures",
    difficulty: "Hard",
  },
  {
    id: 32,
    question:
      "An application needs to store user-uploaded images and automatically generate thumbnails. Which serverless architecture would be most efficient?",
    options: [
      { id: "a", text: "S3 + Lambda (triggered by S3 events) + S3 for thumbnails" },
      { id: "b", text: "EC2 + SQS + Auto Scaling" },
      { id: "c", text: "ECS + Application Load Balancer" },
      { id: "d", text: "Elastic Beanstalk + RDS" },
    ],
    correctAnswer: "a",
    explanation:
      "S3 event notifications can trigger Lambda functions automatically when images are uploaded, providing a fully serverless and cost-effective solution.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 33,
    question:
      "A financial services company requires network isolation and dedicated hardware for compliance reasons. Which AWS service would meet these requirements?",
    options: [
      { id: "a", text: "VPC with private subnets" },
      { id: "b", text: "AWS Dedicated Hosts" },
      { id: "c", text: "AWS Outposts" },
      { id: "d", text: "AWS Local Zones" },
    ],
    correctAnswer: "b",
    explanation:
      "AWS Dedicated Hosts provide physical servers dedicated to a single customer, meeting compliance requirements for dedicated hardware and network isolation.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 34,
    question:
      "A company wants to implement Infrastructure as Code and ensure consistent deployments across multiple environments. Which AWS service would be most appropriate?",
    options: [
      { id: "a", text: "AWS CloudFormation" },
      { id: "b", text: "AWS Config" },
      { id: "c", text: "AWS Systems Manager" },
      { id: "d", text: "AWS Service Catalog" },
    ],
    correctAnswer: "a",
    explanation:
      "AWS CloudFormation enables Infrastructure as Code with templates that can be version-controlled and deployed consistently across multiple environments.",
    domain: "Design Resilient Architectures",
    difficulty: "Easy",
  },
  {
    id: 35,
    question:
      "An application experiences predictable traffic patterns with peak usage during business hours. Which EC2 pricing strategy would optimize costs?",
    options: [
      { id: "a", text: "On-Demand Instances for all capacity" },
      { id: "b", text: "Reserved Instances for baseline + On-Demand for peaks" },
      { id: "c", text: "Spot Instances for all capacity" },
      { id: "d", text: "Dedicated Instances for all capacity" },
    ],
    correctAnswer: "b",
    explanation:
      "Reserved Instances provide cost savings for predictable baseline capacity, while On-Demand instances handle peak traffic without long-term commitments.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Medium",
  },
  {
    id: 36,
    question:
      "A mobile application backend needs to handle user authentication, push notifications, and offline data synchronization. Which AWS services would provide a complete mobile backend solution?",
    options: [
      { id: "a", text: "Amazon Cognito + Amazon SNS + AWS AppSync" },
      { id: "b", text: "AWS IAM + Amazon SES + Amazon RDS" },
      { id: "c", text: "AWS Lambda + API Gateway + DynamoDB" },
      { id: "d", text: "Amazon EC2 + Amazon SQS + Amazon S3" },
    ],
    correctAnswer: "a",
    explanation:
      "Cognito handles authentication, SNS manages push notifications, and AppSync provides real-time data synchronization with offline capabilities.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 37,
    question:
      "A company needs to ensure that sensitive data in their database is encrypted and that database administrators cannot access the plaintext data. Which approach would provide the highest level of security?",
    options: [
      { id: "a", text: "RDS encryption with AWS managed keys" },
      { id: "b", text: "Application-level encryption with customer managed keys" },
      { id: "c", text: "Database-level encryption with transparent data encryption" },
      { id: "d", text: "File system encryption on the database server" },
    ],
    correctAnswer: "b",
    explanation:
      "Application-level encryption with customer-managed keys ensures that even database administrators cannot access plaintext data, providing the highest level of security.",
    domain: "Design Secure Applications",
    difficulty: "Hard",
  },
  {
    id: 38,
    question:
      "A video streaming application needs to deliver content globally with the lowest possible latency. Which AWS service combination would be most effective?",
    options: [
      { id: "a", text: "S3 + CloudFront + Route 53" },
      { id: "b", text: "EC2 + Application Load Balancer" },
      { id: "c", text: "EFS + CloudFront" },
      { id: "d", text: "Glacier + CloudFront" },
    ],
    correctAnswer: "a",
    explanation:
      "S3 stores video content, CloudFront's global edge locations provide low-latency delivery, and Route 53 routes users to the nearest edge location.",
    domain: "Design High-Performing Architectures",
    difficulty: "Easy",
  },
  {
    id: 39,
    question:
      "A company wants to implement a data lake architecture for analytics. They need to store structured, semi-structured, and unstructured data cost-effectively. Which AWS services would be most appropriate?",
    options: [
      { id: "a", text: "Amazon S3 + AWS Glue + Amazon Athena" },
      { id: "b", text: "Amazon RDS + Amazon Redshift" },
      { id: "c", text: "Amazon DynamoDB + Amazon ElastiCache" },
      { id: "d", text: "Amazon EFS + Amazon EMR" },
    ],
    correctAnswer: "a",
    explanation:
      "S3 provides cost-effective storage for all data types, Glue handles ETL and data cataloging, and Athena enables serverless querying of the data lake.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Medium",
  },
  {
    id: 40,
    question:
      "An application requires a database that can automatically scale read capacity based on demand while maintaining strong consistency for writes. Which AWS database service would be most suitable?",
    options: [
      { id: "a", text: "Amazon DynamoDB with Auto Scaling" },
      { id: "b", text: "Amazon Aurora with Auto Scaling read replicas" },
      { id: "c", text: "Amazon RDS with read replicas" },
      { id: "d", text: "Amazon Redshift with elastic resize" },
    ],
    correctAnswer: "b",
    explanation:
      "Aurora Auto Scaling automatically adjusts the number of read replicas based on demand while maintaining strong consistency for writes through the primary instance.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 41,
    question:
      "A company needs to implement a secure file transfer solution that allows external partners to upload files directly to S3 without providing AWS credentials. Which approach would be most secure?",
    options: [
      { id: "a", text: "S3 pre-signed URLs with expiration" },
      { id: "b", text: "Public S3 bucket with bucket policy" },
      { id: "c", text: "IAM users for each partner" },
      { id: "d", text: "S3 Transfer Acceleration" },
    ],
    correctAnswer: "a",
    explanation:
      "Pre-signed URLs provide temporary, secure access to S3 objects without requiring AWS credentials, and can be configured with expiration times for additional security.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 42,
    question:
      "A web application experiences sudden traffic spikes that can overwhelm the backend database. Which caching strategy would provide the best protection for the database?",
    options: [
      { id: "a", text: "CloudFront caching only" },
      { id: "b", text: "ElastiCache with write-through caching" },
      { id: "c", text: "ElastiCache with lazy loading and TTL" },
      { id: "d", text: "Database query result caching only" },
    ],
    correctAnswer: "c",
    explanation:
      "Lazy loading with TTL ensures that frequently accessed data is cached while preventing stale data issues, providing effective database protection during traffic spikes.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 43,
    question:
      "A company wants to ensure their AWS infrastructure follows security best practices and compliance requirements automatically. Which service would provide continuous compliance monitoring?",
    options: [
      { id: "a", text: "AWS Config with compliance rules" },
      { id: "b", text: "AWS CloudTrail with log analysis" },
      { id: "c", text: "AWS Security Hub with findings aggregation" },
      { id: "d", text: "AWS Well-Architected Tool" },
    ],
    correctAnswer: "a",
    explanation:
      "AWS Config continuously monitors resource configurations against compliance rules and can automatically detect and report non-compliant resources.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 44,
    question:
      "A startup needs to minimize operational overhead while running a containerized application with automatic scaling. Which AWS service would require the least management?",
    options: [
      { id: "a", text: "Amazon ECS with EC2 launch type" },
      { id: "b", text: "Amazon ECS with Fargate launch type" },
      { id: "c", text: "Amazon EKS with managed node groups" },
      { id: "d", text: "EC2 instances with Docker" },
    ],
    correctAnswer: "b",
    explanation:
      "ECS with Fargate is serverless, eliminating the need to manage underlying infrastructure while providing automatic scaling and container orchestration.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Easy",
  },
  {
    id: 45,
    question:
      "An application needs to process messages from a queue, but some messages require longer processing times. Which SQS feature would prevent message timeout issues?",
    options: [
      { id: "a", text: "Dead Letter Queues" },
      { id: "b", text: "Visibility Timeout extension" },
      { id: "c", text: "Message deduplication" },
      { id: "d", text: "Long polling" },
    ],
    correctAnswer: "b",
    explanation:
      "Visibility timeout extension allows applications to extend the processing time for messages that require longer processing, preventing premature message redelivery.",
    domain: "Design Resilient Architectures",
    difficulty: "Medium",
  },
  {
    id: 46,
    question:
      "A company wants to analyze their application logs in real-time to detect security threats and operational issues. Which AWS service combination would be most effective?",
    options: [
      { id: "a", text: "CloudWatch Logs + Kinesis Data Analytics + Lambda" },
      { id: "b", text: "S3 + Athena + QuickSight" },
      { id: "c", text: "CloudTrail + Config + Security Hub" },
      { id: "d", text: "X-Ray + CloudWatch + SNS" },
    ],
    correctAnswer: "a",
    explanation:
      "CloudWatch Logs collects logs, Kinesis Data Analytics processes streams in real-time, and Lambda can trigger automated responses to detected threats or issues.",
    domain: "Design Secure Applications",
    difficulty: "Hard",
  },
  {
    id: 47,
    question:
      "A media company needs to transcode video files uploaded by users. The transcoding jobs are CPU-intensive and can take several hours. Which solution would be most cost-effective?",
    options: [
      { id: "a", text: "Always-on EC2 instances with high CPU" },
      { id: "b", text: "AWS Batch with Spot Instances" },
      { id: "c", text: "AWS Lambda with maximum timeout" },
      { id: "d", text: "Amazon ECS with Reserved Instances" },
    ],
    correctAnswer: "b",
    explanation:
      "AWS Batch manages the compute resources for batch jobs, and Spot Instances provide significant cost savings for fault-tolerant, long-running tasks like video transcoding.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Medium",
  },
  {
    id: 48,
    question:
      "An e-commerce application needs to maintain shopping cart data that persists across user sessions and can be accessed quickly. Which storage solution would be most appropriate?",
    options: [
      { id: "a", text: "Amazon S3" },
      { id: "b", text: "Amazon DynamoDB" },
      { id: "c", text: "Amazon EFS" },
      { id: "d", text: "Amazon EBS" },
    ],
    correctAnswer: "b",
    explanation:
      "DynamoDB provides fast, predictable performance for session data with automatic scaling and built-in security features, making it ideal for shopping cart persistence.",
    domain: "Design High-Performing Architectures",
    difficulty: "Easy",
  },
  {
    id: 49,
    question:
      "A company needs to ensure that their multi-tier application can handle the failure of any single component without affecting user experience. Which architectural principle should they follow?",
    options: [
      { id: "a", text: "Implement redundancy at every tier" },
      { id: "b", text: "Use only managed AWS services" },
      { id: "c", text: "Deploy everything in a single AZ" },
      { id: "d", text: "Implement circuit breaker patterns and graceful degradation" },
    ],
    correctAnswer: "d",
    explanation:
      "Circuit breaker patterns prevent cascading failures, while graceful degradation ensures the application continues to function even when some components fail.",
    domain: "Design Resilient Architectures",
    difficulty: "Hard",
  },
  {
    id: 50,
    question:
      "A financial application requires audit logs to be stored immutably for 7 years for compliance. Which S3 storage configuration would meet this requirement most cost-effectively?",
    options: [
      { id: "a", text: "S3 Standard with versioning" },
      { id: "b", text: "S3 Glacier Deep Archive with Object Lock" },
      { id: "c", text: "S3 Intelligent-Tiering with lifecycle policies" },
      { id: "d", text: "S3 One Zone-IA with cross-region replication" },
    ],
    correctAnswer: "b",
    explanation:
      "S3 Glacier Deep Archive provides the lowest cost for long-term storage, while Object Lock ensures immutability for compliance requirements.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Medium",
  },
  {
    id: 51,
    question:
      "A company wants to implement a microservices architecture with service discovery and load balancing. Which AWS service combination would provide the most comprehensive solution?",
    options: [
      { id: "a", text: "ECS with Service Discovery + Application Load Balancer" },
      { id: "b", text: "EC2 with Route 53 + Classic Load Balancer" },
      { id: "c", text: "Lambda with API Gateway + CloudFront" },
      { id: "d", text: "EKS with Kubernetes services + Network Load Balancer" },
    ],
    correctAnswer: "a",
    explanation:
      "ECS Service Discovery automatically registers and deregisters services, while Application Load Balancer provides advanced routing capabilities for microservices.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 52,
    question:
      "An application needs to store configuration data that can be updated without redeploying the application. The data should be encrypted and access should be logged. Which AWS service would be most appropriate?",
    options: [
      { id: "a", text: "AWS Systems Manager Parameter Store" },
      { id: "b", text: "Amazon S3 with versioning" },
      { id: "c", text: "AWS Secrets Manager" },
      { id: "d", text: "Amazon DynamoDB" },
    ],
    correctAnswer: "a",
    explanation:
      "Systems Manager Parameter Store is designed for configuration data, provides encryption, access logging, and allows runtime updates without application redeployment.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 53,
    question:
      "A data processing pipeline needs to handle varying workloads throughout the day. During peak hours, it processes 10x more data than off-peak hours. Which compute solution would be most cost-effective?",
    options: [
      { id: "a", text: "Reserved Instances sized for peak capacity" },
      { id: "b", text: "Auto Scaling with a mix of On-Demand and Spot Instances" },
      { id: "c", text: "Lambda functions for all processing" },
      { id: "d", text: "Always-on EC2 instances sized for average load" },
    ],
    correctAnswer: "b",
    explanation:
      "Auto Scaling adjusts capacity based on demand, while mixing On-Demand and Spot Instances optimizes costs for variable workloads.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Medium",
  },
  {
    id: 54,
    question:
      "A web application needs to protect against DDoS attacks and common web exploits. Which AWS services would provide comprehensive protection?",
    options: [
      { id: "a", text: "AWS WAF + AWS Shield Advanced + CloudFront" },
      { id: "b", text: "Security Groups + NACLs + VPC" },
      { id: "c", text: "AWS Config + CloudTrail + GuardDuty" },
      { id: "d", text: "AWS Inspector + Systems Manager + Trusted Advisor" },
    ],
    correctAnswer: "a",
    explanation:
      "WAF protects against web exploits, Shield Advanced provides DDoS protection, and CloudFront adds an additional layer of protection at edge locations.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 55,
    question:
      "A company needs to migrate their on-premises Active Directory to AWS while maintaining existing user authentication for cloud applications. Which solution would provide seamless integration?",
    options: [
      { id: "a", text: "AWS Directory Service for Microsoft Active Directory" },
      { id: "b", text: "Amazon Cognito User Pools" },
      { id: "c", text: "AWS IAM with SAML federation" },
      { id: "d", text: "AWS Single Sign-On" },
    ],
    correctAnswer: "a",
    explanation:
      "AWS Directory Service for Microsoft Active Directory provides a fully managed Active Directory in AWS that can establish trust relationships with on-premises AD.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 56,
    question:
      "An IoT application collects data from thousands of devices and needs to process this data in real-time for anomaly detection. Which architecture would be most scalable?",
    options: [
      { id: "a", text: "IoT Core + Kinesis Data Streams + Lambda + DynamoDB" },
      { id: "b", text: "API Gateway + SQS + EC2 + RDS" },
      { id: "c", text: "Application Load Balancer + Auto Scaling + Aurora" },
      { id: "d", text: "CloudFront + S3 + Athena + QuickSight" },
    ],
    correctAnswer: "a",
    explanation:
      "IoT Core handles device connectivity, Kinesis streams the data, Lambda processes it in real-time, and DynamoDB provides fast storage for results.",
    domain: "Design High-Performing Architectures",
    difficulty: "Hard",
  },
  {
    id: 57,
    question:
      "A company wants to implement disaster recovery with an RTO of 1 hour and RPO of 15 minutes. Which strategy would meet these requirements?",
    options: [
      { id: "a", text: "Backup and Restore" },
      { id: "b", text: "Pilot Light" },
      { id: "c", text: "Warm Standby" },
      { id: "d", text: "Multi-Site Active/Active" },
    ],
    correctAnswer: "c",
    explanation:
      "Warm Standby maintains a scaled-down version of the production environment that can be quickly scaled up to meet the 1-hour RTO requirement.",
    domain: "Design Resilient Architectures",
    difficulty: "Hard",
  },
  {
    id: 58,
    question:
      "A machine learning application needs to store and serve model artifacts to inference endpoints globally with low latency. Which storage solution would be most effective?",
    options: [
      { id: "a", text: "S3 with CloudFront distribution" },
      { id: "b", text: "EFS with regional replication" },
      { id: "c", text: "EBS with snapshot sharing" },
      { id: "d", text: "FSx with Multi-AZ deployment" },
    ],
    correctAnswer: "a",
    explanation:
      "S3 provides durable storage for model artifacts, while CloudFront's global edge locations ensure low-latency access for inference endpoints worldwide.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 59,
    question:
      "A financial services company needs to ensure that all API calls are authenticated and authorized, with detailed logging for compliance. Which approach would be most comprehensive?",
    options: [
      { id: "a", text: "API Gateway with IAM authentication + CloudTrail logging" },
      { id: "b", text: "Application Load Balancer with SSL termination" },
      { id: "c", text: "CloudFront with signed URLs" },
      { id: "d", text: "WAF with rate limiting rules" },
    ],
    correctAnswer: "a",
    explanation:
      "API Gateway provides built-in authentication and authorization capabilities, while CloudTrail logs all API calls for compliance and audit purposes.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 60,
    question:
      "A company wants to optimize costs for their development environments that are used inconsistently throughout the week. Which approach would provide the maximum cost savings?",
    options: [
      { id: "a", text: "Use Reserved Instances for predictable savings" },
      { id: "b", text: "Implement automated resource scheduling and rightsizing" },
      { id: "c", text: "Use Spot Instances for all development workloads" },
      { id: "d", text: "Migrate everything to serverless architectures" },
    ],
    correctAnswer: "b",
    explanation:
      "Automated scheduling stops resources when not needed, while rightsizing ensures resources match actual requirements, maximizing cost savings for inconsistent usage patterns.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Medium",
  },
  {
    id: 61,
    question:
      "A social media application needs to handle viral content that can cause sudden traffic spikes of 1000x normal load. Which architecture would be most resilient?",
    options: [
      { id: "a", text: "Auto Scaling + CloudFront + ElastiCache + SQS" },
      { id: "b", text: "Fixed capacity EC2 instances + RDS" },
      { id: "c", text: "Lambda + API Gateway + DynamoDB" },
      { id: "d", text: "ECS with manual scaling + Aurora" },
    ],
    correctAnswer: "a",
    explanation:
      "This combination provides multiple layers of scaling and caching to handle extreme traffic spikes while maintaining performance and availability.",
    domain: "Design Resilient Architectures",
    difficulty: "Hard",
  },
  {
    id: 62,
    question:
      "A healthcare application must ensure that patient data is never stored in plaintext and that encryption keys are managed securely. Which approach provides the highest security?",
    options: [
      { id: "a", text: "Client-side encryption with AWS KMS" },
      { id: "b", text: "Server-side encryption with S3 managed keys" },
      { id: "c", text: "Database encryption with RDS managed keys" },
      { id: "d", text: "Application-level encryption with hardcoded keys" },
    ],
    correctAnswer: "a",
    explanation:
      "Client-side encryption ensures data is encrypted before it reaches AWS services, while KMS provides secure key management with audit trails and access controls.",
    domain: "Design Secure Applications",
    difficulty: "Hard",
  },
  {
    id: 63,
    question:
      "A gaming application needs to maintain real-time leaderboards for millions of players with sub-millisecond response times. Which database solution would be most appropriate?",
    options: [
      { id: "a", text: "Amazon RDS with read replicas" },
      { id: "b", text: "Amazon DynamoDB with DAX" },
      { id: "c", text: "Amazon Aurora with parallel query" },
      { id: "d", text: "Amazon Redshift with result caching" },
    ],
    correctAnswer: "b",
    explanation:
      "DynamoDB provides single-digit millisecond performance, while DAX (DynamoDB Accelerator) adds microsecond-level caching for ultra-low latency requirements.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 64,
    question:
      "A company needs to process sensitive financial data and wants to ensure that the processing environment is completely isolated from other AWS customers. Which solution would meet this requirement?",
    options: [
      { id: "a", text: "VPC with private subnets" },
      { id: "b", text: "AWS Dedicated Hosts" },
      { id: "c", text: "AWS Outposts" },
      { id: "d", text: "AWS Local Zones" },
    ],
    correctAnswer: "b",
    explanation:
      "AWS Dedicated Hosts provide physical isolation by dedicating entire physical servers to a single customer, ensuring no resource sharing with other AWS customers.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 65,
    question:
      "A data analytics company processes large datasets that are accessed frequently for the first month, then rarely accessed afterward. Which S3 storage strategy would be most cost-effective?",
    options: [
      { id: "a", text: "S3 Standard for all data" },
      { id: "b", text: "S3 Intelligent-Tiering with lifecycle policies" },
      { id: "c", text: "S3 Glacier for all data" },
      { id: "d", text: "S3 One Zone-IA for all data" },
    ],
    correctAnswer: "b",
    explanation:
      "S3 Intelligent-Tiering automatically moves data between access tiers based on usage patterns, while lifecycle policies can transition old data to cheaper storage classes.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Medium",
  },
  {
    id: 66,
    question:
      "A web application needs to handle file uploads up to 5GB in size. Users should be able to resume interrupted uploads. Which approach would be most reliable?",
    options: [
      { id: "a", text: "Direct upload to EC2 instance storage" },
      { id: "b", text: "S3 multipart upload with pre-signed URLs" },
      { id: "c", text: "Upload to EFS through Application Load Balancer" },
      { id: "d", text: "Stream upload through API Gateway" },
    ],
    correctAnswer: "b",
    explanation:
      "S3 multipart upload allows resumable uploads for large files, while pre-signed URLs provide secure direct upload to S3 without going through application servers.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 67,
    question:
      "A company wants to implement a CI/CD pipeline that automatically deploys code changes after running tests. Which AWS services would provide a complete solution?",
    options: [
      { id: "a", text: "CodeCommit + CodeBuild + CodeDeploy + CodePipeline" },
      { id: "b", text: "S3 + Lambda + CloudFormation" },
      { id: "c", text: "EC2 + Auto Scaling + CloudWatch" },
      { id: "d", text: "ECS + ECR + Application Load Balancer" },
    ],
    correctAnswer: "a",
    explanation:
      "This combination provides source control (CodeCommit), build and test automation (CodeBuild), deployment automation (CodeDeploy), and pipeline orchestration (CodePipeline).",
    domain: "Design Resilient Architectures",
    difficulty: "Medium",
  },
  {
    id: 68,
    question:
      "A mobile application backend needs to handle authentication, real-time messaging, and offline data synchronization. Which serverless architecture would be most suitable?",
    options: [
      { id: "a", text: "Cognito + API Gateway + Lambda + DynamoDB" },
      { id: "b", text: "Cognito + AppSync + Lambda + DynamoDB" },
      { id: "c", text: "IAM + SQS + EC2 + RDS" },
      { id: "d", text: "Directory Service + SNS + ECS + Aurora" },
    ],
    correctAnswer: "b",
    explanation:
      "Cognito handles authentication, AppSync provides real-time subscriptions and offline sync, Lambda handles business logic, and DynamoDB stores data.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 69,
    question:
      "A company needs to ensure that their backup data is protected against accidental deletion and ransomware attacks. Which backup strategy would provide the highest level of protection?",
    options: [
      { id: "a", text: "Daily snapshots stored in the same region" },
      { id: "b", text: "Cross-region backup with versioning and MFA delete" },
      { id: "c", text: "Local backup with encryption" },
      { id: "d", text: "Automated backup with 30-day retention" },
    ],
    correctAnswer: "b",
    explanation:
      "Cross-region backup protects against regional disasters, versioning protects against accidental deletion, and MFA delete prevents unauthorized deletion of backups.",
    domain: "Design Resilient Architectures",
    difficulty: "Hard",
  },
  {
    id: 70,
    question:
      "A streaming video platform needs to optimize costs for storing video content that has different access patterns. Popular videos are accessed frequently, while older content is rarely accessed. Which storage strategy would be most cost-effective?",
    options: [
      { id: "a", text: "Store all content in S3 Standard" },
      { id: "b", text: "Use S3 Intelligent-Tiering for automatic optimization" },
      { id: "c", text: "Store all content in S3 Glacier" },
      { id: "d", text: "Use CloudFront caching only" },
    ],
    correctAnswer: "b",
    explanation:
      "S3 Intelligent-Tiering automatically moves objects between access tiers based on usage patterns, optimizing costs without performance impact or operational overhead.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Medium",
  },
  {
    id: 71,
    question:
      "A financial trading application requires ultra-low latency for market data processing. Which AWS service combination would provide the lowest possible latency?",
    options: [
      { id: "a", text: "EC2 with enhanced networking + Placement Groups + SR-IOV" },
      { id: "b", text: "Lambda with provisioned concurrency" },
      { id: "c", text: "ECS Fargate with high CPU allocation" },
      { id: "d", text: "Auto Scaling with predictive scaling" },
    ],
    correctAnswer: "a",
    explanation:
      "Enhanced networking, cluster placement groups, and SR-IOV provide the lowest network latency and highest network performance for latency-sensitive applications.",
    domain: "Design High-Performing Architectures",
    difficulty: "Hard",
  },
  {
    id: 72,
    question:
      "A company wants to implement zero-trust security principles for their AWS infrastructure. Which combination of services would best support this approach?",
    options: [
      { id: "a", text: "VPC + Security Groups + NACLs" },
      { id: "b", text: "IAM + AWS SSO + GuardDuty + Config" },
      { id: "c", text: "WAF + Shield + CloudFront" },
      { id: "d", text: "KMS + Secrets Manager + Parameter Store" },
    ],
    correctAnswer: "b",
    explanation:
      "Zero-trust requires identity verification (IAM/SSO), continuous monitoring (GuardDuty), and compliance checking (Config) rather than relying on network perimeters.",
    domain: "Design Secure Applications",
    difficulty: "Hard",
  },
  {
    id: 73,
    question:
      "A SaaS application serves customers globally and needs to ensure data residency compliance in different regions. Which architecture approach would be most appropriate?",
    options: [
      { id: "a", text: "Single global deployment with data replication" },
      { id: "b", text: "Regional deployments with data isolation" },
      { id: "c", text: "Multi-AZ deployment in a single region" },
      { id: "d", text: "Edge locations with centralized data storage" },
    ],
    correctAnswer: "b",
    explanation:
      "Regional deployments with data isolation ensure that customer data remains within specific geographic boundaries to meet data residency requirements.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 74,
    question:
      "A company needs to migrate a legacy application that requires specific OS configurations and cannot be containerized. Which AWS service would be most suitable?",
    options: [
      { id: "a", text: "AWS Lambda" },
      { id: "b", text: "Amazon ECS" },
      { id: "c", text: "Amazon EC2" },
      { id: "d", text: "AWS Batch" },
    ],
    correctAnswer: "c",
    explanation:
      "EC2 provides full control over the operating system and allows custom configurations needed for legacy applications that cannot be modernized or containerized.",
    domain: "Design Resilient Architectures",
    difficulty: "Easy",
  },
  {
    id: 75,
    question:
      "A data processing pipeline needs to handle both batch and stream processing workloads cost-effectively. Which architecture would provide the most flexibility?",
    options: [
      { id: "a", text: "EMR for batch + Kinesis Analytics for streaming" },
      { id: "b", text: "Lambda for both batch and streaming" },
      { id: "c", text: "EC2 with custom applications" },
      { id: "d", text: "Glue for batch + Lambda for streaming" },
    ],
    correctAnswer: "a",
    explanation:
      "EMR provides cost-effective batch processing with auto-scaling, while Kinesis Analytics handles real-time stream processing, offering the best of both worlds.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Medium",
  },
  {
    id: 76,
    question:
      "A web application experiences seasonal traffic patterns with 6 months of high traffic and 6 months of low traffic. Which cost optimization strategy would be most effective?",
    options: [
      { id: "a", text: "Reserved Instances for the entire year" },
      { id: "b", text: "Scheduled Reserved Instances for high season + On-Demand for low season" },
      { id: "c", text: "Spot Instances for all capacity" },
      { id: "d", text: "On-Demand Instances for all capacity" },
    ],
    correctAnswer: "b",
    explanation:
      "Scheduled Reserved Instances provide cost savings during predictable high-traffic periods, while On-Demand instances offer flexibility during low-traffic periods.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Medium",
  },
  {
    id: 77,
    question:
      "A microservices application needs service mesh capabilities for traffic management, security, and observability. Which AWS service would provide these features?",
    options: [
      { id: "a", text: "AWS App Mesh" },
      { id: "b", text: "Application Load Balancer" },
      { id: "c", text: "API Gateway" },
      { id: "d", text: "CloudFront" },
    ],
    correctAnswer: "a",
    explanation:
      "AWS App Mesh provides service mesh capabilities including traffic routing, security policies, and observability features specifically designed for microservices architectures.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 78,
    question:
      "A company needs to ensure that their database backups are tested regularly and can be restored quickly in case of failure. Which approach would be most reliable?",
    options: [
      { id: "a", text: "Automated backups with manual testing" },
      { id: "b", text: "Automated backups with automated restore testing" },
      { id: "c", text: "Manual backups with documentation" },
      { id: "d", text: "Cross-region replication only" },
    ],
    correctAnswer: "b",
    explanation:
      "Automated restore testing ensures that backups are valid and can be restored successfully, reducing the risk of backup failures during actual disaster scenarios.",
    domain: "Design Resilient Architectures",
    difficulty: "Medium",
  },
  {
    id: 79,
    question:
      "A mobile gaming application needs to handle millions of concurrent users with real-time multiplayer features. Which architecture would provide the best scalability?",
    options: [
      { id: "a", text: "EC2 Auto Scaling + ElastiCache + RDS" },
      { id: "b", text: "API Gateway + Lambda + DynamoDB + ElastiCache" },
      { id: "c", text: "ECS + Application Load Balancer + Aurora" },
      { id: "d", text: "GameLift + DynamoDB + ElastiCache" },
    ],
    correctAnswer: "d",
    explanation:
      "GameLift is specifically designed for multiplayer gaming with automatic scaling, while DynamoDB and ElastiCache provide the performance needed for real-time gaming data.",
    domain: "Design High-Performing Architectures",
    difficulty: "Hard",
  },
  {
    id: 80,
    question:
      "A company wants to implement infrastructure monitoring that can automatically remediate common issues. Which AWS service combination would provide this capability?",
    options: [
      { id: "a", text: "CloudWatch + Systems Manager Automation + Lambda" },
      { id: "b", text: "Config + CloudTrail + SNS" },
      { id: "c", text: "X-Ray + CloudWatch Insights + SQS" },
      { id: "d", text: "GuardDuty + Security Hub + WAF" },
    ],
    correctAnswer: "a",
    explanation:
      "CloudWatch detects issues through alarms, Systems Manager Automation provides remediation workflows, and Lambda can execute custom remediation logic.",
    domain: "Design Resilient Architectures",
    difficulty: "Medium",
  },
  {
    id: 81,
    question:
      "A financial services company needs to implement data encryption that meets FIPS 140-2 Level 3 requirements. Which AWS service would meet this compliance requirement?",
    options: [
      { id: "a", text: "AWS KMS" },
      { id: "b", text: "AWS CloudHSM" },
      { id: "c", text: "AWS Secrets Manager" },
      { id: "d", text: "AWS Certificate Manager" },
    ],
    correctAnswer: "b",
    explanation:
      "AWS CloudHSM provides FIPS 140-2 Level 3 validated hardware security modules, meeting the highest cryptographic security standards required by financial services.",
    domain: "Design Secure Applications",
    difficulty: "Hard",
  },
  {
    id: 82,
    question:
      "A content delivery application needs to serve different content based on the user's device type and location. Which AWS service would provide this capability most efficiently?",
    options: [
      { id: "a", text: "CloudFront with Lambda@Edge" },
      { id: "b", text: "Application Load Balancer with host-based routing" },
      { id: "c", text: "API Gateway with request validation" },
      { id: "d", text: "Route 53 with weighted routing" },
    ],
    correctAnswer: "a",
    explanation:
      "CloudFront with Lambda@Edge allows content customization at edge locations based on request headers, providing the lowest latency for device and location-based content delivery.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 83,
    question:
      "A company wants to optimize their AWS costs by identifying unused resources and rightsizing opportunities. Which combination of tools would provide the most comprehensive cost optimization insights?",
    options: [
      { id: "a", text: "Cost Explorer + AWS Budgets + Trusted Advisor" },
      { id: "b", text: "CloudWatch + Config + Systems Manager" },
      { id: "c", text: "Well-Architected Tool + Security Hub" },
      { id: "d", text: "CloudTrail + GuardDuty + Inspector" },
    ],
    correctAnswer: "a",
    explanation:
      "Cost Explorer analyzes spending patterns, AWS Budgets provides cost monitoring and alerts, and Trusted Advisor identifies cost optimization opportunities including unused resources.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Easy",
  },
  {
    id: 84,
    question:
      "A data warehouse application needs to handle complex analytical queries on petabytes of data with the ability to scale compute independently from storage. Which AWS service would be most appropriate?",
    options: [
      { id: "a", text: "Amazon RDS" },
      { id: "b", text: "Amazon Redshift" },
      { id: "c", text: "Amazon Aurora" },
      { id: "d", text: "Amazon DynamoDB" },
    ],
    correctAnswer: "b",
    explanation:
      "Amazon Redshift is specifically designed for data warehousing with columnar storage, massively parallel processing, and the ability to scale compute and storage independently.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 85,
    question:
      "A company needs to ensure that their application can survive the complete failure of an AWS region. Which disaster recovery strategy would provide the fastest recovery time?",
    options: [
      { id: "a", text: "Backup and Restore" },
      { id: "b", text: "Pilot Light" },
      { id: "c", text: "Warm Standby" },
      { id: "d", text: "Multi-Site Active/Active" },
    ],
    correctAnswer: "d",
    explanation:
      "Multi-Site Active/Active runs identical workloads in multiple regions simultaneously, providing immediate failover with minimal to no downtime.",
    domain: "Design Resilient Architectures",
    difficulty: "Hard",
  },
  {
    id: 86,
    question:
      "A machine learning application needs to store and version large model files while providing fast access for training and inference. Which storage solution would be most suitable?",
    options: [
      { id: "a", text: "S3 with versioning and Transfer Acceleration" },
      { id: "b", text: "EFS with regional replication" },
      { id: "c", text: "EBS with snapshot sharing" },
      { id: "d", text: "FSx for Lustre with S3 integration" },
    ],
    correctAnswer: "a",
    explanation:
      "S3 provides unlimited storage with versioning for model management, while Transfer Acceleration ensures fast uploads and downloads for large model files.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 87,
    question:
      "A company wants to implement network segmentation to isolate different tiers of their application for security. Which AWS networking approach would be most effective?",
    options: [
      { id: "a", text: "Multiple VPCs with VPC peering" },
      { id: "b", text: "Single VPC with multiple subnets and security groups" },
      { id: "c", text: "Multiple AWS accounts with cross-account roles" },
      { id: "d", text: "Transit Gateway with route tables" },
    ],
    correctAnswer: "b",
    explanation:
      "A single VPC with multiple subnets provides network isolation, while security groups act as virtual firewalls to control traffic between application tiers.",
    domain: "Design Secure Applications",
    difficulty: "Medium",
  },
  {
    id: 88,
    question:
      "A startup needs to minimize operational overhead while running a web application that requires a database, caching, and file storage. Which combination would require the least management?",
    options: [
      { id: "a", text: "RDS + ElastiCache + S3" },
      { id: "b", text: "Aurora Serverless + DAX + S3" },
      { id: "c", text: "DynamoDB + ElastiCache + EFS" },
      { id: "d", text: "EC2 with self-managed databases" },
    ],
    correctAnswer: "b",
    explanation:
      "Aurora Serverless automatically scales database capacity, DAX provides managed caching for DynamoDB, and S3 is fully managed storage, minimizing operational overhead.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Medium",
  },
  {
    id: 89,
    question:
      "A video processing application needs to handle large file uploads and trigger processing workflows. Which serverless architecture would be most efficient?",
    options: [
      { id: "a", text: "S3 + Lambda + Step Functions + MediaConvert" },
      { id: "b", text: "EC2 + SQS + Auto Scaling + FFmpeg" },
      { id: "c", text: "ECS + Application Load Balancer + EFS" },
      { id: "d", text: "API Gateway + Lambda + RDS" },
    ],
    correctAnswer: "a",
    explanation:
      "S3 handles file uploads, Lambda triggers on upload events, Step Functions orchestrates the workflow, and MediaConvert provides managed video processing.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 90,
    question:
      "A company needs to implement a solution that automatically scales based on custom metrics like queue depth or API response time. Which AWS service would provide this capability?",
    options: [
      { id: "a", text: "EC2 Auto Scaling with CloudWatch custom metrics" },
      { id: "b", text: "Application Auto Scaling with target tracking" },
      { id: "c", text: "Predictive Scaling with machine learning" },
      { id: "d", text: "All of the above" },
    ],
    correctAnswer: "d",
    explanation:
      "All these services can scale based on custom metrics: EC2 Auto Scaling uses CloudWatch metrics, Application Auto Scaling supports various AWS services, and Predictive Scaling uses ML for forecasting.",
    domain: "Design High-Performing Architectures",
    difficulty: "Medium",
  },
  {
    id: 91,
    question:
      "A financial application requires that all data access is logged and that logs are tamper-proof for compliance auditing. Which logging strategy would meet these requirements?",
    options: [
      { id: "a", text: "CloudWatch Logs with log retention" },
      { id: "b", text: "CloudTrail with log file validation and S3 Object Lock" },
      { id: "c", text: "VPC Flow Logs with encryption" },
      { id: "d", text: "Application logs stored in RDS" },
    ],
    correctAnswer: "b",
    explanation:
      "CloudTrail provides comprehensive API logging, log file validation ensures integrity, and S3 Object Lock prevents tampering with log files for compliance requirements.",
    domain: "Design Secure Applications",
    difficulty: "Hard",
  },
  {
    id: 92,
    question:
      "A global e-commerce platform needs to provide consistent user experience regardless of geographic location while minimizing latency. Which architecture would be most effective?",
    options: [
      { id: "a", text: "Single region deployment with CloudFront" },
      { id: "b", text: "Multi-region deployment with Global Load Balancer" },
      { id: "c", text: "CloudFront + Regional edge caches + Multi-region origins" },
      { id: "d", text: "Local Zones in major cities" },
    ],
    correctAnswer: "c",
    explanation:
      "CloudFront provides global edge locations, regional edge caches improve cache hit ratios, and multi-region origins ensure high availability and performance worldwide.",
    domain: "Design High-Performing Architectures",
    difficulty: "Hard",
  },
  {
    id: 93,
    question:
      "A company wants to implement cost allocation and chargeback for different business units using AWS resources. Which approach would provide the most granular cost tracking?",
    options: [
      { id: "a", text: "Separate AWS accounts for each business unit" },
      { id: "b", text: "Resource tagging with cost allocation tags" },
      { id: "c", text: "AWS Organizations with consolidated billing" },
      { id: "d", text: "All of the above combined" },
    ],
    correctAnswer: "d",
    explanation:
      "Combining separate accounts, resource tagging, and Organizations provides the most comprehensive cost allocation and chargeback capabilities with multiple levels of granularity.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Medium",
  },
  {
    id: 94,
    question:
      "A real-time analytics application needs to process streaming data with exactly-once semantics and maintain state across processing nodes. Which AWS service would be most appropriate?",
    options: [
      { id: "a", text: "Kinesis Data Streams with Lambda" },
      { id: "b", text: "Kinesis Data Analytics for Apache Flink" },
      { id: "c", text: "SQS with Lambda" },
      { id: "d", text: "MSK with custom consumers" },
    ],
    correctAnswer: "b",
    explanation:
      "Kinesis Data Analytics for Apache Flink provides exactly-once processing semantics and stateful stream processing capabilities required for complex real-time analytics.",
    domain: "Design High-Performing Architectures",
    difficulty: "Hard",
  },
  {
    id: 95,
    question:
      "A company needs to ensure that their containerized applications can communicate securely across multiple AWS accounts and regions. Which networking solution would be most appropriate?",
    options: [
      { id: "a", text: "VPC Peering across accounts and regions" },
      { id: "b", text: "AWS Transit Gateway with cross-account sharing" },
      { id: "c", text: "AWS PrivateLink with cross-account access" },
      { id: "d", text: "Service mesh with mutual TLS authentication" },
    ],
    correctAnswer: "d",
    explanation:
      "Service mesh provides secure service-to-service communication with mutual TLS, traffic encryption, and policy enforcement across accounts and regions for containerized applications.",
    domain: "Design Secure Applications",
    difficulty: "Hard",
  },
  {
    id: 96,
    question:
      "A data science team needs a cost-effective solution for running Jupyter notebooks with access to large datasets stored in S3. Which approach would minimize costs while providing good performance?",
    options: [
      { id: "a", text: "Always-on EC2 instances with Jupyter" },
      { id: "b", text: "Amazon SageMaker Studio with lifecycle configurations" },
      { id: "c", text: "AWS Batch with Jupyter containers" },
      { id: "d", text: "Lambda with Jupyter kernels" },
    ],
    correctAnswer: "b",
    explanation:
      "SageMaker Studio provides managed Jupyter environments with automatic shutdown capabilities through lifecycle configurations, optimizing costs while maintaining performance and S3 integration.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Medium",
  },
  {
    id: 97,
    question:
      "A company needs to implement a solution that can automatically detect and respond to security threats in real-time. Which AWS service combination would provide comprehensive threat detection and response?",
    options: [
      { id: "a", text: "GuardDuty + Security Hub + Lambda + Systems Manager" },
      { id: "b", text: "CloudTrail + CloudWatch + SNS" },
      { id: "c", text: "Config + Inspector + Trusted Advisor" },
      { id: "d", text: "WAF + Shield + CloudFront" },
    ],
    correctAnswer: "a",
    explanation:
      "GuardDuty detects threats, Security Hub aggregates findings, Lambda processes alerts, and Systems Manager can execute automated remediation actions for comprehensive threat response.",
    domain: "Design Secure Applications",
    difficulty: "Hard",
  },
  {
    id: 98,
    question:
      "A media streaming company needs to optimize video delivery costs while maintaining quality. They serve content globally with varying popularity. Which strategy would be most cost-effective?",
    options: [
      { id: "a", text: "Store all content in S3 Standard with CloudFront" },
      { id: "b", text: "Use S3 Intelligent-Tiering with CloudFront and origin request policies" },
      { id: "c", text: "Store popular content in S3 Standard, archive old content in Glacier" },
      { id: "d", text: "Use multiple S3 storage classes with CloudFront caching policies" },
    ],
    correctAnswer: "b",
    explanation:
      "S3 Intelligent-Tiering automatically optimizes storage costs based on access patterns, while CloudFront with origin request policies ensures efficient content delivery and caching.",
    domain: "Design Cost-Optimized Architectures",
    difficulty: "Hard",
  },
  {
    id: 99,
    question:
      "A high-frequency trading application requires the absolute lowest network latency between compute instances. Which AWS configuration would provide the best performance?",
    options: [
      { id: "a", text: "EC2 instances in the same AZ with enhanced networking" },
      { id: "b", text: "EC2 instances in a cluster placement group with SR-IOV" },
      { id: "c", text: "EC2 instances with dedicated tenancy and enhanced networking" },
      { id: "d", text: "All of the above combined" },
    ],
    correctAnswer: "d",
    explanation:
      "Combining cluster placement groups, enhanced networking, SR-IOV, and dedicated tenancy provides the absolute lowest latency and highest network performance for latency-critical applications.",
    domain: "Design High-Performing Architectures",
    difficulty: "Hard",
  },
  {
    id: 100,
    question:
      "A company wants to implement a comprehensive backup and disaster recovery strategy that meets a 4-hour RTO and 1-hour RPO across multiple failure scenarios. Which combination of strategies would be most appropriate?",
    options: [
      { id: "a", text: "Cross-region automated backups + Pilot light DR + Infrastructure as Code" },
      { id: "b", text: "Local backups + Manual restore procedures" },
      { id: "c", text: "Multi-AZ deployment + Read replicas" },
      { id: "d", text: "Snapshot-based backups + CloudFormation templates" },
    ],
    correctAnswer: "a",
    explanation:
      "Cross-region backups protect against regional failures, pilot light DR enables 4-hour RTO, automated backups meet 1-hour RPO, and Infrastructure as Code ensures consistent recovery environments.",
    domain: "Design Resilient Architectures",
    difficulty: "Hard",
  },
]
