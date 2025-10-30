# Pet Shelter Backend - Complete Deployment Guide

This guide walks you through deploying the Pet Shelter microservices backend and integrating it with the React frontend.

---

## 📋 Prerequisites Checklist

- [x] AWS CLI configured (`aws sts get-caller-identity` works)
- [x] AWS SAM CLI installed (`sam --version` works)
- [x] Python 3.11+ installed
- [x] Git configured
- [ ] GitHub account ready
- [ ] Frontend repo at https://github.com/ivan-rivera-projects/pet_shelter

---

## 🚀 Part 1: Backend Deployment (30-45 minutes)

### Step 1: Push Backend to GitHub

```bash
# Navigate to backend directory
cd /Users/ivanrivera/Downloads/AWS/dev/pet-backend

# Create repository on GitHub:
# Go to https://github.com/new
# Name: pet-shelter-backend
# Description: AWS SAM microservices backend for Pet Shelter
# Visibility: Public (or Private)
# DO NOT initialize with README

# Add remote and push
git remote add origin https://github.com/ivan-rivera-projects/pet-shelter-backend.git
git branch -M main
git push -u origin main
```

**✅ Checkpoint**: Verify your repo is live at https://github.com/ivan-rivera-projects/pet-shelter-backend

---

### Step 2: Validate SAM Template

```bash
cd /Users/ivanrivera/Downloads/AWS/dev/pet-backend

# Validate template syntax
sam validate
```

**Expected Output**: `/path/to/template.yaml is a valid SAM Template`

---

### Step 3: Build and Deploy Backend

```bash
# Build Lambda functions
sam build

# Deploy to AWS
sam deploy
```

**Deployment Prompts**:
- Confirm changes: `y`

**⏱️ This takes 3-5 minutes**

**Expected Output**:
```
Successfully created/updated stack - pet-shelter-backend in us-east-1

Outputs
-------
Key                 PetsAPIBaseURL
Description         Base URL for Pet Shelter API Gateway
Value               https://abc123xyz.execute-api.us-east-1.amazonaws.com/Prod

Key                 GetPetsEndpoint
Value               https://abc123xyz.execute-api.us-east-1.amazonaws.com/Prod/pets

Key                 CreateApplicationEndpoint
Value               https://abc123xyz.execute-api.us-east-1.amazonaws.com/Prod/applications

Key                 GetApplicationsEndpoint
Value               https://abc123xyz.execute-api.us-east-1.amazonaws.com/Prod/applications
```

**📝 IMPORTANT: Copy the `PetsAPIBaseURL` value - you'll need it for the frontend!**

Example: `https://abc123xyz.execute-api.us-east-1.amazonaws.com/Prod`

---

### Step 4: Verify DynamoDB Tables Created

```bash
# List DynamoDB tables
aws dynamodb list-tables
```

**Expected Output**: Should include `Pets` and `Applications`

---

### Step 5: Populate Pets Table with Data

```bash
cd /Users/ivanrivera/Downloads/AWS/dev/pet-backend

# Run the data population script
python scripts/populate_pets_table.py
```

**Expected Output**:
```
Starting to populate Pets table...
✓ Added: Buddy (Dog) - ID: 1
✓ Added: Mittens (Cat) - ID: 2
✓ Added: Max (Dog) - ID: 3
...
Total pets added: 9
```

---

### Step 6: Test GET /pets Endpoint

```bash
# Replace with YOUR actual API URL
export API_URL=https://abc123xyz.execute-api.us-east-1.amazonaws.com/Prod

# Test the pets endpoint
curl -i $API_URL/pets
```

**Expected Output (200 OK)**:
```json
{
  "message": "Successfully got pets",
  "pets": [
    {
      "id": 1,
      "name": "Buddy",
      "age": 2,
      "species": "Dog",
      "breed": "Golden Retriever",
      "date_entered": "2024-07-01",
      "image": "pet5.jpeg"
    },
    ...
  ]
}
```

**✅ Checkpoint**: If you see pet data, the backend is working!

---

### Step 7: Create S3 Bucket for Pet Images

```bash
cd /Users/ivanrivera/Downloads/AWS/dev/pet-backend

# Create the bucket
python scripts/create_images_bucket.py
```

**Expected Output**:
```
Creating S3 bucket: images-954976299507-20250130
Region: us-east-1
✓ Bucket created successfully
✓ Block public access turned off
✓ Public read policy applied
✓ CORS configuration applied

SUCCESSFULLY COMPLETED. Bucket name is: images-954976299507-20250130

Next steps:
1. Upload images: cd pet-shelter-client/src/assets
2. Run: aws s3 cp . s3://images-954976299507-20250130/images/ --recursive
3. Set frontend .env variable:
   VITE_PET_IMAGES_BUCKET_URL='https://images-954976299507-20250130.s3.us-east-1.amazonaws.com/images'
```

