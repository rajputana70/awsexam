import sys
import datetime
import os
from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash
from random import sample

# Database connection
db_url = os.environ.get('DATABASE_URL')
engine = create_engine(db_url)

# Helper function to execute SQL statements
def execute_sql(sql, params=None):
    with engine.connect() as conn:
        if params:
            result = conn.execute(text(sql), params)
        else:
            result = conn.execute(text(sql))
        conn.commit()
        return result

# Create admin user
def create_admin_user():
    # Check if admin already exists
    result = execute_sql("SELECT id FROM \"user\" WHERE username='admin' LIMIT 1")
    rows = result.fetchall()
    if len(rows) > 0:
        print("Admin user already exists")
        return
    
    # Create admin user
    admin_sql = """
    INSERT INTO "user" (username, email, password_hash, created_at, is_admin) 
    VALUES (:username, :email, :password_hash, :created_at, :is_admin)
    """
    admin_params = {
        'username': 'admin',
        'email': 'admin@example.com',
        'password_hash': generate_password_hash('adminpassword'),
        'created_at': datetime.datetime.utcnow(),
        'is_admin': True
    }
    execute_sql(admin_sql, admin_params)
    print("Admin user created")

# Create question categories
def create_categories():
    categories = [
        {
            'name': 'Design Secure Architectures',
            'description': 'Questions about designing secure AWS architectures, including access controls, secure workloads, and data security.',
        },
        {
            'name': 'Design Resilient Architectures',
            'description': 'Questions about creating scalable, loosely coupled, highly available, and fault-tolerant architectures.',
        },
        {
            'name': 'Design High-Performing Architectures',
            'description': 'Questions about high-performance storage, compute, database, and networking solutions.',
        },
        {
            'name': 'Design Cost-Optimized Architectures',
            'description': 'Questions about cost-effective storage, compute, database, and networking solutions.',
        }
    ]
    
    category_ids = {}
    
    for category in categories:
        # Check if category exists
        result = execute_sql("SELECT id FROM question_category WHERE name=:name LIMIT 1", 
                            {'name': category['name']})
        rows = result.fetchall()
        if len(rows) == 0:
            # Create new category
            sql = """
            INSERT INTO question_category (name, description) 
            VALUES (:name, :description) RETURNING id
            """
            result = execute_sql(sql, category)
            row = result.fetchone()
            category_ids[category['name']] = row[0]
            print(f"Category created: {category['name']}")
        else:
            # Get existing category id
            category_ids[category['name']] = rows[0][0]
            print(f"Category already exists: {category['name']}")
    
    return category_ids

# Create secure architecture questions (batch 1)
def create_secure_architecture_questions(category_id):
    questions = [
        {
            "question_text": "A company needs to restrict access to its S3 buckets to users connecting from the corporate network. Which combination of AWS services and features should be used?",
            "explanation": "S3 bucket policies can restrict access based on the source IP address. By combining this with a VPC endpoint for S3, you can ensure that access is only allowed from the corporate network through the VPC. AWS PrivateLink enhances this by providing private connectivity.",
            "difficulty": "medium",
            "options": [
                {"option_text": "S3 bucket policy with IP-based restrictions and VPC endpoint for S3", "is_correct": True},
                {"option_text": "S3 bucket ACLs with IAM roles and CloudFront distributions", "is_correct": False},
                {"option_text": "S3 bucket server-side encryption with customer-managed KMS keys", "is_correct": False},
                {"option_text": "S3 access points with cross-region replication and MFA Delete", "is_correct": False}
            ]
        },
        {
            "question_text": "A Solutions Architect is designing a multi-account AWS structure using AWS Organizations. Which feature would allow centralized control of allowed actions across all accounts?",
            "explanation": "Service Control Policies (SCPs) in AWS Organizations provide centralized control over the maximum available permissions for all accounts in your organization. SCPs limit permissions for IAM users and roles in member accounts, including the root user.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Service Control Policies (SCPs)", "is_correct": True},
                {"option_text": "IAM Permission Boundaries", "is_correct": False},
                {"option_text": "AWS Shield Standard protection", "is_correct": False},
                {"option_text": "AWS Config Rules", "is_correct": False}
            ]
        },
        {
            "question_text": "A company wants to implement a solution that securely stores application secrets and provides centralized rotation policies. Which AWS service should they use?",
            "explanation": "AWS Secrets Manager helps you protect secrets needed to access your applications, services, and IT resources. It enables you to easily rotate, manage, and retrieve database credentials, API keys, and other secrets throughout their lifecycle.",
            "difficulty": "easy",
            "options": [
                {"option_text": "AWS Secrets Manager", "is_correct": True},
                {"option_text": "AWS Parameter Store", "is_correct": False},
                {"option_text": "Amazon Cognito", "is_correct": False},
                {"option_text": "AWS Shield", "is_correct": False}
            ]
        },
        {
            "question_text": "A company is implementing multi-factor authentication (MFA) for its AWS account. Which two options can be combined for a valid MFA configuration?",
            "explanation": "AWS supports virtual MFA devices (like Google Authenticator) and hardware MFA devices (like YubiKey security keys) as valid forms of MFA. Virtual MFA device apps conform to RFC 6238 (TOTP), while hardware YubiKey devices enable FIDO security keys for MFA.",
            "difficulty": "easy",
            "options": [
                {"option_text": "Virtual MFA device app and hardware FIDO security key", "is_correct": True},
                {"option_text": "SMS text message and email verification code", "is_correct": False},
                {"option_text": "Amazon Cognito user pool and AWS Shield Advanced", "is_correct": False},
                {"option_text": "Amazon SNS notification and AWS Trusted Advisor check", "is_correct": False}
            ]
        },
        {
            "question_text": "A company needs to implement a solution that allows their developers to access AWS resources without the need to manage long-term credentials. What should they implement?",
            "explanation": "IAM Roles provide temporary security credentials that applications can use when making requests. Federation allows users to assume IAM roles temporarily using existing corporate credentials, eliminating the need to manage long-term AWS credentials.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Federated identity with IAM roles", "is_correct": True},
                {"option_text": "IAM users with access keys rotated manually", "is_correct": False},
                {"option_text": "AWS account root user credentials shared among developers", "is_correct": False},
                {"option_text": "Embedded access keys in application code", "is_correct": False}
            ]
        }
    ]
    
    insert_questions(questions, category_id)

