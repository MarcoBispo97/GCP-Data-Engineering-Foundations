# GCP Access Report

**Execution date:** 2026-03-15 00:16:05
**Project path:** C:\Users\marco\Documents\code_classes\GCP-Data-Engineering-Foundations

## Quick read
- GCP connection: ok
- Estimated current level: RESTRICTED

## What was confirmed as allowed
- Delete buckets
- Upload objects
- Delete objects
- Read bucket metadata

## What was confirmed as not allowed
- Read objects

## What could not be verified yet
- Create buckets
- Read project
- Read project IAM policy

## How to read this report
- allowed: confirmed by a real check.
- denied: tested and not allowed in the current scenario.
- not_verified: could not be validated, usually because an API is disabled or visibility is limited.

## Recommended next steps
Enable Cloud Resource Manager API and run the audit again.

## Technical appendix
### Structured summary
```json
{
  "Create buckets": "not_verified",
  "Delete buckets": "allowed",
  "Upload objects": "allowed",
  "Delete objects": "allowed",
  "Read objects": "denied",
  "Read project": "not_verified",
  "Read project IAM policy": "not_verified",
  "Read bucket metadata": "allowed"
}
```

### Full JSON report
```json
{
  "GCP Access Report": {
    "connection": {
      "status": "ok",
      "project_from_config": "global-grammar-432121-d7",
      "project_from_credentials": "global-grammar-432121-d7"
    },
    "hierarchy": {
      "status": "failed",
      "http_status": 403,
      "error": "{\n  \"error\": {\n    \"code\": 403,\n    \"message\": \"Cloud Resource Manager API has not been used in project global-grammar-432121-d7 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.\",\n    \"status\": \"PERMISSION_DENIED\",\n    \"details\": [\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.ErrorInfo\",\n        \"reason\": \"SERVICE_DISABLED\",\n        \"domain\": \"googleapis.com\",\n        \"metadata\": {\n          \"consumer\": \"projects/global-grammar-432121-d7\",\n          \"service\": \"cloudresourcemanager.googleapis.com\",\n          \"activationUrl\": \"https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7\",\n          \"containerInfo\": \"global-grammar-432121-d7\",\n          \"serviceTitle\": \"Cloud Resource Manager API\"\n        }\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.LocalizedMessage\",\n        \"locale\": \"en-US\",\n        \"message\": \"Cloud Resource Manager API has not been used in project global-grammar-432121-d7 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.\"\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.Help\",\n        \"links\": [\n          {\n            \"description\": \"Google developers console API activation\",\n            \"url\": \"https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7\"\n          }\n        ]\n      }\n    ]\n  }\n}\n"
    },
    "iam": {
      "status": "failed",
      "http_status": 403,
      "can_read_iam_policy": false,
      "error": "{\n  \"error\": {\n    \"code\": 403,\n    \"message\": \"Cloud Resource Manager API has not been used in project global-grammar-432121-d7 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.\",\n    \"status\": \"PERMISSION_DENIED\",\n    \"details\": [\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.ErrorInfo\",\n        \"reason\": \"SERVICE_DISABLED\",\n        \"domain\": \"googleapis.com\",\n        \"metadata\": {\n          \"activationUrl\": \"https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7\",\n          \"containerInfo\": \"global-grammar-432121-d7\",\n          \"consumer\": \"projects/global-grammar-432121-d7\",\n          \"serviceTitle\": \"Cloud Resource Manager API\",\n          \"service\": \"cloudresourcemanager.googleapis.com\"\n        }\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.LocalizedMessage\",\n        \"locale\": \"en-US\",\n        \"message\": \"Cloud Resource Manager API has not been used in project global-grammar-432121-d7 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.\"\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.Help\",\n        \"links\": [\n          {\n            \"description\": \"Google developers console API activation\",\n            \"url\": \"https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7\"\n          }\n        ]\n      }\n    ]\n  }\n}\n"
    },
    "permissions": {
      "status": "failed",
      "http_status": 403,
      "granted_permissions": [],
      "missing_permissions": [
        "resourcemanager.projects.get",
        "resourcemanager.projects.getIamPolicy",
        "storage.buckets.create",
        "storage.buckets.delete",
        "storage.buckets.get",
        "storage.objects.create",
        "storage.objects.delete",
        "storage.objects.get"
      ],
      "error": "{\n  \"error\": {\n    \"code\": 403,\n    \"message\": \"Cloud Resource Manager API has not been used in project global-grammar-432121-d7 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.\",\n    \"status\": \"PERMISSION_DENIED\",\n    \"details\": [\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.ErrorInfo\",\n        \"reason\": \"SERVICE_DISABLED\",\n        \"domain\": \"googleapis.com\",\n        \"metadata\": {\n          \"serviceTitle\": \"Cloud Resource Manager API\",\n          \"service\": \"cloudresourcemanager.googleapis.com\",\n          \"containerInfo\": \"global-grammar-432121-d7\",\n          \"activationUrl\": \"https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7\",\n          \"consumer\": \"projects/global-grammar-432121-d7\"\n        }\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.LocalizedMessage\",\n        \"locale\": \"en-US\",\n        \"message\": \"Cloud Resource Manager API has not been used in project global-grammar-432121-d7 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.\"\n      },\n      {\n        \"@type\": \"type.googleapis.com/google.rpc.Help\",\n        \"links\": [\n          {\n            \"description\": \"Google developers console API activation\",\n            \"url\": \"https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=global-grammar-432121-d7\"\n          }\n        ]\n      }\n    ]\n  }\n}\n",
      "verified": false,
      "not_verified_reason": "resource_manager_api_disabled"
    },
    "storage_bucket_permissions": {
      "status": "ok",
      "verified": true,
      "requested_permissions": [
        "storage.buckets.get",
        "storage.buckets.delete",
        "storage.objects.create",
        "storage.objects.delete",
        "storage.objects.get"
      ],
      "granted_permissions": [
        "storage.buckets.delete",
        "storage.buckets.get",
        "storage.objects.create",
        "storage.objects.delete"
      ],
      "not_verified_reason": null
    },
    "capabilities": {
      "Create buckets": "not_verified",
      "Delete buckets": "allowed",
      "Upload objects": "allowed",
      "Delete objects": "allowed",
      "Read objects": "denied",
      "Read project": "not_verified",
      "Read project IAM policy": "not_verified",
      "Read bucket metadata": "allowed"
    },
    "access_level": "RESTRICTED",
    "recommended_actions": [
      "Enable Cloud Resource Manager API and run the audit again."
    ]
  }
}
```