**📝 IMPORTANT: Copy the bucket name - you'll need it!**

---

### Step 8: Upload Pet Images to S3

```bash
# Navigate to frontend assets
cd /Users/ivanrivera/Downloads/AWS/dev/pet-shelter-client/src/assets

# Upload images (REPLACE with YOUR bucket name!)
aws s3 cp . s3://images-954976299507-20250130/images/ --recursive
```

**Expected Output**:
```
upload: ./pet5.jpeg to s3://images-954976299507-20250130/images/pet5.jpeg
upload: ./pet-image2.jpeg to s3://images-954976299507-20250130/images/pet-image2.jpeg
...
```

---

### Step 9: Test All Backend Endpoints

```bash
# Set your API URL
export API_URL=https://abc123xyz.execute-api.us-east-1.amazonaws.com/Prod

# Test GET /pets
curl $API_URL/pets | jq '.pets | length'
# Expected: 9

# Test POST /applications
curl -X POST $API_URL/applications \
  -H "Content-Type: application/json" \
  -d '{
    "pet_id": "1",
    "pet_name": "Buddy",
    "species": "Dog",
    "pet_image": "pet5.jpeg",
    "applicant_name": "Test User",
    "email": "test@example.com",
    "phone": "555-1234"
  }'

# Test GET /applications
curl $API_URL/applications | jq '.count'
# Expected: 1 (from the test above)
```

**✅ Backend Complete!** All endpoints are working!

---

## 🎨 Part 2: Frontend Integration (20-30 minutes)

### Step 10: Update Frontend Environment Variables

```bash
cd /Users/ivanrivera/Downloads/AWS/dev/pet-shelter-client

# Edit .env file
# Replace with YOUR actual URLs
```

**Edit `.env`**:
```bash
# API Gateway Base URL (from Step 3)
VITE_API_GATEWAY_URL='https://abc123xyz.execute-api.us-east-1.amazonaws.com/Prod'

# S3 Bucket URL for images (from Step 7)
VITE_PET_IMAGES_BUCKET_URL='https://images-954976299507-20250130.s3.us-east-1.amazonaws.com/images'
```

---

### Step 11: Create API Service Layer

I'll create the API service file next (run this after I provide the code).

**✅ Checkpoint**: Save the .env file

---

## 📊 Deployment Summary

After completing all steps:

### Backend Resources Created:
- ✅ 2 DynamoDB tables (Pets, Applications)
- ✅ 3 Lambda functions (getPets, createApplication, getApplications)
- ✅ 1 API Gateway (with 3 endpoints)
- ✅ 3 IAM execution roles (auto-generated by SAM)
- ✅ 1 S3 bucket for images
- ✅ CloudWatch Log Groups (for Lambda logging)

### Frontend Changes Needed:
- [ ] Create `src/services/api.js`
- [ ] Update `App.jsx` (remove hardcoded pets, fetch from API)
- [ ] Update `Pets.jsx` (load images from S3)
- [ ] Update `AdoptionForm.jsx` (POST to API)
- [ ] Update `Applications.jsx` (fetch from API)

---

## 🐛 Troubleshooting

### "ResourceNotFoundException" when calling API
```bash
# Check DynamoDB tables exist
aws dynamodb list-tables

# Re-run population script
python scripts/populate_pets_table.py
```

### "CORS error" in browser console
- CORS is already configured in template.yaml
- Try refreshing the browser with Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

### Images not loading
```bash
# Verify images in S3
aws s3 ls s3://YOUR-BUCKET-NAME/images/

# Check bucket policy
aws s3api get-bucket-policy --bucket YOUR-BUCKET-NAME
```

### API returns 500 error
```bash
# Check Lambda logs
sam logs -n getPets --tail

# Or in AWS Console
# CloudWatch > Log Groups > /aws/lambda/getPets
```

---

## 🎯 Next Steps

**Where you are now**: Backend deployed and tested ✅

**Next task**: Integrate frontend with backend APIs

**Estimated time**: 20-30 minutes

Would you like me to create the frontend integration code now?

---

## 📚 Learning Resources

- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [API Gateway CORS](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors.html)
- [Lambda Error Handling](https://docs.aws.amazon.com/lambda/latest/dg/python-exceptions.html)

---

**Last Updated**: January 2025
**AWS Region**: us-east-1
**Stack Name**: pet-shelter-backend