# Create secure architecture questions (batch 2)
def create_secure_architecture_questions_batch2(category_id):
    questions = [
        {
            "question_text": "An application running on EC2 instances needs to securely store and rotate API credentials for a third-party service. What is the MOST secure approach?",
            "explanation": "AWS Secrets Manager is specifically designed to manage API credentials and other secrets. It provides automatic rotation capability and integration with Lambda for custom rotation logic. EC2 instances can retrieve secrets from Secrets Manager as needed, ensuring the credentials are never stored locally.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Use AWS Secrets Manager with automatic rotation configured", "is_correct": True},
                {"option_text": "Store credentials in environment variables within the EC2 instances", "is_correct": False},
                {"option_text": "Hardcode the credentials in the application code", "is_correct": False},
                {"option_text": "Store the credentials in an EBS volume with server-side encryption", "is_correct": False}
            ]
        },
        {
            "question_text": "A Solutions Architect is designing a VPC network. Which combination of security controls will provide the MOST defense in depth?",
            "explanation": "Defense in depth involves multiple layers of security controls. Security groups act as a stateful firewall at the instance level, network ACLs provide stateless filtering at the subnet level, and VPC Flow Logs provide visibility into network traffic for monitoring and auditing.",
            "difficulty": "hard",
            "options": [
                {"option_text": "Security groups, network ACLs, and VPC Flow Logs", "is_correct": True},
                {"option_text": "Security groups, route tables, and Internet Gateway", "is_correct": False},
                {"option_text": "Network ACLs, IAM policies, and NAT Gateway", "is_correct": False},
                {"option_text": "VPC endpoints, VPC peering, and transit gateway", "is_correct": False}
            ]
        },
        {
            "question_text": "A company wants to protect its web application from SQL injection and cross-site scripting attacks. Which AWS service should they implement?",
            "explanation": "AWS WAF is a web application firewall that helps protect web applications from common web exploits like SQL injection and cross-site scripting. It allows you to define customizable security rules that control which traffic reaches your applications.",
            "difficulty": "easy",
            "options": [
                {"option_text": "AWS WAF", "is_correct": True},
                {"option_text": "AWS Shield Standard", "is_correct": False},
                {"option_text": "Amazon Inspector", "is_correct": False},
                {"option_text": "AWS Network Firewall", "is_correct": False}
            ]
        },
        {
            "question_text": "A Solutions Architect needs to encrypt data on an Amazon RDS for PostgreSQL database. When should the encryption be configured?",
            "explanation": "Amazon RDS encryption must be enabled when the database instance is created. It cannot be added to an existing database instance. To encrypt an existing database, you must create a snapshot, make an encrypted copy of that snapshot, and then restore from the encrypted snapshot.",
            "difficulty": "medium",
            "options": [
                {"option_text": "When the database instance is created", "is_correct": True},
                {"option_text": "After the database instance is created, using the modify instance option", "is_correct": False},
                {"option_text": "After creating the first database within the instance", "is_correct": False},
                {"option_text": "When the first user is created in the database", "is_correct": False}
            ]
        },
        {
            "question_text": "A company needs to control access to specific AWS resources based on the source IP address of their corporate office. Which AWS feature should they use?",
            "explanation": "IAM policy conditions allow you to add additional constraints to policies, such as restricting access based on source IP addresses. The IpAddress condition operator can be used to limit actions to specific IP ranges, making it the most appropriate choice.",
            "difficulty": "medium",
            "options": [
                {"option_text": "IAM policy conditions with the IpAddress condition operator", "is_correct": True},
                {"option_text": "AWS Shield with custom network ACL rules", "is_correct": False},
                {"option_text": "VPC Flow Logs with CloudWatch alarms", "is_correct": False},
                {"option_text": "Route 53 health checks with geolocation routing", "is_correct": False}
            ]
        }
    ]
    
    insert_questions(questions, category_id)
    
