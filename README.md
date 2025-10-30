# Pet Shelter Backend - AWS SAM Microservices

**Learning Project**: Building microservices with AWS Lambda, API Gateway, and DynamoDB

**Related Frontend**: https://github.com/ivan-rivera-projects/pet_shelter
**Production URL**: https://pet-shelter.iam-ivan.com/

---

## 🏗️ Architecture Overview

This backend implements a serverless microservices architecture using AWS SAM (Serverless Application Model).

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
│                  https://pet-shelter.iam-ivan.com               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTPS Requests
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Amazon API Gateway (REST)                    │
│                           /Prod Stage                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  GET  /pets          - Retrieve all available pets        │  │
│  │  POST /applications  - Submit adoption application        │  │
│  │  GET  /applications  - Retrieve all applications          │  │
│  └───────────────────────────────────────────────────────────┘  │
└──────┬─────────────────────┬──────────────────────┬─────────────┘
       │                     │                      │
       │                     │                      │
       ▼                     ▼                      ▼
┌─────────────────┐  ┌──────────────────┐  ┌─────────────────────┐
│  Lambda:        │  │  Lambda:         │  │  Lambda:            │
│  getPets        │  │  createApp       │  │  getApplications    │
│                 │  │                  │  │                     │
│  Python 3.11    │  │  Python 3.11     │  │  Python 3.11        │
│  Timeout: 30s   │  │  Timeout: 30s    │  │  Timeout: 30s       │
└────────┬────────┘  └────────┬─────────┘  └─────────┬───────────┘
         │                    │                       │
         │                    │                       │
         ▼                    ▼                       ▼
┌──────────────────┐    ┌─────────────────────────────────────┐
│  DynamoDB:       │    │  DynamoDB:                          │
│  Pets            │    │  Applications                       │
│                  │    │                                     │
│  Key: petId      │    │  Key: applicationId                 │
│  Billing: On-Demand    │  Billing: On-Demand               │
└──────────────────┘    └─────────────────────────────────────┘
```

---

## 📂 Project Structure

```
pet-backend/
├── template.yaml                          # SAM template (Infrastructure as Code)
├── samconfig.toml                        # SAM CLI configuration
├── README.md                             # This file
├── .gitignore                            # Git exclusions
│
└── handlers/                             # Lambda function handlers
    ├── get_pets/
    │   ├── getPets.py                   # GET /pets handler
    │   └── requirements.txt             # Python dependencies
    │
    ├── create_application/
    │   ├── createApplication.py         # POST /applications handler
    │   └── requirements.txt             # Python dependencies
    │
    └── get_applications/
        ├── getApplications.py           # GET /applications handler
        └── requirements.txt             # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

- [AWS CLI](https://aws.amazon.com/cli/) configured with credentials
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Python 3.11+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/ivan-rivera-projects/pet-shelter-backend.git
cd pet-shelter-backend

# Validate the SAM template
sam validate

# Build the application
sam build

# Deploy to AWS (guided - first time)
sam deploy --guided
```

### Guided Deployment Prompts

When running `sam deploy --guided`, you'll be asked:

- **Stack Name**: `pet-shelter-backend` (recommended)
- **AWS Region**: `us-east-1` (or your preferred region)
- **Confirm changes**: `y`
- **Allow SAM CLI IAM role creation**: `y` ⚠️ **Important - creates Lambda execution roles**
- **Disable rollback**: `n`
- **Save to samconfig.toml**: `y`

### Subsequent Deployments

After the first deployment, simply run:

```bash
sam build && sam deploy
```

---

## 🔌 API Endpoints

After deployment, SAM outputs your API Gateway URLs:

### Base URL
```
https://{api-id}.execute-api.us-east-1.amazonaws.com/Prod
```

### Endpoints

#### 1. GET /pets
Retrieve all available pets for adoption.

**Request:**
```bash
curl https://{api-id}.execute-api.us-east-1.amazonaws.com/Prod/pets
```

**Response (200 OK):**
```json
{
  "message": "Successfully got pets",
  "pets": [
    {
      "petId": "1",
      "name": "Buddy",
      "age": 3,
      "species": "Dog",
      "breed": "Golden Retriever",
      "date_entered": "2024-07-01",
      "image": "https://..."
    }
  ]
}
```

#### 2. POST /applications
Submit a new adoption application.

**Request:**
```bash
curl -X POST https://{api-id}.execute-api.us-east-1.amazonaws.com/Prod/applications \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "1",
    "pet_name": "Buddy",
    "species": "Dog",
    "pet_image": "pet1.jpg",
    "applicant_name": "John Doe",
    "email": "john@example.com",
    "phone": "555-123-4567"
  }'
