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
    if result.rowcount > 0:
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
        if result.rowcount == 0:
            # Create new category
            sql = """
            INSERT INTO question_category (name, description) 
            VALUES (:name, :description) RETURNING id
            """
            result = execute_sql(sql, category)
            for row in result:
                category_ids[category['name']] = row[0]
            print(f"Category created: {category['name']}")
        else:
            # Get existing category id
            for row in result:
                category_ids[category['name']] = row[0]
            print(f"Category already exists: {category['name']}")
    
    return category_ids

# Create questions with options
def create_questions(category_ids):
    # Dictionary of AWS SAA-C03 questions organized by domain
    questions = {
        "Design Secure Architectures": [
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
            },
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
            },
            {
                "question_text": "A company needs to implement end-to-end encryption for data transmitted between clients and their application running on Amazon EC2. Which approach should they use?",
                "explanation": "AWS Certificate Manager (ACM) provides a managed service for provisioning and managing SSL/TLS certificates. Using ACM with an Application Load Balancer allows for SSL/TLS termination at the load balancer, ensuring that data transmitted between clients and the application is encrypted end-to-end.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Use AWS Certificate Manager to provision an SSL/TLS certificate and configure it with an Application Load Balancer", "is_correct": True},
                    {"option_text": "Use Amazon CloudFront with default certificates and disable HTTPS connections to origin", "is_correct": False},
                    {"option_text": "Use AWS Direct Connect with public virtual interfaces", "is_correct": False},
                    {"option_text": "Use Amazon API Gateway with AWS Lambda authorizers", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is deploying a web application in AWS that processes credit card information. Which security requirement aligns with the AWS shared responsibility model?",
                "explanation": "Under the AWS Shared Responsibility Model, AWS is responsible for security 'of' the cloud, while customers are responsible for security 'in' the cloud. This includes PCI DSS compliance for application-level security controls, which is the customer's responsibility.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "The company implements PCI DSS compliant application-level security controls", "is_correct": True},
                    {"option_text": "AWS implements hypervisor virtualization security", "is_correct": False},
                    {"option_text": "AWS maintains physical security of data centers", "is_correct": False},
                    {"option_text": "AWS patches underlying infrastructure components", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has a multi-tier web application deployed in a VPC with public and private subnets. Which network architecture best secures the database tier?",
                "explanation": "A secure network architecture places databases in a private subnet with no internet access, using security groups to restrict inbound access to only the application servers in another private subnet. This provides multiple layers of network security for the database tier.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Place the database in a private subnet with no internet access and use security groups to allow only traffic from the application tier", "is_correct": True},
                    {"option_text": "Place the database in a public subnet with a security group allowing access only on the database port", "is_correct": False},
                    {"option_text": "Place the database in a private subnet with a NAT gateway and allow all outbound internet access", "is_correct": False},
                    {"option_text": "Place the database in a separate VPC and use VPC peering with open security groups", "is_correct": False}
                ]
            },
            {
                "question_text": "A Solutions Architect is designing an application that processes sensitive data. The data must be encrypted in transit and at rest, and the customer must maintain full control of the encryption keys. Which solution should be implemented?",
                "explanation": "KMS Customer Managed Keys (CMKs) provide full control over the encryption keys, including rotation policies and access controls. When integrated with AWS services like S3 and DynamoDB, they provide encryption at rest. For in-transit encryption, HTTPS with an ACM certificate ensures data is protected while moving between services.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Use AWS KMS with Customer Managed Keys and HTTPS with ACM certificates for all API calls", "is_correct": True},
                    {"option_text": "Use AWS-managed encryption keys and HTTP connections with VPC endpoints", "is_correct": False},
                    {"option_text": "Use server-side encryption with S3-managed keys and default RDS encryption", "is_correct": False},
                    {"option_text": "Use client-side encryption and store the encryption keys in EC2 instance metadata", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs to enforce security policies on all resources created in their AWS account. Which approach should they take?",
                "explanation": "AWS Service Control Policies (SCPs) allow you to centrally control permissions for all accounts in an organization. AWS Config Rules can automatically evaluate resources against defined rules, CloudFormation StackSets let you deploy consistent resources across accounts, and IAM permission boundaries define maximum permissions.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Implement AWS Organizations with Service Control Policies, AWS Config Rules, CloudFormation StackSets, and IAM permission boundaries", "is_correct": True},
                    {"option_text": "Configure IAM users with administrative permissions in each account and implement manual checks", "is_correct": False},
                    {"option_text": "Use Amazon CloudWatch monitoring on all resources and set up alerts for policy violations", "is_correct": False},
                    {"option_text": "Create a single shared VPC for all resources and control access with security groups", "is_correct": False}
                ]
            },
            {
                "question_text": "A company wants to securely store and automatically rotate database credentials used by a Lambda function. What is the most efficient and secure approach?",
                "explanation": "AWS Secrets Manager is specifically designed to manage and automatically rotate sensitive information such as database credentials. When combined with Lambda, it can securely provide credentials to the function at runtime without hardcoding them in the code.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Store the credentials in AWS Secrets Manager with automatic rotation and retrieve them in the Lambda function code", "is_correct": True},
                    {"option_text": "Store the credentials in environment variables in the Lambda function configuration", "is_correct": False},
                    {"option_text": "Store the credentials in an S3 bucket with server-side encryption and download them in the Lambda function", "is_correct": False},
                    {"option_text": "Hardcode the credentials in the Lambda function code and update them manually when needed", "is_correct": False}
                ]
            },
            {
                "question_text": "A company uses multiple AWS accounts and needs a centralized way to manage identities and access across all accounts. What should they implement?",
                "explanation": "AWS IAM Identity Center (previously known as AWS Single Sign-On) provides a central place to manage access across multiple AWS accounts. It integrates with existing identity providers, enabling single sign-on access to all assigned accounts and applications.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "AWS IAM Identity Center (AWS SSO)", "is_correct": True},
                    {"option_text": "Cross-account IAM roles in each account", "is_correct": False},
                    {"option_text": "Amazon Cognito User Pools", "is_correct": False},
                    {"option_text": "AWS Directory Service in each account", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is running a payment processing application on EC2 instances that requires encryption keys to securely process transactions. What is the MOST secure way to manage these keys?",
                "explanation": "AWS CloudHSM provides dedicated Hardware Security Modules (HSMs) in the AWS Cloud, giving you full control over key management with FIPS 140-2 Level 3 validated hardware. This provides the highest level of security for managing keys used for sensitive payment processing.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Use AWS CloudHSM to store and manage encryption keys", "is_correct": True},
                    {"option_text": "Store encryption keys in AWS Secrets Manager", "is_correct": False},
                    {"option_text": "Store encryption keys in environment variables on the EC2 instances", "is_correct": False},
                    {"option_text": "Use AWS KMS with AWS-managed keys", "is_correct": False}
                ]
            },
            {
                "question_text": "A security team wants to monitor and analyze network traffic patterns across their entire AWS infrastructure. Which AWS service should they use?",
                "explanation": "VPC Flow Logs capture information about the IP traffic going to and from network interfaces in your VPC. These logs can be published to CloudWatch Logs or S3, allowing you to analyze network traffic patterns and identify security issues across your entire AWS infrastructure.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "VPC Flow Logs", "is_correct": True},
                    {"option_text": "AWS CloudTrail", "is_correct": False},
                    {"option_text": "Amazon Inspector", "is_correct": False},
                    {"option_text": "AWS Trusted Advisor", "is_correct": False}
                ]
            },
            {
                "question_text": "A company wants to protect its web application from common web exploits using a managed AWS service. Which service should they choose?",
                "explanation": "AWS WAF is a web application firewall that helps protect web applications from common web exploits that could affect application availability, compromise security, or consume excessive resources. It allows you to create custom rules to block common attack patterns.",
                "difficulty": "easy",
                "options": [
                    {"option_text": "AWS WAF", "is_correct": True},
                    {"option_text": "AWS Shield Standard", "is_correct": False},
                    {"option_text": "Amazon GuardDuty", "is_correct": False},
                    {"option_text": "AWS Network Firewall", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs to ensure that S3 objects in a bucket used for financial records are retained for 7 years and cannot be deleted by any user during that period. How should they configure the bucket?",
                "explanation": "S3 Object Lock in compliance mode prevents objects from being deleted or overwritten for a specified retention period, even by the root user. When combined with a bucket policy that denies delete actions for all users, this provides strong protection against accidental or intentional deletion.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Configure S3 Object Lock in compliance mode with a 7-year retention period and add a bucket policy that denies delete actions", "is_correct": True},
                    {"option_text": "Enable S3 versioning and set a lifecycle policy to move objects to Glacier after 7 years", "is_correct": False},
                    {"option_text": "Configure S3 cross-region replication to ensure multiple copies exist", "is_correct": False},
                    {"option_text": "Set up CloudWatch Events to monitor delete actions and trigger a Lambda function to restore objects", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has a requirement to monitor all API calls made by IAM users and roles within their AWS account. Which AWS service should they enable?",
                "explanation": "AWS CloudTrail records API calls made within an AWS account, providing you with detailed event history of user, role, or service activity. It records important information including who made the request, when it was made, and IP address of the requester.",
                "difficulty": "easy",
                "options": [
                    {"option_text": "AWS CloudTrail", "is_correct": True},
                    {"option_text": "Amazon CloudWatch", "is_correct": False},
                    {"option_text": "VPC Flow Logs", "is_correct": False},
                    {"option_text": "AWS Config", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs to control which API requests are allowed for each of their applications running on AWS. Which feature should they implement?",
                "explanation": "IAM Service Control Policies (SCPs) can restrict API actions at the organization or account level, but for fine-grained application-level control, IAM resource-based policies are most appropriate. These policies can be attached directly to AWS resources to control who can perform specific API actions on those resources.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "IAM resource-based policies with explicit denies for unauthorized API calls", "is_correct": True},
                    {"option_text": "Security groups configured to block unauthorized API endpoints", "is_correct": False},
                    {"option_text": "Route 53 DNS routing policies to control API endpoint access", "is_correct": False},
                    {"option_text": "VPC endpoints with endpoint policies restricting all API calls", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs to authenticate users from their corporate directory service with AWS. Which approach provides the MOST secure and seamless experience?",
                "explanation": "SAML 2.0 federation allows users to authenticate with their corporate identity provider (like Active Directory) and receive temporary credentials for AWS through IAM roles, providing single sign-on without sharing corporate credentials with AWS.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Configure SAML 2.0 federation between the corporate identity provider and AWS IAM", "is_correct": True},
                    {"option_text": "Create IAM users that match corporate usernames and distribute access keys", "is_correct": False},
                    {"option_text": "Set up a VPN connection and manage access through security groups", "is_correct": False},
                    {"option_text": "Create a shared IAM user for all corporate access", "is_correct": False}
                ]
            },
            {
                "question_text": "A Solutions Architect needs to protect data in an S3 bucket against accidental deletion or overwriting. Which combination of features should be used?",
                "explanation": "S3 versioning keeps multiple variants of an object, allowing you to recover from accidental deletions or overwrites. MFA Delete requires multi-factor authentication for deleting objects, and S3 Object Lock can be configured to prevent object deletion for a set period.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Enable S3 versioning with MFA Delete and S3 Object Lock", "is_correct": True},
                    {"option_text": "Configure bucket policies with IAM roles and CORS headers", "is_correct": False},
                    {"option_text": "Set up S3 lifecycle policies with cross-region replication", "is_correct": False},
                    {"option_text": "Enable server-side encryption with CloudTrail logging", "is_correct": False}
                ]
            },
            {
                "question_text": "A company wants to ensure that nobody can modify the security groups attached to their EC2 instances. Which AWS service should they use to enforce this policy?",
                "explanation": "AWS Organizations Service Control Policies (SCPs) allow you to centrally control the maximum available permissions for all accounts in your organization. You can create an SCP that explicitly denies the ability to modify security groups, effectively preventing anyone from modifying them.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "AWS Organizations with Service Control Policies (SCPs)", "is_correct": True},
                    {"option_text": "Amazon Inspector with assessment templates", "is_correct": False},
                    {"option_text": "AWS Trusted Advisor with security checks", "is_correct": False},
                    {"option_text": "Amazon GuardDuty with threat detection", "is_correct": False}
                ]
            }
        ],
        "Design Resilient Architectures": [
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
            },
            {
                "question_text": "A company wants to ensure their database maintains high availability while minimizing data loss in case of a failure. Which Amazon RDS feature should they use?",
                "explanation": "Amazon RDS Multi-AZ deployments provide enhanced availability and durability by automatically provisioning and maintaining a synchronous standby replica in a different Availability Zone. In case of an infrastructure failure, RDS automatically fails over to the standby without manual intervention.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Multi-AZ deployment", "is_correct": True},
                    {"option_text": "Single-AZ with automated backups", "is_correct": False},
                    {"option_text": "Read replicas in the same AZ", "is_correct": False},
                    {"option_text": "Cross-region snapshot copy", "is_correct": False}
                ]
            },
            {
                "question_text": "An application needs to store and retrieve any amount of data from anywhere. The access patterns are unpredictable, and the company wants to pay only for what they use. Which AWS storage service should they choose?",
                "explanation": "Amazon S3 is designed for 99.999999999% (11 9s) of durability and can store and retrieve any amount of data from anywhere. With S3's pay-as-you-go pricing model, you only pay for what you use, making it ideal for unpredictable access patterns.",
                "difficulty": "easy",
                "options": [
                    {"option_text": "Amazon S3", "is_correct": True},
                    {"option_text": "Amazon EBS", "is_correct": False},
                    {"option_text": "AWS Storage Gateway", "is_correct": False},
                    {"option_text": "Amazon FSx", "is_correct": False}
                ]
            },
            {
                "question_text": "A company wants to minimize the impact of DDoS attacks on their web application. Which combination of AWS services should they implement?",
                "explanation": "AWS Shield Advanced provides enhanced DDoS protection for applications running on AWS, while AWS WAF helps protect against common web exploits. CloudFront distributes traffic across multiple edge locations, and Route 53 ensures DNS availability - together providing comprehensive DDoS protection.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "AWS Shield Advanced, AWS WAF, Amazon CloudFront, and Amazon Route 53", "is_correct": True},
                    {"option_text": "Amazon VPC, Security Groups, and Network ACLs", "is_correct": False},
                    {"option_text": "AWS CloudTrail, AWS Config, and Amazon Inspector", "is_correct": False},
                    {"option_text": "Amazon GuardDuty, Amazon Macie, and AWS Firewall Manager", "is_correct": False}
                ]
            },
            {
                "question_text": "A Solutions Architect is designing a workflow orchestration for a microservices architecture. Which AWS service should they use?",
                "explanation": "AWS Step Functions provides a serverless orchestration service that makes it easy to coordinate the components of distributed applications and microservices using visual workflows. It automatically triggers and tracks each step, and retries when there are errors.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "AWS Step Functions", "is_correct": True},
                    {"option_text": "Amazon SWF", "is_correct": False},
                    {"option_text": "AWS Batch", "is_correct": False},
                    {"option_text": "Amazon MQ", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is building an application that requires millisecond latency for data retrieval. Which AWS service should they use for caching?",
                "explanation": "Amazon ElastiCache provides in-memory caching that can deliver sub-millisecond latency for read-intensive workloads. It supports both Memcached and Redis engines, providing a solution for real-time applications requiring high performance.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Amazon ElastiCache", "is_correct": True},
                    {"option_text": "Amazon DynamoDB without DAX", "is_correct": False},
                    {"option_text": "Amazon RDS read replicas", "is_correct": False},
                    {"option_text": "Amazon S3 with standard retrieval", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has a legacy application that needs to be migrated to AWS with minimal modifications. Which compute service offers the LEAST amount of operational overhead while still allowing the application to run without changes?",
                "explanation": "AWS Elastic Beanstalk is a Platform as a Service (PaaS) that handles deployment, capacity provisioning, load balancing, auto-scaling, and application health monitoring automatically. It allows you to focus on your code while AWS manages the infrastructure, requiring minimal changes to legacy applications.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "AWS Elastic Beanstalk", "is_correct": True},
                    {"option_text": "Amazon EC2 with custom AMIs", "is_correct": False},
                    {"option_text": "AWS Lambda functions", "is_correct": False},
                    {"option_text": "Amazon ECS with Docker containers", "is_correct": False}
                ]
            },
            {
                "question_text": "An e-commerce company needs to ensure their shopping cart data is highly available and can survive an Availability Zone failure. Where should they store this data?",
                "explanation": "DynamoDB global tables provide fully managed, multi-region, multi-active database that delivers fast local read and write performance for globally distributed applications. It automatically replicates data across your choice of AWS Regions with built-in conflict resolution.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Amazon DynamoDB with global tables enabled", "is_correct": True},
                    {"option_text": "Amazon S3 with cross-region access points", "is_correct": False},
                    {"option_text": "Amazon EC2 instances with instance store volumes", "is_correct": False},
                    {"option_text": "Amazon EFS in a single Availability Zone", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has containerized their application and wants a fully managed service to run their containers without managing servers or clusters. Which AWS service should they use?",
                "explanation": "AWS Fargate is a serverless compute engine for containers that works with both Amazon ECS and Amazon EKS. With Fargate, you don't need to provision, configure, or scale clusters of virtual machines to run containers. This removes the need to choose server types, decide when to scale clusters, or optimize cluster packing.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "AWS Fargate", "is_correct": True},
                    {"option_text": "Amazon EC2 with Auto Scaling", "is_correct": False},
                    {"option_text": "Amazon EMR", "is_correct": False},
                    {"option_text": "AWS Lambda", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has an application that needs to process messages in the exact order they are sent and ensure each message is processed exactly once. Which AWS service should they use?",
                "explanation": "Amazon SQS FIFO (First-In-First-Out) queues are designed to guarantee that messages are processed exactly once and in the exact order they are sent. They provide features like content-based deduplication and message group ID to support ordered, exactly-once processing.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Amazon SQS FIFO queue", "is_correct": True},
                    {"option_text": "Amazon SQS standard queue", "is_correct": False},
                    {"option_text": "Amazon SNS", "is_correct": False},
                    {"option_text": "Amazon MQ", "is_correct": False}
                ]
            },
            {
                "question_text": "A Solutions Architect is designing an application with a variable workload that has unpredictable spikes. Which combination of AWS services should they use to implement a scalable and cost-effective architecture?",
                "explanation": "Auto Scaling groups automatically adjust EC2 capacity based on demand, while Application Load Balancer distributes traffic across the instances. CloudWatch provides metrics and alarms to trigger scaling policies, and EC2 Spot Instances reduce costs during peak periods.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Auto Scaling groups, Application Load Balancer, CloudWatch alarms, and EC2 Spot Instances", "is_correct": True},
                    {"option_text": "Reserved Instances in multiple AZs with Route 53 failover routing", "is_correct": False},
                    {"option_text": "On-Demand Instances with scheduled scaling and Elastic IP addresses", "is_correct": False},
                    {"option_text": "Dedicated Hosts with placement groups and fixed instance counts", "is_correct": False}
                ]
            },
            {
                "question_text": "A global company needs a data storage solution that provides low-latency access to their data from multiple AWS Regions. Which solution should they implement?",
                "explanation": "Amazon Aurora Global Database is designed for globally distributed applications, allowing a single Aurora database to span multiple AWS Regions. It replicates data with no impact on database performance, enables fast local reads with typical latency of less than a second, and provides disaster recovery from region-wide outages.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Amazon Aurora Global Database", "is_correct": True},
                    {"option_text": "Amazon RDS Read Replicas in each region", "is_correct": False},
                    {"option_text": "Amazon S3 with Cross-Region Replication", "is_correct": False},
                    {"option_text": "Amazon DynamoDB with regular backups to multiple regions", "is_correct": False}
                ]
            },
            {
                "question_text": "A Solutions Architect needs to design a highly available architecture for a critical application. The application must be able to withstand the failure of a single Availability Zone. What is the MINIMUM number of Availability Zones required?",
                "explanation": "To ensure high availability and the ability to withstand the failure of a single Availability Zone, you need a minimum of 2 Availability Zones. This allows the application to continue operating if one zone experiences an outage, while minimizing costs compared to using more zones.",
                "difficulty": "easy",
                "options": [
                    {"option_text": "2", "is_correct": True},
                    {"option_text": "1", "is_correct": False},
                    {"option_text": "3", "is_correct": False},
                    {"option_text": "4", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has a stateful application that frequently writes to a shared file system. They want to move this application to AWS and maintain high availability. Which storage solution should they use?",
                "explanation": "Amazon EFS is a fully managed elastic NFS file system that can be accessed concurrently by multiple EC2 instances across multiple Availability Zones. It provides the shared, stateful storage needed for applications that frequently write to a common file system.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Amazon EFS", "is_correct": True},
                    {"option_text": "Amazon S3", "is_correct": False},
                    {"option_text": "Amazon EBS", "is_correct": False},
                    {"option_text": "Amazon Instance Store", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs to design a highly available database architecture with automatic failover capabilities. Which Amazon RDS feature should they implement?",
                "explanation": "Amazon RDS Multi-AZ deployments provide enhanced availability and durability for database instances by automatically provisioning and maintaining a synchronous standby replica in a different Availability Zone. In case of infrastructure failure, RDS automatically fails over to the standby.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Multi-AZ deployment", "is_correct": True},
                    {"option_text": "Read Replicas", "is_correct": False},
                    {"option_text": "Database snapshots", "is_correct": False},
                    {"option_text": "Single-AZ with enhanced monitoring", "is_correct": False}
                ]
            },
            {
                "question_text": "A company wants to implement a disaster recovery strategy for their critical application with an RTO of 10 minutes and an RPO of 5 minutes. Which strategy should they choose?",
                "explanation": "The Warm Standby strategy maintains a scaled-down but fully functional environment in another region, which can be quickly scaled up in case of a disaster. This approach can typically achieve RTOs of minutes, meeting the 10-minute requirement, while continuous data replication can achieve the 5-minute RPO.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Warm Standby", "is_correct": True},
                    {"option_text": "Backup and Restore", "is_correct": False},
                    {"option_text": "Pilot Light", "is_correct": False},
                    {"option_text": "Multi-site Active/Active", "is_correct": False}
                ]
            },
            {
                "question_text": "A Solutions Architect is designing a system to distribute traffic across multiple EC2 instances running in private subnets. The system must be highly available and support SSL termination. Which AWS service should they use?",
                "explanation": "Application Load Balancer can distribute traffic across multiple EC2 instances in private subnets, supports SSL termination, and can be deployed across multiple Availability Zones for high availability. It's designed to handle HTTP/HTTPS traffic with advanced request routing capabilities.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Application Load Balancer", "is_correct": True},
                    {"option_text": "Classic Load Balancer", "is_correct": False},
                    {"option_text": "Amazon Route 53", "is_correct": False},
                    {"option_text": "AWS Global Accelerator", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is deploying a new application and wants to make sure it can handle traffic spikes without manual intervention. Which AWS feature should they configure?",
                "explanation": "Auto Scaling helps maintain application availability by automatically adding or removing EC2 instances according to conditions you define. It can automatically adjust capacity to maintain steady, predictable performance at the lowest possible cost, handling traffic spikes without manual intervention.",
                "difficulty": "easy",
                "options": [
                    {"option_text": "Auto Scaling", "is_correct": True},
                    {"option_text": "Reserved Instances", "is_correct": False},
                    {"option_text": "Dedicated Hosts", "is_correct": False},
                    {"option_text": "Placement Groups", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs to ensure that their Amazon S3 data remains available even if an entire AWS Region goes down. What should they implement?",
                "explanation": "S3 Cross-Region Replication (CRR) automatically replicates data from a source bucket to a destination bucket in a different AWS Region. This provides a way to maintain an exact copy of your data in another region, ensuring availability even if the original region experiences an outage.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "S3 Cross-Region Replication", "is_correct": True},
                    {"option_text": "S3 Same-Region Replication", "is_correct": False},
                    {"option_text": "S3 Versioning without replication", "is_correct": False},
                    {"option_text": "S3 Transfer Acceleration", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has a critical application with a Recovery Time Objective (RTO) of 2 hours and a Recovery Point Objective (RPO) of 1 hour. Which disaster recovery strategy should they implement?",
                "explanation": "Pilot Light keeps core systems running in a different region at minimal cost, with data continuously replicated. It can be quickly expanded to handle production load, achieving RTOs of 1-2 hours and RPOs of minutes, meeting the company's 2-hour RTO and 1-hour RPO requirements.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Pilot Light", "is_correct": True},
                    {"option_text": "Backup and Restore", "is_correct": False},
                    {"option_text": "Multi-site Active/Active", "is_correct": False},
                    {"option_text": "Warm Standby", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs to process data streams in real-time with custom code. Which AWS service should they use?",
                "explanation": "Amazon Kinesis Data Analytics allows you to process and analyze streaming data in real-time with standard SQL or Apache Flink. It enables you to build SQL queries and Java applications that process streaming data and generate analytics, making it ideal for real-time data processing with custom code.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Amazon Kinesis Data Analytics", "is_correct": True},
                    {"option_text": "Amazon EMR", "is_correct": False},
                    {"option_text": "AWS Glue", "is_correct": False},
                    {"option_text": "Amazon QuickSight", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is deploying an application that will store sensitive customer data in DynamoDB. They want to ensure the data is protected from unauthorized access. Which feature should they implement?",
                "explanation": "DynamoDB encryption at rest provides enhanced security by protecting your data from unauthorized access to the underlying storage. When enabled, it encrypts all data at rest using encryption keys stored in AWS KMS. This provides an additional layer of data protection for sensitive customer data.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "DynamoDB encryption at rest", "is_correct": True},
                    {"option_text": "DynamoDB Streams", "is_correct": False},
                    {"option_text": "DynamoDB Accelerator (DAX)", "is_correct": False},
                    {"option_text": "DynamoDB Global Tables", "is_correct": False}
                ]
            },
            {
                "question_text": "A Solutions Architect is designing a solution that needs to access and process data from an Amazon S3 bucket in a secure manner. The processing will be done by EC2 instances in a private subnet. What is the MOST secure way to allow the EC2 instances to access the S3 bucket?",
                "explanation": "A VPC endpoint for S3 allows EC2 instances in private subnets to access S3 without requiring internet access, public IP addresses, or NAT devices. When combined with IAM roles for EC2 instances, this provides secure access without exposing long-term credentials.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Create a VPC endpoint for S3 and assign IAM roles to the EC2 instances", "is_correct": True},
                    {"option_text": "Create a NAT gateway and assign public IP addresses to the EC2 instances", "is_correct": False},
                    {"option_text": "Store AWS access keys on the EC2 instances and use public API endpoints", "is_correct": False},
                    {"option_text": "Create an internet gateway and a route to S3 through the public internet", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is migrating a monolithic application to AWS and wants to adopt a microservices architecture. Which combination of AWS services should they consider for a resilient, loosely coupled design?",
                "explanation": "These services together create a resilient, loosely coupled microservices architecture: Lambda provides serverless compute, API Gateway manages API requests, Step Functions coordinates complex workflows, SQS enables asynchronous communication, DynamoDB offers scalable storage, and X-Ray provides visibility into service interactions.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "AWS Lambda, Amazon API Gateway, AWS Step Functions, Amazon SQS, Amazon DynamoDB, and AWS X-Ray", "is_correct": True},
                    {"option_text": "Amazon EC2 with Auto Scaling, Elastic Load Balancing, and Amazon RDS Multi-AZ", "is_correct": False},
                    {"option_text": "Amazon ECS, AWS Fargate, Amazon Aurora, and Amazon CloudWatch", "is_correct": False},
                    {"option_text": "AWS Elastic Beanstalk, Amazon SQS, Amazon ElastiCache, and Amazon CloudFront", "is_correct": False}
                ]
            }
        ],
        "Design High-Performing Architectures": [
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
            },
            {
                "question_text": "A company has a highly transactional application that requires consistent, single-digit millisecond latency. Which AWS database service should they choose?",
                "explanation": "Amazon DynamoDB is a fully managed NoSQL database service that provides fast and predictable performance with seamless scalability. It delivers consistent, single-digit millisecond latency at any scale, making it ideal for highly transactional applications that need predictable performance.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Amazon DynamoDB", "is_correct": True},
                    {"option_text": "Amazon RDS", "is_correct": False},
                    {"option_text": "Amazon Redshift", "is_correct": False},
                    {"option_text": "Amazon Neptune", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is designing a data processing application that needs to process and analyze large amounts of data in parallel. Which AWS service should they use?",
                "explanation": "Amazon EMR is a cloud big data platform for processing vast amounts of data using open source tools such as Apache Spark, Hadoop, HBase, Presto, and Hive. EMR makes it easy to set up, operate, and scale your big data environments by automating time-consuming tasks like provisioning capacity and tuning clusters.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Amazon EMR", "is_correct": True},
                    {"option_text": "Amazon RDS", "is_correct": False},
                    {"option_text": "AWS Lambda", "is_correct": False},
                    {"option_text": "Amazon DynamoDB", "is_correct": False}
                ]
            },
            {
                "question_text": "A Solutions Architect is designing a solution that requires maximum network performance between multiple EC2 instances. What should they implement?",
                "explanation": "EC2 placement groups with cluster placement strategy allow you to place instances close together within a single Availability Zone, providing very low latency and high throughput network performance between instances. This is ideal for applications that require high network performance.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Cluster placement groups", "is_correct": True},
                    {"option_text": "Spread placement groups", "is_correct": False},
                    {"option_text": "Partition placement groups", "is_correct": False},
                    {"option_text": "Dedicated Hosts without placement groups", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is running an application that frequently accesses a small set of objects from Amazon S3. How can they optimize performance?",
                "explanation": "Amazon CloudFront can cache frequently accessed S3 objects at edge locations, reducing latency for global users. For objects accessed repeatedly from S3, CloudFront caching significantly improves performance by serving the content from a location closer to the user with a cached copy.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Use Amazon CloudFront to cache frequently accessed objects", "is_correct": True},
                    {"option_text": "Enable Transfer Acceleration on the S3 bucket", "is_correct": False},
                    {"option_text": "Use S3 Standard-IA storage class for the objects", "is_correct": False},
                    {"option_text": "Enable versioning on the S3 bucket", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has an application that uploads large files to S3 from various locations around the world. How can they improve the upload speed?",
                "explanation": "S3 Transfer Acceleration enables fast, easy, and secure transfers of files to and from Amazon S3 over long distances. It uses Amazon CloudFront's globally distributed edge locations to route data over an optimized network path, accelerating uploads for large files from distant locations.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Enable S3 Transfer Acceleration", "is_correct": True},
                    {"option_text": "Use S3 Standard-IA storage class", "is_correct": False},
                    {"option_text": "Enable S3 versioning", "is_correct": False},
                    {"option_text": "Use S3 batch operations", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs to run a high-performance computing workload with tightly coupled, node-to-node communication. Which EC2 instance feature should they use?",
                "explanation": "Elastic Fabric Adapter (EFA) is a network interface for Amazon EC2 instances that enables customers to run applications requiring high levels of inter-node communications at scale on AWS. It provides lower and more consistent latency and higher throughput than the TCP transport traditionally used in cloud-based HPC systems.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Elastic Fabric Adapter (EFA)", "is_correct": True},
                    {"option_text": "Elastic Network Adapter (ENA)", "is_correct": False},
                    {"option_text": "Enhanced Networking", "is_correct": False},
                    {"option_text": "Elastic IP addresses", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is deploying a machine learning application that requires GPU-based instances. Which Amazon EC2 instance type should they choose?",
                "explanation": "Amazon EC2 P4 instances are accelerated computing instances powered by NVIDIA A100 Tensor Core GPUs and provide high performance for machine learning and high performance computing (HPC) applications. They are designed specifically for compute-intensive machine learning workloads.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "P4 instances", "is_correct": True},
                    {"option_text": "M6g instances", "is_correct": False},
                    {"option_text": "C6g instances", "is_correct": False},
                    {"option_text": "R6g instances", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs to improve the performance of their application that reads data from DynamoDB tables. The application experiences high read latency. What should they implement?",
                "explanation": "DynamoDB Accelerator (DAX) is a fully managed, highly available, in-memory cache for DynamoDB that delivers up to 10x performance improvement by caching frequently accessed data. It reduces the read load on DynamoDB tables and lowers read latency to microseconds.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "DynamoDB Accelerator (DAX)", "is_correct": True},
                    {"option_text": "DynamoDB Streams", "is_correct": False},
                    {"option_text": "DynamoDB Global Tables", "is_correct": False},
                    {"option_text": "DynamoDB Auto Scaling", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is running an application on multiple EC2 instances. The application generates logs that need to be collected and analyzed in real-time. Which AWS service should they use?",
                "explanation": "Amazon Kinesis Data Streams is designed for real-time processing of streaming data at massive scale. It can continuously capture and store terabytes of data per hour from thousands of sources, making it ideal for real-time log collection and analysis from multiple EC2 instances.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Amazon Kinesis Data Streams", "is_correct": True},
                    {"option_text": "Amazon CloudWatch Logs without subscription filters", "is_correct": False},
                    {"option_text": "Amazon S3 with periodic batch uploads", "is_correct": False},
                    {"option_text": "AWS CloudTrail", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs a data warehouse solution that can scale to petabytes and deliver fast query performance. Which AWS service should they use?",
                "explanation": "Amazon Redshift is a fully managed, petabyte-scale data warehouse service designed for analytics workloads. It is optimized for dataset sizes from gigabytes to petabytes and delivers fast query performance through columnar storage technology and parallel query execution.",
                "difficulty": "easy",
                "options": [
                    {"option_text": "Amazon Redshift", "is_correct": True},
                    {"option_text": "Amazon RDS", "is_correct": False},
                    {"option_text": "Amazon DynamoDB", "is_correct": False},
                    {"option_text": "Amazon ElastiCache", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has a web application with rapidly growing traffic. They need a database solution that will automatically scale to accommodate increasing read and write throughput. Which AWS database service should they choose?",
                "explanation": "Amazon DynamoDB with Auto Scaling automatically adjusts provisioned throughput capacity in response to actual traffic patterns. It uses target tracking to add or remove throughput capacity to your tables and global secondary indexes, ensuring high performance with minimal management.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Amazon DynamoDB with Auto Scaling", "is_correct": True},
                    {"option_text": "Amazon RDS with fixed provisioned IOPS", "is_correct": False},
                    {"option_text": "Amazon ElastiCache without read replicas", "is_correct": False},
                    {"option_text": "Amazon Redshift with a fixed node count", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs to deploy compute capacity that can process workloads requiring high memory, storage, and network bandwidth. Which EC2 instance family should they choose?",
                "explanation": "The R family of EC2 instances is specifically designed for memory-intensive applications. They provide the highest ratio of memory to vCPU among EC2 instance types, making them ideal for applications that require high memory, storage, and network bandwidth like in-memory databases and real-time big data analytics.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Memory optimized (R family)", "is_correct": True},
                    {"option_text": "Compute optimized (C family)", "is_correct": False},
                    {"option_text": "Storage optimized (D family)", "is_correct": False},
                    {"option_text": "General purpose (T family)", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is running a latency-sensitive application on EC2 instances. Which networking feature should they enable to achieve higher packet per second (PPS) performance and lower latencies?",
                "explanation": "Enhanced Networking provides higher bandwidth, higher packet per second (PPS) performance, and consistently lower inter-instance latencies. It uses single root I/O virtualization (SR-IOV) to provide high-performance networking capabilities on supported instance types.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Enhanced Networking", "is_correct": True},
                    {"option_text": "VPC Endpoints", "is_correct": False},
                    {"option_text": "Elastic IP addresses", "is_correct": False},
                    {"option_text": "VPC peering", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has an application that needs to upload large files to S3. The application runs on EC2 instances in a private subnet. What is the most efficient way to allow the uploads?",
                "explanation": "A VPC endpoint for S3 enables private connections between your VPC and S3, allowing EC2 instances in private subnets to access S3 without requiring an internet gateway, NAT device, or VPN connection. This provides the most efficient path for uploading large files from private subnets.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Create a Gateway VPC endpoint for S3", "is_correct": True},
                    {"option_text": "Configure a NAT Gateway and Internet Gateway", "is_correct": False},
                    {"option_text": "Set up a VPN connection to S3", "is_correct": False},
                    {"option_text": "Use AWS Direct Connect to connect to S3", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is migrating a MySQL database to AWS. The database is currently 6 TB and is expected to grow. They need a fully managed solution with high availability. Which AWS service should they use?",
                "explanation": "Amazon Aurora is a MySQL and PostgreSQL-compatible relational database built for the cloud that combines the performance and availability of traditional enterprise databases with the simplicity and cost-effectiveness of open source databases. Aurora provides up to 15 read replicas with minimal impact on performance and can scale to handle large databases.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Amazon Aurora", "is_correct": True},
                    {"option_text": "Amazon RDS for MySQL", "is_correct": False},
                    {"option_text": "Amazon DynamoDB", "is_correct": False},
                    {"option_text": "Amazon Redshift", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is designing an application that requires frequent, small, random I/O operations. Which Amazon EBS volume type should they choose?",
                "explanation": "Provisioned IOPS (io2) volumes are designed to meet the needs of I/O-intensive workloads that require consistent and predictable performance. They are especially suitable for workloads that require frequent, small, random I/O operations, such as transactional databases.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Provisioned IOPS (io2)", "is_correct": True},
                    {"option_text": "Throughput Optimized HDD (st1)", "is_correct": False},
                    {"option_text": "Cold HDD (sc1)", "is_correct": False},
                    {"option_text": "Magnetic (standard)", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has a workload that requires high sequential read and write operations on large data sets. Which Amazon EBS volume type is most cost-effective for this workload?",
                "explanation": "Throughput Optimized HDD (st1) volumes are designed for frequently accessed, throughput-intensive workloads that require high sequential read and write operations on large datasets. They provide low-cost magnetic storage that defines performance in terms of throughput rather than IOPS.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Throughput Optimized HDD (st1)", "is_correct": True},
                    {"option_text": "Provisioned IOPS SSD (io2)", "is_correct": False},
                    {"option_text": "General Purpose SSD (gp3)", "is_correct": False},
                    {"option_text": "Cold HDD (sc1)", "is_correct": False}
                ]
            },
            {
                "question_text": "A Solutions Architect is designing a solution for a web application that experiences high traffic during business hours but minimal traffic outside of business hours. How should they configure the Auto Scaling group for optimal performance and cost?",
                "explanation": "Scheduled scaling allows you to set specific times when you know your application will experience increased traffic, automatically increasing capacity before business hours start and decreasing after hours end. Combined with target tracking scaling for unexpected traffic variations, this optimizes both performance and cost.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Use scheduled scaling actions for predictable traffic patterns combined with target tracking scaling policies for unexpected variations", "is_correct": True},
                    {"option_text": "Configure step scaling policies based on CPU utilization", "is_correct": False},
                    {"option_text": "Use simple scaling policies with fixed instance counts", "is_correct": False},
                    {"option_text": "Maintain maximum capacity at all times to handle potential peak loads", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is designing a system to process large datasets with complex queries. They need a massively parallel processing (MPP) database. Which AWS service should they use?",
                "explanation": "Amazon Redshift is a fully managed, petabyte-scale data warehouse service that uses MPP (Massively Parallel Processing) to enable extremely fast queries on large datasets. It's designed for analyzing data using standard SQL and existing BI tools, making it ideal for complex queries on large datasets.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Amazon Redshift", "is_correct": True},
                    {"option_text": "Amazon RDS", "is_correct": False},
                    {"option_text": "Amazon DynamoDB", "is_correct": False},
                    {"option_text": "Amazon Neptune", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has a high-traffic website with a global user base. They want to improve performance and reduce latency for their dynamic content. Which service should they use?",
                "explanation": "AWS Global Accelerator is a networking service that improves the availability and performance of applications with global users. Unlike CloudFront which primarily helps with static content, Global Accelerator optimizes the path from users to applications by using the AWS global network, improving performance for dynamic content.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "AWS Global Accelerator", "is_correct": True},
                    {"option_text": "Amazon CloudFront", "is_correct": False},
                    {"option_text": "Elastic Load Balancing", "is_correct": False},
                    {"option_text": "Amazon Route 53 latency-based routing", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs to optimize the performance of their relational database with minimal code changes. The database has a mix of read and write operations. What should they implement?",
                "explanation": "Amazon RDS with Read Replicas allows you to create read-only copies of your database to offload read queries, improving performance without modifying application code. Connection pooling optimizes database connections, and proper indexing improves query performance, while query caching reduces database load.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Amazon RDS with Read Replicas, connection pooling, proper indexing, and query caching", "is_correct": True},
                    {"option_text": "Amazon DynamoDB with on-demand capacity", "is_correct": False},
                    {"option_text": "Amazon ElastiCache without connection to RDS", "is_correct": False},
                    {"option_text": "Amazon Aurora Serverless with auto-scaling", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is deploying a distributed application that requires shared file storage accessible from multiple EC2 instances concurrently. Which AWS storage service should they use?",
                "explanation": "Amazon EFS provides a simple, scalable, fully managed elastic NFS file system that can be accessed concurrently by thousands of EC2 instances. It's designed to provide massively parallel shared access to files, making it ideal for applications that require shared storage across multiple instances.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Amazon EFS", "is_correct": True},
                    {"option_text": "Amazon EBS", "is_correct": False},
                    {"option_text": "Amazon S3", "is_correct": False},
                    {"option_text": "Amazon FSx for Windows File Server", "is_correct": False}
                ]
            }
        ],
        "Design Cost-Optimized Architectures": [
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
            },
            {
                "question_text": "A company has a database workload with high read intensity but few writes. Which AWS database configuration would be most cost-effective?",
                "explanation": "For read-heavy workloads, a smaller primary RDS instance (to handle writes) with multiple read replicas efficiently distributes the read traffic. This approach is more cost-effective than sizing the primary instance to handle all traffic or using multi-AZ which is designed for high availability rather than performance.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Amazon RDS with a small primary instance and multiple read replicas", "is_correct": True},
                    {"option_text": "Amazon RDS with a large primary instance and no read replicas", "is_correct": False},
                    {"option_text": "Amazon RDS Multi-AZ deployment without read replicas", "is_correct": False},
                    {"option_text": "Amazon Redshift cluster with large node types", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs to optimize costs for an application with unpredictable traffic but requires high availability. Which deployment strategy should they use?",
                "explanation": "Combining a base capacity of Reserved Instances (for predictable minimum traffic) with On-Demand instances (for reliable scaling during traffic increases) and Spot Instances (for cost-efficient handling of peak loads) creates a cost-effective, highly available solution for applications with unpredictable traffic.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Use a mix of Reserved Instances for base capacity, On-Demand for reliable scaling, and Spot Instances for peak handling", "is_correct": True},
                    {"option_text": "Use only On-Demand Instances with Auto Scaling", "is_correct": False},
                    {"option_text": "Use only Reserved Instances sized for peak capacity", "is_correct": False},
                    {"option_text": "Use only Spot Instances with large instance types", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is planning to move rarely accessed archival data to AWS for long-term retention. They rarely expect to retrieve the data. Which storage option is most cost-effective?",
                "explanation": "S3 Glacier Deep Archive is the lowest-cost storage class in Amazon S3, designed for long-term retention of data that is rarely accessed. It offers retrieval times from 12 to 48 hours, making it ideal for archival data that is rarely, if ever, needed but must be retained for compliance purposes.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "S3 Glacier Deep Archive", "is_correct": True},
                    {"option_text": "S3 Standard-IA", "is_correct": False},
                    {"option_text": "S3 One Zone-IA", "is_correct": False},
                    {"option_text": "S3 Glacier", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs to analyze several petabytes of data. The analysis will run for about one week each month. What is the most cost-effective solution?",
                "explanation": "For periodic data processing needs like monthly analytics, Redshift with pause and resume capability allows you to pay only when the cluster is active. This eliminates compute costs when the cluster is not in use, while maintaining your data in storage for the next processing window.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Use Amazon Redshift with the ability to pause and resume the cluster", "is_correct": True},
                    {"option_text": "Run the analysis on a fleet of On-Demand EC2 instances", "is_correct": False},
                    {"option_text": "Purchase Reserved Instances for the EC2 fleet to run the analysis", "is_correct": False},
                    {"option_text": "Use a continuously running Amazon EMR cluster", "is_correct": False}
                ]
            },
            {
                "question_text": "A company wants to optimize costs for their EC2 workload. The application has a base load and variable traffic throughout the day. Which approach will be most cost-effective?",
                "explanation": "This strategy optimizes costs by using Reserved Instances for the predictable base load, taking advantage of their significant discount. Meanwhile, Auto Scaling with On-Demand Instances handles variable traffic, ensuring you only pay for additional capacity when needed. This combination provides the best balance of cost savings and flexibility.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Use Reserved Instances for the base load and Auto Scaling with On-Demand Instances for variable traffic", "is_correct": True},
                    {"option_text": "Use On-Demand Instances for all the workload", "is_correct": False},
                    {"option_text": "Use Reserved Instances for all potential peak capacity", "is_correct": False},
                    {"option_text": "Use Spot Instances for the entire workload", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs to store log files that must be retained for 7 years for compliance reasons. The data will not be accessed during this period. Which is the most cost-effective solution?",
                "explanation": "S3 Lifecycle policies can automatically transition objects between storage classes based on defined rules. For log files that won't be accessed but must be retained, moving them from Standard to Standard-IA after 30 days and to Glacier Deep Archive after 90 days minimizes storage costs while maintaining compliance.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Store the logs in S3 Standard and use lifecycle policies to transition to S3 Standard-IA after 30 days and to S3 Glacier Deep Archive after 90 days", "is_correct": True},
                    {"option_text": "Store the logs directly in S3 Glacier Deep Archive", "is_correct": False},
                    {"option_text": "Store the logs in S3 Standard for the entire 7-year period", "is_correct": False},
                    {"option_text": "Store the logs on EBS volumes attached to EC2 instances", "is_correct": False}
                ]
            },
            {
                "question_text": "A company wants to use AWS but needs to control costs. Which AWS feature should they implement to receive alerts when costs exceed specified thresholds?",
                "explanation": "AWS Budgets allows you to set custom cost and usage budgets that alert you when your costs or usage exceed (or are forecasted to exceed) your budgeted amount. It's specifically designed to help track and control costs by providing notifications when thresholds are reached.",
                "difficulty": "easy",
                "options": [
                    {"option_text": "AWS Budgets", "is_correct": True},
                    {"option_text": "AWS Cost Explorer", "is_correct": False},
                    {"option_text": "AWS Trusted Advisor", "is_correct": False},
                    {"option_text": "Amazon CloudWatch", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has an Auto Scaling group of EC2 instances running behind an Application Load Balancer. The instances handle web traffic that has predictable peak times. What is the most cost-effective scaling strategy?",
                "explanation": "Predictive scaling uses machine learning to predict future traffic and proactively scale resources ahead of forecasted load. For predictable traffic patterns, this ensures capacity is available before needed, preventing over-provisioning while maintaining performance, making it the most cost-effective approach.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Use predictive scaling based on historical traffic patterns", "is_correct": True},
                    {"option_text": "Use dynamic scaling based only on current CPU utilization", "is_correct": False},
                    {"option_text": "Manually adjust the desired capacity before expected peak times", "is_correct": False},
                    {"option_text": "Keep a fixed number of instances running at all times", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is designing a solution that will transfer large amounts of data to AWS. The data transfer needs to be done as quickly and cost-effectively as possible. Which service should they use?",
                "explanation": "AWS Snowball is a petabyte-scale data transport service that uses secure appliances to transfer large amounts of data into and out of AWS. It's designed for moving large datasets cost-effectively, avoiding internet transfer costs while providing faster transfer speeds than internet-based solutions for large datasets.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "AWS Snowball", "is_correct": True},
                    {"option_text": "Amazon S3 Transfer Acceleration", "is_correct": False},
                    {"option_text": "AWS Direct Connect", "is_correct": False},
                    {"option_text": "Amazon CloudFront", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has a workload with data processing requirements that vary greatly, from very low to very high. They want to minimize costs while ensuring that all jobs complete in a timely manner. Which AWS service should they use?",
                "explanation": "AWS Batch dynamically provisions compute resources based on the specific requirements of batch jobs. It automatically scales from zero when no jobs are running to the exact capacity needed for current jobs, eliminating idle resources and optimizing costs for variable workloads.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "AWS Batch", "is_correct": True},
                    {"option_text": "Amazon EC2 with fixed capacity", "is_correct": False},
                    {"option_text": "Amazon ECS with fixed task counts", "is_correct": False},
                    {"option_text": "Amazon Redshift", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is designing a new application and wants to optimize storage costs. The data access pattern will include frequent access for new data, but older data will rarely be accessed. What is the most cost-effective storage strategy?",
                "explanation": "This strategy optimizes costs by automatically managing storage based on access patterns: S3 Intelligent-Tiering monitors and moves objects between tiers based on usage, Standard-IA stores infrequently accessed objects at lower cost, and Glacier Deep Archive provides the lowest cost for rarely accessed archival data.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Use S3 Intelligent-Tiering for new data, with lifecycle policies to move older data to S3 Standard-IA and eventually to S3 Glacier Deep Archive", "is_correct": True},
                    {"option_text": "Store all data in S3 Standard regardless of access pattern", "is_correct": False},
                    {"option_text": "Store all data in S3 Glacier immediately upon creation", "is_correct": False},
                    {"option_text": "Use EBS volumes for all storage needs", "is_correct": False}
                ]
            },
            {
                "question_text": "A company wants to optimize costs for their EC2 instances that run only during business hours (8 AM to 6 PM, Monday to Friday). Which purchasing option should they use?",
                "explanation": "Scheduled Reserved Instances allow you to reserve capacity that recurs on a daily, weekly, or monthly schedule with a specified duration. For instances that only run during business hours, Scheduled Reserved Instances provide significant cost savings compared to On-Demand pricing for the predictable usage pattern.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Scheduled Reserved Instances", "is_correct": True},
                    {"option_text": "Standard Reserved Instances", "is_correct": False},
                    {"option_text": "On-Demand Instances", "is_correct": False},
                    {"option_text": "Dedicated Hosts", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has multiple AWS accounts used by different departments. They want to optimize costs across all accounts. Which AWS feature should they implement?",
                "explanation": "AWS Organizations with Consolidated Billing allows multiple AWS accounts to be managed centrally and billed as a single entity. This enables volume pricing discounts across all accounts, shares Reserved Instance discounts across the organization, and provides centralized cost management capabilities.",
                "difficulty": "easy",
                "options": [
                    {"option_text": "AWS Organizations with Consolidated Billing", "is_correct": True},
                    {"option_text": "AWS Cost Explorer in each account separately", "is_correct": False},
                    {"option_text": "Amazon CloudWatch dashboards", "is_correct": False},
                    {"option_text": "AWS Trusted Advisor in each account", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs to reduce their Amazon RDS costs without impacting performance during business hours. Their database is primarily used during the day, with minimal usage overnight and on weekends. Which approach should they implement?",
                "explanation": "Amazon RDS allows you to stop and start your database instances when they're not in use, charged only for storage during stopped periods. For databases primarily used during business hours, scheduling automatic stop and start for nights and weekends can significantly reduce costs without impacting availability during work hours.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Use Aurora Serverless with automatic pause and resume capability during low usage periods", "is_correct": True},
                    {"option_text": "Use Reserved Instances for the database", "is_correct": False},
                    {"option_text": "Scale down the database instance type during off-hours", "is_correct": False},
                    {"option_text": "Use a Multi-AZ deployment to share the workload", "is_correct": False}
                ]
            },
            {
                "question_text": "A company wants to optimize costs for their development and test environments, which are only used during business hours. What is the most effective approach?",
                "explanation": "Development and test environments that are only needed during business hours can be automatically started and stopped based on a schedule. AWS Instance Scheduler provides this functionality through CloudFormation templates, automating the process and ensuring instances run only when needed for significant cost savings.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Implement AWS Instance Scheduler to automatically stop and start instances outside of business hours", "is_correct": True},
                    {"option_text": "Purchase Reserved Instances for all development and test environments", "is_correct": False},
                    {"option_text": "Run all environments continuously on Spot Instances", "is_correct": False},
                    {"option_text": "Manually start and stop the environments each day", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has large amounts of log data that must be available for occasional analysis. Most of the analysis focuses on the most recent data, with older data accessed very rarely. What is the most cost-effective data storage solution?",
                "explanation": "Amazon S3 lifecycle policies allow you to automatically transition objects between storage classes based on their age. By moving older, less frequently accessed logs to progressively cheaper storage tiers while keeping recent data readily accessible, you can optimize storage costs while maintaining necessary access to all data.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Store data in S3 with lifecycle policies that transition objects from Standard to Standard-IA after 30 days, to Glacier after 90 days, and to Glacier Deep Archive after 180 days", "is_correct": True},
                    {"option_text": "Store all data in Amazon Redshift continuously", "is_correct": False},
                    {"option_text": "Store all data in S3 Standard regardless of age", "is_correct": False},
                    {"option_text": "Delete all log data older than 30 days", "is_correct": False}
                ]
            },
            {
                "question_text": "A company operates a fleet of EC2 instances to run their application. They experience variable traffic but need to maintain high availability. Which Auto Scaling configuration would be most cost-effective?",
                "explanation": "This approach optimizes cost while maintaining availability by using a capacity buffer (min instances > 0) to ensure immediate availability, target tracking scaling to efficiently adjust to traffic changes, and multiple instance types across purchase options to balance cost and reliability based on workload needs.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "Configure a capacity buffer with minimum instances greater than zero, use target tracking scaling policies, and use multiple instance types across purchase options", "is_correct": True},
                    {"option_text": "Set minimum and maximum capacity to the same value based on peak load", "is_correct": False},
                    {"option_text": "Use only On-Demand Instances with no scaling policies", "is_correct": False},
                    {"option_text": "Set minimum capacity to zero and rely solely on simple scaling policies", "is_correct": False}
                ]
            },
            {
                "question_text": "A company wants to identify unused or underutilized resources in their AWS environment to reduce costs. Which AWS service should they use?",
                "explanation": "AWS Trusted Advisor provides real-time guidance to help optimize your AWS infrastructure, improve performance and security, and reduce costs. It includes cost optimization checks that identify idle or underutilized resources, providing specific recommendations for eliminating waste and reducing costs.",
                "difficulty": "easy",
                "options": [
                    {"option_text": "AWS Trusted Advisor", "is_correct": True},
                    {"option_text": "Amazon Inspector", "is_correct": False},
                    {"option_text": "AWS Config", "is_correct": False},
                    {"option_text": "AWS Service Catalog", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has a large number of Amazon EBS volumes, many of which are underutilized. How can they most effectively optimize storage costs?",
                "explanation": "Amazon EBS volumes are billed based on provisioned size, regardless of actual usage. For underutilized volumes, reducing the size to match actual needs directly reduces costs. Using gp3 volumes instead of gp2 provides better price performance for general-purpose workloads, and removing unnecessary snapshots further reduces storage costs.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Resize EBS volumes to match actual usage needs, use gp3 volumes instead of gp2, and remove unnecessary snapshots", "is_correct": True},
                    {"option_text": "Replace all EBS volumes with Instance Store volumes", "is_correct": False},
                    {"option_text": "Create more snapshots of all volumes for backup", "is_correct": False},
                    {"option_text": "Upgrade all volumes to Provisioned IOPS (io2) type", "is_correct": False}
                ]
            },
            {
                "question_text": "A company needs to transfer large amounts of data from their on-premises data center to Amazon S3 on a daily basis. Which transfer method is most cost-effective if they have an existing internet connection with limited bandwidth?",
                "explanation": "AWS Direct Connect provides a dedicated network connection between your on-premises data center and AWS, bypassing the public internet. For large, regular data transfers, it eliminates internet data transfer costs and provides consistent network performance, making it the most cost-effective long-term solution.",
                "difficulty": "hard",
                "options": [
                    {"option_text": "AWS Direct Connect", "is_correct": True},
                    {"option_text": "Amazon S3 Transfer Acceleration", "is_correct": False},
                    {"option_text": "AWS Snowball for daily transfers", "is_correct": False},
                    {"option_text": "Multiple AWS Site-to-Site VPN connections", "is_correct": False}
                ]
            },
            {
                "question_text": "A company is running several underutilized MySQL databases on individual Amazon EC2 instances. How can they reduce costs while maintaining performance?",
                "explanation": "Consolidating multiple underutilized databases onto a single, appropriately sized RDS instance reduces infrastructure costs by eliminating multiple EC2 instances and their associated management overhead. RDS also provides built-in backups, high availability options, and simplified administration.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Migrate the databases to a properly sized Amazon RDS instance", "is_correct": True},
                    {"option_text": "Keep all databases on separate EC2 instances but use Reserved Instances", "is_correct": False},
                    {"option_text": "Move all databases to a smaller instance type", "is_correct": False},
                    {"option_text": "Switch all databases to DynamoDB", "is_correct": False}
                ]
            },
            {
                "question_text": "A company has an application that requires block storage with specific IOPS requirements. Which storage solution is most cost-effective?",
                "explanation": "For applications with specific IOPS requirements, Amazon EBS gp3 volumes provide the most cost-effective solution because they allow you to provision performance (IOPS and throughput) independently of storage capacity. This means you can optimize both performance and cost by tailoring the exact specifications needed.",
                "difficulty": "medium",
                "options": [
                    {"option_text": "Amazon EBS gp3 volumes with provisioned IOPS that match the application requirements", "is_correct": True},
                    {"option_text": "Amazon EBS io2 Block Express volumes", "is_correct": False},
                    {"option_text": "Amazon S3 with frequent GET requests", "is_correct": False},
                    {"option_text": "Amazon EC2 Instance Store volumes", "is_correct": False}
                ]
            }
        ]
    }
    
    # Insert questions into database
    question_count = 0
    
    for category_name, questions_list in questions.items():
        category_id = category_ids[category_name]
        
        for question in questions_list:
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
            question_id = None
            for row in result:
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
    
    print(f"Created {question_count} questions total.")
    
    # Create sample exams
    exams = [
        {
            'title': 'AWS SAA-C03 Practice Exam 1',
            'description': 'A full-length practice exam with questions covering all domains of the AWS Solutions Architect Associate certification.',
            'duration_minutes': 130,
            'pass_percentage': 72.0,
            'is_active': True,
            'question_count': 65
        },
        {
            'title': 'AWS SAA-C03 Security Domain Quiz',
            'description': 'A focused quiz on security-related concepts from the AWS Solutions Architect Associate certification.',
            'duration_minutes': 30,
            'pass_percentage': 70.0,
            'is_active': True,
            'question_count': 15
        },
        {
            'title': 'AWS SAA-C03 Resilient Architectures Quiz',
            'description': 'Test your knowledge of designing resilient and highly available architectures in AWS.',
            'duration_minutes': 30,
            'pass_percentage': 70.0,
            'is_active': True,
            'question_count': 15
        },
        {
            'title': 'AWS SAA-C03 Performance Optimization Quiz',
            'description': 'A quiz focused on optimizing performance of AWS architectures and services.',
            'duration_minutes': 30,
            'pass_percentage': 70.0,
            'is_active': True,
            'question_count': 15
        },
        {
            'title': 'AWS SAA-C03 Cost Optimization Quiz',
            'description': 'Test your knowledge of AWS cost optimization strategies and services.',
            'duration_minutes': 30,
            'pass_percentage': 70.0,
            'is_active': True,
            'question_count': 15
        }
    ]
    
    for exam in exams:
        # Get random questions based on the exam type
        if 'Practice Exam' in exam['title']:
            # For practice exam, get a mix from all categories
            result = execute_sql("SELECT id FROM question")
            all_question_ids = [row[0] for row in result]
            question_ids = sample(all_question_ids, min(exam['question_count'], len(all_question_ids)))
        else:
            # For domain-specific quizzes, get questions from the relevant category
            domain_name = None
            if 'Security' in exam['title']:
                domain_name = 'Design Secure Architectures'
            elif 'Resilient' in exam['title']:
                domain_name = 'Design Resilient Architectures'
            elif 'Performance' in exam['title']:
                domain_name = 'Design High-Performing Architectures'
            elif 'Cost' in exam['title']:
                domain_name = 'Design Cost-Optimized Architectures'
            
            if domain_name:
                result = execute_sql("""
                SELECT q.id FROM question q 
                JOIN question_category c ON q.category_id = c.id 
                WHERE c.name = :category_name
                """, {'category_name': domain_name})
                category_question_ids = [row[0] for row in result]
                question_ids = sample(category_question_ids, min(exam['question_count'], len(category_question_ids)))
        
        # Create the exam
        exam_sql = """
        INSERT INTO exam (title, description, duration_minutes, pass_percentage, created_at, is_active) 
        VALUES (:title, :description, :duration_minutes, :pass_percentage, :created_at, :is_active) 
        RETURNING id
        """
        
        exam_params = {
            'title': exam['title'],
            'description': exam['description'],
            'duration_minutes': exam['duration_minutes'],
            'pass_percentage': exam['pass_percentage'],
            'created_at': datetime.datetime.utcnow(),
            'is_active': exam['is_active']
        }
        
        result = execute_sql(exam_sql, exam_params)
        exam_id = None
        for row in result:
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
        
        print(f"Created exam: {exam['title']} with {len(question_ids)} questions")
    
    print("Database seeding completed.")

# Main execution
if __name__ == "__main__":
    print("Starting to seed the database...")
    create_admin_user()
    category_ids = create_categories()
    create_questions(category_ids)
    print("Database seeding completed successfully.")