# Create secure architecture questions (batch 3)
def create_secure_architecture_questions_batch3(category_id):
    questions = [
        {
            "question_text": "A company is storing sensitive customer data in an Amazon S3 bucket. Which combination of AWS features should they implement to enhance security?",
            "explanation": "S3 bucket policies restrict access to specific resources, S3 server-side encryption protects data at rest, S3 access logs provide detailed access records, and AWS CloudTrail tracks all API calls for auditing and compliance purposes. Together, these provide comprehensive security for sensitive data.",
            "difficulty": "medium",
            "options": [
                {"option_text": "S3 bucket policies, server-side encryption, S3 access logs, and AWS CloudTrail", "is_correct": True},
                {"option_text": "S3 bucket policies, client-side encryption, VPC endpoints, and AWS Trusted Advisor", "is_correct": False},
                {"option_text": "S3 bucket ACLs, AWS Shield, AWS WAF, and Amazon Inspector", "is_correct": False},
                {"option_text": "S3 bucket ACLs, AWS Firewall Manager, AWS Config, and Amazon Macie", "is_correct": False}
            ]
        },
        {
            "question_text": "A Solutions Architect is designing a new workload where EC2 instances need to access an S3 bucket, but all traffic must remain within the AWS network. How should this be achieved?",
            "explanation": "A VPC endpoint for S3 allows EC2 instances in a VPC to access S3 without requiring an internet gateway, NAT device, VPN connection, or AWS Direct Connect connection. All traffic between the VPC and S3 stays within the AWS network and doesn't traverse the public internet.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Create a VPC endpoint for S3", "is_correct": True},
                {"option_text": "Use an Internet Gateway with a route to S3", "is_correct": False},
                {"option_text": "Configure a NAT Gateway with an elastic IP", "is_correct": False},
                {"option_text": "Set up an AWS Direct Connect connection to S3", "is_correct": False}
            ]
        },
        {
            "question_text": "A security team needs to capture a complete history of all API calls made in their AWS account for security analysis and troubleshooting. Which service should they use?",
            "explanation": "AWS CloudTrail records API calls for your account and delivers log files to your specified S3 bucket. These logs contain detailed information about each call, including who made the call, when it was made, and from which IP address, making it the best tool for API call auditing.",
            "difficulty": "easy",
            "options": [
                {"option_text": "AWS CloudTrail", "is_correct": True},
                {"option_text": "Amazon CloudWatch Logs", "is_correct": False},
                {"option_text": "VPC Flow Logs", "is_correct": False},
                {"option_text": "AWS Config", "is_correct": False}
            ]
        },
        {
            "question_text": "A company needs to ensure that all their S3 buckets are encrypted and not publicly accessible. What is the most efficient way to enforce and monitor this across multiple AWS accounts?",
            "explanation": "AWS Organizations with Service Control Policies (SCPs) can enforce encryption and block public access settings across all accounts. AWS Config rules can monitor compliance with these policies continuously, and Security Hub provides a comprehensive view of the security posture across multiple accounts.",
            "difficulty": "hard",
            "options": [
                {"option_text": "Use AWS Organizations with SCPs, AWS Config rules, and AWS Security Hub", "is_correct": True},
                {"option_text": "Manually check each S3 bucket setting in each account", "is_correct": False},
                {"option_text": "Create an AWS Lambda function to modify bucket settings when created", "is_correct": False},
                {"option_text": "Use Amazon Macie to detect public buckets and unencrypted data", "is_correct": False}
            ]
        },
        {
            "question_text": "A company is developing a new application that requires temporary, limited-privilege security credentials for users. Which AWS service should they use?",
            "explanation": "AWS Security Token Service (STS) provides temporary security credentials for users who have been authenticated by an identity provider. These credentials expire after a specified time period, reducing the risk associated with long-term credentials while allowing fine-grained access control.",
            "difficulty": "medium",
            "options": [
                {"option_text": "AWS Security Token Service (STS)", "is_correct": True},
                {"option_text": "AWS Key Management Service (KMS)", "is_correct": False},
                {"option_text": "AWS Certificate Manager (ACM)", "is_correct": False},
                {"option_text": "AWS Artifact", "is_correct": False}
            ]
        },
        {
            "question_text": "A company wants to ensure that their Amazon RDS database is protected against unauthorized access. Which security measure does NOT provide protection for the database?",
            "explanation": "Amazon GuardDuty is a threat detection service that monitors for malicious activity across your AWS accounts and workloads, but it doesn't directly protect RDS databases. The other options all provide protection: security groups control access, encryption protects data, and IAM policies control who can manage the database.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Amazon GuardDuty", "is_correct": True},
                {"option_text": "Security groups restricting access to the database", "is_correct": False},
                {"option_text": "Encryption of data at rest using AWS KMS", "is_correct": False},
                {"option_text": "IAM database authentication", "is_correct": False}
            ]
        },
        {
            "question_text": "A company needs to ensure that critical data in their application is encrypted both in transit and at rest. Which combination of AWS services should they use?",
            "explanation": "AWS KMS provides managed encryption keys that can be used by other AWS services, AWS Certificate Manager provides SSL/TLS certificates for encryption in transit, and DynamoDB and S3 offer native integration with KMS for server-side encryption of data at rest.",
            "difficulty": "medium",
            "options": [
                {"option_text": "AWS KMS, AWS Certificate Manager, Amazon DynamoDB with encryption, and Amazon S3 with encryption", "is_correct": True},
                {"option_text": "AWS WAF, Amazon CloudFront, Amazon API Gateway, and AWS Shield", "is_correct": False},
                {"option_text": "AWS IAM, Amazon Cognito, AWS Security Hub, and AWS Control Tower", "is_correct": False},
                {"option_text": "Amazon Inspector, AWS Config, AWS CloudTrail, and AWS Trusted Advisor", "is_correct": False}
            ]
        }
    ]
    
    insert_questions(questions, category_id)

# Create resilient architecture questions (batch 1)
def create_resilient_architecture_questions(category_id):
    questions = [
        {
            "question_text": "A company runs a stateless web application across multiple Availability Zones. Which AWS service should they use to distribute traffic for maximum availability?",
            "explanation": "An Application Load Balancer automatically distributes traffic across multiple targets, such as EC2 instances, in multiple Availability Zones. It continuously monitors the health of registered targets and routes traffic only to healthy targets, providing high availability.",
            "difficulty": "easy",
            "options": [
                {"option_text": "Application Load Balancer", "is_correct": True},
                {"option_text": "CloudFront with S3 Origin", "is_correct": False},
                {"option_text": "Auto Scaling group without a load balancer", "is_correct": False},
                {"option_text": "Route 53 with simple routing policy", "is_correct": False}
            ]
        },
        {
            "question_text": "A microservices application needs a fully managed message queuing service to decouple components. Which AWS service is most appropriate?",
            "explanation": "Amazon SQS is a fully managed message queuing service that enables you to decouple and scale microservices, distributed systems, and serverless applications. It provides a simple, cost-effective way to decouple components of a cloud application.",
            "difficulty": "easy",
            "options": [
                {"option_text": "Amazon SQS", "is_correct": True},
                {"option_text": "Amazon RDS Multi-AZ", "is_correct": False},
                {"option_text": "AWS Lambda", "is_correct": False},
                {"option_text": "Amazon EFS", "is_correct": False}
            ]
        },
        {
            "question_text": "A company's application needs to handle unpredictable, intermittent spikes in request volumes. Which combination of AWS services should they use?",
            "explanation": "Lambda provides serverless compute that scales automatically with the workload, while API Gateway manages the API requests and can throttle if needed. Together, they provide a resilient, automatically scaling solution for handling unpredictable request volumes.",
            "difficulty": "medium",
            "options": [
                {"option_text": "AWS Lambda with Amazon API Gateway", "is_correct": True},
                {"option_text": "Amazon EC2 with fixed instance sizes", "is_correct": False},
                {"option_text": "Amazon RDS with read replicas", "is_correct": False},
                {"option_text": "AWS Elastic Beanstalk with single-instance environment", "is_correct": False}
            ]
        },
        {
            "question_text": "A company runs a critical application and needs to ensure it can recover quickly in case of a regional AWS outage. What is the most effective disaster recovery strategy?",
            "explanation": "The active-active strategy with Route 53 health checks provides the fastest recovery by maintaining fully operational environments in multiple regions simultaneously. Traffic is automatically directed to healthy regions, minimizing recovery time in case of a regional outage.",
            "difficulty": "hard",
            "options": [
                {"option_text": "Implement an active-active multi-region architecture with Amazon Route 53 health checks", "is_correct": True},
                {"option_text": "Create regular EBS snapshots and store them in the same region", "is_correct": False},
                {"option_text": "Use a single region with multiple Availability Zones", "is_correct": False},
                {"option_text": "Maintain an inventory list of resources for manual recreation", "is_correct": False}
            ]
        },
        {
            "question_text": "A company needs to design a system that allows different components of their application to react to events in near real-time. Which AWS service should they use?",
            "explanation": "Amazon EventBridge is a serverless event bus service that makes it easy to connect applications together using data from your own applications, integrated Software-as-a-Service (SaaS) applications, and AWS services. It delivers a stream of real-time data and routes that data to targets like Lambda.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Amazon EventBridge", "is_correct": True},
                {"option_text": "Amazon ElastiCache", "is_correct": False},
                {"option_text": "AWS Elastic Beanstalk", "is_correct": False},
                {"option_text": "Amazon CloudFront", "is_correct": False}
            ]
        }
    ]
    
    insert_questions(questions, category_id)
    