```

**Response (201 Created):**
```json
{
  "message": "Application submitted successfully",
  "application": {
    "applicationId": "a1b2c3d4-...",
    "pet_id": "1",
    "applicant_name": "John Doe",
    "email": "john@example.com",
    "submitted_at": "2024-01-15T10:30:00.000Z",
    "status": "pending"
  }
}
```

#### 3. GET /applications
Retrieve all adoption applications.

**Request:**
```bash
curl https://{api-id}.execute-api.us-east-1.amazonaws.com/Prod/applications
```

**Response (200 OK):**
```json
{
  "message": "Successfully got applications",
  "applications": [...],
  "count": 5
}
```

---

## 🗄️ DynamoDB Tables

### Pets Table

**Primary Key**: `petId` (String)

**Attributes**:
- `petId` - Unique identifier
- `name` - Pet's name
- `age` - Age in years
- `species` - "Dog" or "Cat"
- `breed` - Breed of the pet
- `date_entered` - ISO date when pet entered shelter
- `image` - URL or filename of pet image

### Applications Table

**Primary Key**: `applicationId` (String/UUID)

**Attributes**:
- `applicationId` - UUID generated by Lambda
- `pet_id` - Reference to Pets table
- `pet_name` - Denormalized for convenience
- `pet_image` - Pet image reference
- `species` - Pet species
- `applicant_name` - Full name
- `email` - Contact email
- `phone` - Contact phone
- `submitted_at` - ISO timestamp
- `status` - "pending" | "approved" | "rejected"

---

## 🧪 Testing

### Test GET /pets
```bash
export API_URL=$(aws cloudformation describe-stacks \
  --stack-name pet-shelter-backend \
  --query 'Stacks[0].Outputs[?OutputKey==`PetsAPIBaseURL`].OutputValue' \
  --output text)

