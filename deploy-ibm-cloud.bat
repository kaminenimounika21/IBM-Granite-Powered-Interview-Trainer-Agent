@echo off
REM ==============================================================================
REM IBM Cloud Code Engine Automated Deployment Script
REM Target: IBM Cloud Lite / Pay-As-You-Go with IBM Code Engine & Container Registry
REM ==============================================================================

echo [1/6] Logging in to IBM Cloud...
REM Usage: ibmcloud login -a cloud.ibm.com -r us-south -g Default --apikey YOUR_API_KEY
ibmcloud target -r us-south -g Default

echo [2/6] Logging into IBM Cloud Container Registry (ICR)...
ibmcloud cr login
ibmcloud cr namespace-add ibm-interview-trainer 2>nul

echo [3/6] Building Container Image locally or with IBM Code Engine...
docker build -t us.icr.io/ibm-interview-trainer/agent:latest -f deploy/Dockerfile .

echo [4/6] Pushing Image to IBM Container Registry...
docker push us.icr.io/ibm-interview-trainer/agent:latest

echo [5/6] Creating / Updating IBM Code Engine Application...
ibmcloud ce project select --name ibm-skillsbuild-project 2>nul
if %errorlevel% neq 0 (
    echo Creating project ibm-skillsbuild-project...
    ibmcloud ce project create --name ibm-skillsbuild-project
)

ibmcloud ce app create --name ibm-granite-trainer ^
  --image us.icr.io/ibm-interview-trainer/agent:latest ^
  --port 8000 ^
  --min-scale 0 ^
  --max-scale 2 ^
  --cpu 0.25 ^
  --memory 0.5G ^
  --env WATSONX_URL=https://us-south.ml.cloud.ibm.com ^
  --env WATSONX_MODEL_ID=ibm/granite-3-8b-instruct ^
  --env WATSONX_APIKEY=%WATSONX_APIKEY% ^
  --env WATSONX_PROJECT_ID=%WATSONX_PROJECT_ID%

echo [6/6] Deployment finished! Retrieving Public URL...
ibmcloud ce app get --name ibm-granite-trainer --output url
pause