# Create resilient architecture questions (batch 2)
def create_resilient_architecture_questions_batch2(category_id):
    questions = [
        {
            "question_text": "A company wants to ensure their application can continue operating even if an entire AWS region becomes unavailable. Which approach should they implement?",
            "explanation": "A multi-region active-passive architecture with data replication provides the best resilience against regional outages. The primary region handles all traffic during normal operation, while the standby region can be quickly promoted if the primary region fails, with replicated data ensuring minimal data loss.",
            "difficulty": "hard",
            "options": [
                {"option_text": "Deploy a multi-region active-passive architecture with continuous data replication", "is_correct": True},
                {"option_text": "Use a single region with resources spread across multiple Availability Zones", "is_correct": False},
                {"option_text": "Configure backups to Amazon S3 with cross-region replication enabled", "is_correct": False},
                {"option_text": "Deploy resources in a single Availability Zone with automatic backups", "is_correct": False}
            ]
        },
        {
            "question_text": "A company's application uses Amazon RDS MySQL database. Which configuration provides the highest level of database availability?",
            "explanation": "Multi-AZ deployment with read replicas provides the highest availability by deploying a primary DB instance in one AZ with a synchronous standby replica in a different AZ, plus additional read replicas that can be promoted to the primary role if needed, all while serving read traffic.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Multi-AZ deployment with read replicas in a third Availability Zone", "is_correct": True},
                {"option_text": "Single-AZ deployment with automated backups", "is_correct": False},
                {"option_text": "Multi-AZ deployment without read replicas", "is_correct": False},
                {"option_text": "Single-AZ deployment with daily snapshots", "is_correct": False}
            ]
        },
        {
            "question_text": "An application needs to continue operating during an AWS service disruption. Which combination of AWS services creates the most resilient architecture?",
            "explanation": "This combination provides multi-layer resilience: Route 53 health checks detect failures and can failover between regions, CloudFront distributes content globally, Lambda functions are stateless and automatically deployed across AZs, and DynamoDB global tables replicate data across regions.",
            "difficulty": "hard",
            "options": [
                {"option_text": "Amazon Route 53 with health checks, Amazon CloudFront, AWS Lambda, and Amazon DynamoDB global tables", "is_correct": True},
                {"option_text": "AWS Shield Advanced, Amazon EC2 Auto Scaling, Amazon RDS single-AZ, and Amazon S3", "is_correct": False},
                {"option_text": "AWS Elastic Beanstalk, Amazon S3, Amazon CloudWatch, and Amazon RDS read replicas", "is_correct": False},
                {"option_text": "Amazon API Gateway, AWS Lambda, Amazon Aurora, and Amazon ElastiCache", "is_correct": False}
            ]
        },
        {
            "question_text": "A company needs to implement data storage for their application that offers high durability for critical data. Which AWS service should they use?",
            "explanation": "Amazon S3 provides 99.999999999% (11 nines) durability for objects, making it the most durable storage option. It automatically stores data redundantly across multiple facilities and devices within a region, protecting against hardware failures and errors.",
            "difficulty": "easy",
            "options": [
                {"option_text": "Amazon S3", "is_correct": True},
                {"option_text": "Amazon EC2 instance store", "is_correct": False},
                {"option_text": "Amazon EBS volumes without snapshots", "is_correct": False},
                {"option_text": "Amazon EFS without backups", "is_correct": False}
            ]
        },
        {
            "question_text": "A company runs an application with components that need to communicate with each other but can tolerate delays in message processing. Which service should they use to maximize reliability?",
            "explanation": "Amazon SQS ensures reliable message delivery by storing messages until they are processed and deleted. If a component fails while processing a message, the visibility timeout expires, and the message becomes available for another component to process, preventing message loss.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Amazon SQS", "is_correct": True},
                {"option_text": "Amazon SNS", "is_correct": False},
                {"option_text": "AWS AppSync", "is_correct": False},
                {"option_text": "Amazon MSK", "is_correct": False}
            ]
        },
        {
            "question_text": "A company wants to implement a reliable backup strategy for their critical data. Which approach provides the highest level of data protection?",
            "explanation": "This comprehensive approach provides multiple layers of data protection: regular backups stored in S3 with its high durability, cross-region replication to protect against regional issues, versioning to recover from accidental deletions, and lifecycle policies to manage costs while maintaining long-term archives.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Store backups in Amazon S3 with cross-region replication, versioning, and lifecycle policies", "is_correct": True},
                {"option_text": "Create daily snapshots of Amazon EBS volumes and store them in the same region", "is_correct": False},
                {"option_text": "Back up data to Amazon S3 Glacier without versioning", "is_correct": False},
                {"option_text": "Use Amazon EFS and rely on its built-in redundancy within a single region", "is_correct": False}
            ]
        },
        {
            "question_text": "A web application needs to handle highly variable traffic loads while maintaining availability. Which combination of AWS services should be implemented?",
            "explanation": "This combination provides resilient, auto-scaling architecture: ALB distributes traffic across multiple AZs, Auto Scaling adjusts capacity based on demand, a multi-AZ database ensures database availability, and CloudWatch monitors the environment and triggers scaling actions.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Application Load Balancer, EC2 Auto Scaling group across multiple AZs, RDS Multi-AZ, and CloudWatch alarms", "is_correct": True},
                {"option_text": "CloudFront, EC2 instances in a single AZ, RDS Single-AZ, and AWS Trusted Advisor", "is_correct": False},
                {"option_text": "Network Load Balancer, fixed number of EC2 instances, RDS read replicas, and AWS Config", "is_correct": False},
                {"option_text": "API Gateway, fixed number of Lambda functions, DynamoDB without auto scaling, and CloudTrail", "is_correct": False}
            ]
        }
    ]
    
    insert_questions(questions, category_id)
    