curl -i $API_URL/pets
```

### Seed Sample Pet Data

Create a file `seed-pets.json`:
```json
{
  "Pets": [
    {
      "PutRequest": {
        "Item": {
          "petId": {"S": "1"},
          "name": {"S": "Buddy"},
          "age": {"N": "3"},
          "species": {"S": "Dog"},
          "breed": {"S": "Golden Retriever"},
          "date_entered": {"S": "2024-07-01"},
          "image": {"S": "pet1.jpg"}
        }
      }
    }
  ]
}
```

Load data:
```bash
aws dynamodb batch-write-item --request-items file://seed-pets.json
```

---

## 🛠️ AWS Resources Created

When you deploy this SAM template, CloudFormation creates:

1. **2 DynamoDB Tables**
   - `Pets` - Stores pet data
   - `Applications` - Stores adoption applications

2. **1 API Gateway REST API**
   - Stage: `Prod`
   - CORS enabled for all origins

3. **3 Lambda Functions**
   - `getPets` - Handles GET /pets
   - `createApplication` - Handles POST /applications
   - `getApplications` - Handles GET /applications

4. **3 IAM Roles** (auto-generated by SAM)
   - Execution roles for each Lambda with appropriate DynamoDB permissions

5. **CloudWatch Log Groups** (auto-created)
   - One per Lambda function for logging

---

## 🎓 Learning Concepts (AWS Certification)

This project demonstrates key AWS concepts:

### 1. **Serverless Architecture**
- No servers to manage
- Auto-scaling
- Pay-per-request pricing

### 2. **Infrastructure as Code (IaC)**
- SAM template defines all resources
- Version controlled infrastructure
- Repeatable deployments

### 3. **IAM Best Practices**
- Least privilege access
- Service-specific roles
- SAM policy templates (DynamoDBReadPolicy, DynamoDBCrudPolicy)

### 4. **API Gateway Concepts**
- REST API endpoints
- CORS configuration
- Lambda proxy integration
- Stages (Prod)

### 5. **Lambda Function Design**
- Event-driven architecture
- Environment variables
- Error handling and exception catching
- CloudWatch logging

### 6. **DynamoDB Concepts**
- NoSQL database
- Primary keys (partition key)
- Scan operations
- Pagination handling
- On-demand billing mode

---

## 💰 AWS Free Tier Coverage

This application stays within AWS Free Tier limits:

- **Lambda**: 1M requests/month + 400,000 GB-seconds compute
- **API Gateway**: 1M API calls/month (12 months)
- **DynamoDB**: 25 GB storage + 25 read/write capacity units
- **CloudWatch Logs**: 5 GB ingestion + 5 GB storage

**Estimated monthly cost**: $0 for learning/development usage

---

## 🔐 Security Considerations

### Current Implementation (Learning)
- ✅ CORS enabled for all origins (`*`)
- ✅ Lambda functions have minimal IAM permissions
- ⚠️ No authentication/authorization (API is public)
- ⚠️ No input validation middleware
- ⚠️ No rate limiting

### Production Recommendations
- [ ] Add Amazon Cognito for user authentication
- [ ] Implement API Gateway authorizers
- [ ] Add request validation schemas
- [ ] Enable API Gateway throttling
- [ ] Use AWS WAF for additional protection
- [ ] Restrict CORS to specific domains
- [ ] Add DynamoDB encryption at rest
- [ ] Implement CloudTrail logging

---

## 🐛 Troubleshooting

### Deployment Fails with "Stack already exists"
```bash
sam delete
sam deploy --guided
```

### Lambda returns "ResourceNotFoundException"
- DynamoDB table doesn't exist or wrong table name
- Check environment variables in template.yaml
- Verify table was created: `aws dynamodb list-tables`

### API returns 403 Forbidden
- Check Lambda execution role has DynamoDB permissions
- Verify API Gateway CORS configuration
- Check Lambda function logs: `sam logs -n getPets --tail`

### View Lambda Logs
```bash
# Real-time logs
sam logs -n getPets --tail

# Last 10 minutes
sam logs -n getPets --start-time '10min ago'
```

---

## 🔄 CI/CD (Future Enhancement)

To automate backend deployment with GitHub Actions:

1. Create `.github/workflows/deploy-backend.yml`
2. Configure AWS credentials as GitHub secrets
3. On push to `main`, trigger `sam build && sam deploy`

---

## 🧹 Cleanup

To delete all AWS resources and avoid charges:

```bash
sam delete
```

This will:
- Delete all Lambda functions
- Delete API Gateway
- Delete DynamoDB tables (⚠️ **Data will be lost**)
- Delete IAM roles
- Delete CloudWatch log groups

---

## 📚 Additional Resources

- [AWS SAM Developer Guide](https://docs.aws.amazon.com/serverless-application-model/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [Amazon API Gateway](https://docs.aws.amazon.com/apigateway/)
- [Amazon DynamoDB](https://docs.aws.amazon.com/dynamodb/)
- [Boto3 DynamoDB Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html)

---

## 📝 License

This is a learning project for AWS certification preparation.

---

## 🤝 Contributing

This is a personal learning project, but suggestions and improvements are welcome!

---

**Built with ❤️ for learning AWS microservices architecture**
# pet-shelter-backend