# Create high-performance architecture questions (batch 1)
def create_high_performance_architecture_questions(category_id):
    questions = [
        {
            "question_text": "A company needs a storage solution for a high-performance computing application that requires high throughput and low-latency access to temporary data. Which AWS storage solution is most appropriate?",
            "explanation": "Instance Store volumes are physically attached to the host computer, providing very high I/O performance with low latency. They are ideal for temporary storage of data that changes frequently, such as buffers, caches, and scratch data for high-performance computing applications.",
            "difficulty": "hard",
            "options": [
                {"option_text": "EC2 Instance Store", "is_correct": True},
                {"option_text": "Amazon S3", "is_correct": False},
                {"option_text": "Amazon EFS", "is_correct": False},
                {"option_text": "Amazon S3 Glacier", "is_correct": False}
            ]
        },
        {
            "question_text": "A video processing application requires high-performance storage for processing large files. Which Amazon EBS volume type should be used?",
            "explanation": "Amazon EBS Provisioned IOPS (io2) volumes are designed to deliver predictable, high performance for I/O intensive workloads such as database workloads and video processing that require low latency and high throughput. They provide the ability to provision a specific level of IOPS performance.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Provisioned IOPS (io2)", "is_correct": True},
                {"option_text": "General Purpose (gp2)", "is_correct": False},
                {"option_text": "Throughput Optimized (st1)", "is_correct": False},
                {"option_text": "Cold HDD (sc1)", "is_correct": False}
            ]
        },
        {
            "question_text": "A company needs to optimize the performance of a frequently accessed, read-heavy database. Which AWS service should they implement?",
            "explanation": "Amazon ElastiCache is a web service that makes it easy to deploy, operate, and scale an in-memory cache in the cloud. It improves the performance of read-heavy database workloads by caching frequently accessed data in memory, reducing the need to access the primary database.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Amazon ElastiCache", "is_correct": True},
                {"option_text": "Amazon S3", "is_correct": False},
                {"option_text": "Amazon EBS Provisioned IOPS", "is_correct": False},
                {"option_text": "AWS Storage Gateway", "is_correct": False}
            ]
        },
        {
            "question_text": "A company is deploying a web application that will serve users globally. Which AWS service will help reduce latency for delivering static content?",
            "explanation": "Amazon CloudFront is a Content Delivery Network (CDN) that delivers data, videos, applications, and APIs to customers globally with low latency and high transfer speeds. It caches static content at edge locations around the world, reducing latency for global users.",
            "difficulty": "easy",
            "options": [
                {"option_text": "Amazon CloudFront", "is_correct": True},
                {"option_text": "Amazon RDS Read Replicas", "is_correct": False},
                {"option_text": "Amazon EFS", "is_correct": False},
                {"option_text": "AWS Global Accelerator", "is_correct": False}
            ]
        },
        {
            "question_text": "A company is experiencing slow performance with their MariaDB database on RDS. The database is read-heavy with numerous reporting queries. What is the MOST effective way to improve performance?",
            "explanation": "RDS Read Replicas allow you to create read-only copies of your database that can serve read traffic, reducing the load on your primary database. For read-heavy workloads with reporting queries, this is the most effective way to improve performance without changing the database engine.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Create RDS Read Replicas for read traffic", "is_correct": True},
                {"option_text": "Increase the allocated storage of the database", "is_correct": False},
                {"option_text": "Switch to provisioned IOPS storage", "is_correct": False},
                {"option_text": "Enable Multi-AZ deployment", "is_correct": False}
            ]
        }
    ]
    
    insert_questions(questions, category_id)

# Create high-performance architecture questions (batch 2)
def create_high_performance_architecture_questions_batch2(category_id):
    questions = [
        {
            "question_text": "A company needs to process and analyze real-time streaming data from IoT devices. Which AWS service should they use?",
            "explanation": "Amazon Kinesis Data Streams is designed for real-time processing of streaming data at scale. It can continuously capture and store terabytes of data per hour from thousands of IoT devices, making it ideal for real-time analytics and processing of streaming data.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Amazon Kinesis Data Streams", "is_correct": True},
                {"option_text": "Amazon SQS", "is_correct": False},
                {"option_text": "Amazon S3", "is_correct": False},
                {"option_text": "Amazon RDS", "is_correct": False}
            ]
        },
        {
            "question_text": "A company's application needs to access data with microsecond latency. Which AWS database service is most suitable?",
            "explanation": "Amazon DynamoDB Accelerator (DAX) is an in-memory cache for DynamoDB that provides microsecond latency for accessing frequently read data. DAX significantly improves read performance for DynamoDB tables without requiring application logic changes.",
            "difficulty": "hard",
            "options": [
                {"option_text": "Amazon DynamoDB with DAX", "is_correct": True},
                {"option_text": "Amazon RDS for MySQL", "is_correct": False},
                {"option_text": "Amazon Aurora with read replicas", "is_correct": False},
                {"option_text": "Amazon Redshift", "is_correct": False}
            ]
        },
        {
            "question_text": "A company runs compute-intensive simulations that require high-performance computing capabilities. Which EC2 instance type should they choose?",
            "explanation": "Compute Optimized instances (C-type) are designed for compute-intensive workloads that require high-performance processors. They are ideal for scientific modeling, batch processing, distributed analytics, and CPU-based machine learning inference, making them the best choice for compute-intensive simulations.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Compute Optimized (C-type)", "is_correct": True},
                {"option_text": "Memory Optimized (R-type)", "is_correct": False},
                {"option_text": "Storage Optimized (D-type)", "is_correct": False},
                {"option_text": "General Purpose (T-type)", "is_correct": False}
            ]
        },
        {
            "question_text": "A company's web application needs to handle millions of requests per second with consistent single-digit millisecond latency. Which AWS service should they use for the database layer?",
            "explanation": "Amazon DynamoDB is designed to deliver consistent, single-digit millisecond response times at any scale. It can handle millions of requests per second and automatically scales to handle high throughput without requiring manual intervention to add capacity.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Amazon DynamoDB", "is_correct": True},
                {"option_text": "Amazon RDS for PostgreSQL", "is_correct": False},
                {"option_text": "Amazon ElastiCache", "is_correct": False},
                {"option_text": "Amazon Redshift", "is_correct": False}
            ]
        },
        {
            "question_text": "A company needs to analyze petabytes of data with complex queries. Which AWS service should they use?",
            "explanation": "Amazon Redshift is a fully managed, petabyte-scale data warehouse service designed for complex queries across large datasets. It uses columnar storage, parallel query execution, and advanced query optimization to deliver fast performance for complex analytical workloads.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Amazon Redshift", "is_correct": True},
                {"option_text": "Amazon RDS", "is_correct": False},
                {"option_text": "Amazon DynamoDB", "is_correct": False},
                {"option_text": "Amazon Aurora", "is_correct": False}
            ]
        },
        {
            "question_text": "A global application needs to provide the lowest possible latency for users accessing dynamic content from different geographic regions. Which solution should be implemented?",
            "explanation": "AWS Global Accelerator uses the AWS global network to optimize the path from users to applications, improving performance by up to 60%. Unlike CloudFront which primarily caches static content, Global Accelerator improves performance for both static and dynamic content by routing traffic over the AWS backbone.",
            "difficulty": "hard",
            "options": [
                {"option_text": "AWS Global Accelerator with regional endpoints", "is_correct": True},
                {"option_text": "Amazon CloudFront with regional caching", "is_correct": False},
                {"option_text": "Replicate the application in each region with Route 53 latency routing", "is_correct": False},
                {"option_text": "Amazon API Gateway with regional endpoints", "is_correct": False}
            ]
        },
        {
            "question_text": "A company is running an application that requires fast disk I/O for a NoSQL database. Which EBS volume type should they choose?",
            "explanation": "Provisioned IOPS SSD (io2) volumes are designed for I/O-intensive workloads such as NoSQL databases that require consistent and predictable performance. They offer the highest performance and durability among EBS volume types, making them ideal for critical database workloads.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Provisioned IOPS SSD (io2)", "is_correct": True},
                {"option_text": "Throughput Optimized HDD (st1)", "is_correct": False},
                {"option_text": "Cold HDD (sc1)", "is_correct": False},
                {"option_text": "General Purpose SSD (gp3)", "is_correct": False}
            ]
        }
    ]
    
    insert_questions(questions, category_id)
    
# Create cost-optimized architecture questions (batch 1)
def create_cost_optimized_architecture_questions(category_id):
    questions = [
        {
            "question_text": "A company runs a batch processing workload on EC2 instances that can be interrupted and restarted without issues. Which EC2 purchasing option should they use for maximum cost savings?",
            "explanation": "Spot Instances provide the largest discount (up to 90% off On-Demand prices) but can be interrupted with short notice when EC2 needs the capacity back. They are ideal for batch processing workloads that can be interrupted and restarted without issues.",
            "difficulty": "easy",
            "options": [
                {"option_text": "Spot Instances", "is_correct": True},
                {"option_text": "On-Demand Instances", "is_correct": False},
                {"option_text": "Reserved Instances", "is_correct": False},
                {"option_text": "Dedicated Hosts", "is_correct": False}
            ]
        },
        {
            "question_text": "A company has predictable EC2 usage that runs continuously throughout the year. Which purchasing option will provide the maximum cost savings?",
            "explanation": "Standard Reserved Instances provide the greatest discount (up to 72% off On-Demand pricing) for applications with steady-state or predictable usage that run continuously throughout the year. With a 3-year term and upfront payment, they maximize cost savings for predictable workloads.",
            "difficulty": "easy",
            "options": [
                {"option_text": "3-year Standard Reserved Instances with All Upfront payment", "is_correct": True},
                {"option_text": "Spot Instances", "is_correct": False},
                {"option_text": "On-Demand Instances", "is_correct": False},
                {"option_text": "1-year Convertible Reserved Instances", "is_correct": False}
            ]
        },
        {
            "question_text": "A company has a website with varying traffic patterns that increase during business hours and decrease overnight and on weekends. Which EC2 Auto Scaling strategy should they implement to optimize costs?",
            "explanation": "Target tracking scaling adjusts capacity automatically based on a target metric (like CPU utilization), scaling in during low traffic and out during high traffic. Scheduled scaling adds predictable capacity increases before business hours and decreases after hours and on weekends.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Implement target tracking scaling based on CPU utilization with scheduled scaling actions for predictable patterns", "is_correct": True},
                {"option_text": "Use fixed instance counts based on peak capacity needs", "is_correct": False},
                {"option_text": "Deploy only Spot Instances with no scaling policies", "is_correct": False},
                {"option_text": "Use Reserved Instances with manual scaling", "is_correct": False}
            ]
        },
        {
            "question_text": "A company has 50 TB of infrequently accessed data that must be retained for compliance reasons. The data will be accessed only a few times per year but must be accessible within a few hours when needed. Which S3 storage class should they use?",
            "explanation": "S3 Glacier is designed for data archiving at a low cost (approximately 1/5th the price of S3 Standard). It's ideal for infrequently accessed data that needs to be retained for compliance and retrieved within hours. Standard retrieval typically takes 3-5 hours, which meets the requirement of 'accessible within a few hours.'",
            "difficulty": "medium",
            "options": [
                {"option_text": "S3 Glacier", "is_correct": True},
                {"option_text": "S3 Standard", "is_correct": False},
                {"option_text": "S3 One Zone-IA", "is_correct": False},
                {"option_text": "S3 Intelligent-Tiering", "is_correct": False}
            ]
        },
        {
            "question_text": "A company needs to host a static website with the lowest possible cost. Which solution should they implement?",
            "explanation": "S3 static website hosting is the most cost-effective way to host a static website. It eliminates the need for web servers and associated infrastructure costs. Content is delivered directly from S3 to users' browsers, and CloudFront further reduces costs by caching content at edge locations.",
            "difficulty": "easy",
            "options": [
                {"option_text": "Amazon S3 static website hosting with CloudFront distribution", "is_correct": True},
                {"option_text": "Amazon EC2 instances with Auto Scaling", "is_correct": False},
                {"option_text": "AWS Elastic Beanstalk environment", "is_correct": False},
                {"option_text": "Amazon ECS with Fargate", "is_correct": False}
            ]
        }
    ]
    
    insert_questions(questions, category_id)

# Create cost-optimized architecture questions (batch 2)
def create_cost_optimized_architecture_questions_batch2(category_id):
    questions = [
        {
            "question_text": "A company wants to optimize costs for their Amazon RDS deployment. Their database is primarily used during business hours with minimal activity at night and on weekends. Which feature should they implement?",
            "explanation": "RDS scheduled automatic start/stop allows you to automatically stop your database instances during periods of inactivity (like nights and weekends) and start them when they're needed again. This can significantly reduce costs since you only pay for compute resources when your database is running.",
            "difficulty": "medium",
            "options": [
                {"option_text": "RDS scheduled automatic start/stop", "is_correct": True},
                {"option_text": "RDS Multi-AZ deployment", "is_correct": False},
                {"option_text": "RDS Provisioned IOPS", "is_correct": False},
                {"option_text": "RDS Enhanced Monitoring", "is_correct": False}
            ]
        },
        {
            "question_text": "A company needs to store large amounts of data that is rarely accessed. The data needs to be retained for compliance reasons, but the probability of needing to retrieve it is less than 1%. Which is the MOST cost-effective storage solution?",
            "explanation": "S3 Glacier Deep Archive is the lowest-cost storage class designed for long-term retention of data that might be accessed once or twice a year. It offers the lowest storage cost among all S3 storage classes (up to 95% less than S3 Standard), making it ideal for rarely accessed archival data.",
            "difficulty": "medium",
            "options": [
                {"option_text": "Amazon S3 Glacier Deep Archive", "is_correct": True},
                {"option_text": "Amazon S3 Standard", "is_correct": False},
                {"option_text": "Amazon S3 Intelligent-Tiering", "is_correct": False},
                {"option_text": "Amazon EBS Cold HDD volumes", "is_correct": False}
            ]
        },
        {
            "question_text": "A company has variable and unpredictable computing needs. Some workloads run for just a few minutes, while others run for hours. Which AWS service would be most cost-effective for this scenario?",
            "explanation": "AWS Lambda charges only for the compute time consumed, with no charges when code is not running. With per-millisecond billing and no minimum fees, it's ideal for variable, unpredictable workloads that have idle periods, as you don't pay for idle capacity like you would with EC2.",
            "difficulty": "medium",
            "options": [
                {"option_text": "AWS Lambda", "is_correct": True},
                {"option_text": "Amazon EC2 with Reserved Instances", "is_correct": False},
                {"option_text": "Amazon EC2 Dedicated Hosts", "is_correct": False},
                {"option_text": "AWS Outposts", "is_correct": False}
            ]
        },
        {
            "question_text": "A company wants to optimize storage costs for their application data. The data has distinct access patterns: 20% is accessed frequently, 30% is accessed infrequently, and 50% is rarely accessed. Which S3 strategy would be most cost-effective?",
            "explanation": "S3 Lifecycle policies allow you to automatically transition objects between storage classes based on defined rules. Using a combination of S3 Standard for frequently accessed data, S3 Standard-IA for infrequently accessed data, and S3 Glacier for rarely accessed data optimizes costs while maintaining appropriate accessibility.",
            "difficulty": "hard",
            "options": [
                {"option_text": "Implement S3 Lifecycle policies to automatically transition objects between S3 Standard, S3 Standard-IA, and S3 Glacier", "is_correct": True},
                {"option_text": "Store all data in S3 Standard to ensure fast access when needed", "is_correct": False},
                {"option_text": "Store all data in S3 Glacier to minimize storage costs", "is_correct": False},
                {"option_text": "Use S3 Intelligent-Tiering for all objects regardless of access pattern", "is_correct": False}
            ]
        },
        {
            "question_text": "A company has a large number of infrequently used EC2 instances running 24/7. Which AWS service should they implement to optimize costs?",
            "explanation": "AWS Instance Scheduler is a solution that automates the starting and stopping of EC2 and RDS instances according to user-defined schedules. For infrequently used instances, this can reduce operational costs by stopping instances when they're not needed, potentially saving 70% or more on instance costs.",
            "difficulty": "medium",
            "options": [
                {"option_text": "AWS Instance Scheduler", "is_correct": True},
                {"option_text": "AWS Budgets", "is_correct": False},
                {"option_text": "AWS Cost Explorer", "is_correct": False},
                {"option_text": "AWS Trusted Advisor", "is_correct": False}
            ]
        },
        {
            "question_text": "A company needs to run a database that requires high availability but wants to minimize costs. Which Amazon RDS deployment option should they choose?",
            "explanation": "RDS Multi-AZ with Single-AZ read replica is cost-effective while maintaining high availability. The Multi-AZ deployment provides a standby for failover, ensuring availability, while the read replica offloads read traffic from the primary database, improving performance. This costs less than a Multi-AZ deployment with multiple read replicas.",
            "difficulty": "medium",
            "options": [
                {"option_text": "RDS Multi-AZ with a Single-AZ read replica", "is_correct": True},
                {"option_text": "RDS Single-AZ with Provisioned IOPS", "is_correct": False},
                {"option_text": "RDS Multi-AZ with multiple read replicas in each Availability Zone", "is_correct": False},
                {"option_text": "RDS Aurora Global Database", "is_correct": False}
            ]
        },
        {
            "question_text": "A company wants to reduce their AWS data transfer costs. They have a web application hosted in AWS that serves users across North America and Europe. Which service should they implement?",
            "explanation": "Amazon CloudFront can significantly reduce data transfer costs by caching content at edge locations closer to users. It offers optimized data transfer pricing compared to direct EC2-to-internet transfer costs, especially for serving content to users across multiple geographic regions.",
            "difficulty": "easy",
            "options": [
                {"option_text": "Amazon CloudFront", "is_correct": True},
                {"option_text": "AWS Direct Connect", "is_correct": False},
                {"option_text": "AWS Transit Gateway", "is_correct": False},
                {"option_text": "Amazon Route 53", "is_correct": False}
            ]
        }
    ]
    
    insert_questions(questions, category_id)

# Helper function to insert questions
def insert_questions(questions, category_id):
    question_count = 0
    
    for question in questions:
        # Insert question
        question_sql = """
        INSERT INTO question (question_text, explanation, category_id, difficulty, created_at, updated_at) 
        VALUES (:question_text, :explanation, :category_id, :difficulty, :created_at, :updated_at) 
        RETURNING id
        """
        
        question_params = {
            'question_text': question['question_text'],
            'explanation': question['explanation'],
            'category_id': category_id,
            'difficulty': question['difficulty'],
            'created_at': datetime.datetime.utcnow(),
            'updated_at': datetime.datetime.utcnow()
        }
        
        result = execute_sql(question_sql, question_params)
        row = result.fetchone()
        question_id = row[0]
        
        # Insert options for this question
        for option in question['options']:
            option_sql = """
            INSERT INTO question_option (question_id, option_text, is_correct) 
            VALUES (:question_id, :option_text, :is_correct)
            """
            
            option_params = {
                'question_id': question_id,
                'option_text': option['option_text'],
                'is_correct': option['is_correct']
            }
            
            execute_sql(option_sql, option_params)
        
        question_count += 1
        print(f"Created question {question_count}: {question['question_text'][:50]}...")
    
    print(f"Created {question_count} questions in this batch.")

# Create practice exam
def create_practice_exam():
    # Get all questions
    result = execute_sql("SELECT id FROM question")
    all_question_ids = [row[0] for row in result.fetchall()]
    
    if len(all_question_ids) < 20:
        print("Not enough questions to create an exam. Please add more questions first.")
        return
    
    # Take a sample for our exam (max 20 questions or all available questions)
    question_count = min(20, len(all_question_ids))
    question_ids = sample(all_question_ids, question_count)
    
    # Create the exam
    exam_sql = """
    INSERT INTO exam (title, description, duration_minutes, pass_percentage, created_at, is_active) 
    VALUES (:title, :description, :duration_minutes, :pass_percentage, :created_at, :is_active) 
    RETURNING id
    """
    
    exam_params = {
        'title': 'AWS SAA-C03 Practice Exam',
        'description': 'A practice exam with questions covering the AWS Solutions Architect Associate certification domains.',
        'duration_minutes': min(65, question_count * 3),  # 3 minutes per question, max 65 minutes
        'pass_percentage': 72.0,
        'created_at': datetime.datetime.utcnow(),
        'is_active': True
    }
    
    result = execute_sql(exam_sql, exam_params)
    row = result.fetchone()
    exam_id = row[0]
    
    # Add questions to the exam
    for i, q_id in enumerate(question_ids):
        exam_question_sql = """
        INSERT INTO exam_question (exam_id, question_id, "order") 
        VALUES (:exam_id, :question_id, :order)
        """
        
        exam_question_params = {
            'exam_id': exam_id,
            'question_id': q_id,
            'order': i + 1
        }
        
        execute_sql(exam_question_sql, exam_question_params)
    
    print(f"Created practice exam with {len(question_ids)} questions")

if __name__ == "__main__":
    # Check which action to perform
    if len(sys.argv) < 2:
        print("Please specify an action: setup, secure, secure2, secure3, resilient, resilient2, performance, performance2, cost, cost2, or exam")
        sys.exit(1)
    
    action = sys.argv[1]
    
    # Always create admin user and categories
    create_admin_user()
    category_ids = create_categories()
    
    if action == "setup":
        print("Setup completed. Admin user and categories created.")
    
    elif action == "secure":
        create_secure_architecture_questions(category_ids["Design Secure Architectures"])
    
    elif action == "secure2":
        create_secure_architecture_questions_batch2(category_ids["Design Secure Architectures"])
    
    elif action == "secure3":
        create_secure_architecture_questions_batch3(category_ids["Design Secure Architectures"])
    
    elif action == "resilient":
        create_resilient_architecture_questions(category_ids["Design Resilient Architectures"])
    
    elif action == "resilient2":
        create_resilient_architecture_questions_batch2(category_ids["Design Resilient Architectures"])
    
    elif action == "performance":
        create_high_performance_architecture_questions(category_ids["Design High-Performing Architectures"])
    
    elif action == "performance2":
        create_high_performance_architecture_questions_batch2(category_ids["Design High-Performing Architectures"])
    
    elif action == "cost":
        create_cost_optimized_architecture_questions(category_ids["Design Cost-Optimized Architectures"])
    
    elif action == "cost2":
        create_cost_optimized_architecture_questions_batch2(category_ids["Design Cost-Optimized Architectures"])
    
    elif action == "exam":
        create_practice_exam()
    
    else:
        print(f"Unknown action: {action}")
        print("Please specify an action: setup, secure, secure2, secure3, resilient, resilient2, performance, performance2, cost, cost2, or exam")