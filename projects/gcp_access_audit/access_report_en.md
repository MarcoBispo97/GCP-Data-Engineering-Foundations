# GCP Access Report

**Execution date:** 2026-03-15 00:29:38
**Project path:** C:\Users\marco\Documents\code_classes\GCP-Data-Engineering-Foundations

## Quick read
- GCP connection: ok
- Estimated current level: EDITOR

## What was confirmed as allowed
- Create buckets
- Delete buckets
- Upload objects
- Delete objects
- Read project
- Read project IAM policy
- Read bucket metadata

## What was confirmed as not allowed
- Read objects

## What could not be verified yet
- No items in this category.

## How to read this report
- allowed: confirmed by a real check.
- denied: tested and not allowed in the current scenario.
- not_verified: could not be validated, usually because an API is disabled or visibility is limited.

## Recommended next steps
Ask for object read permission (storage.objects.get).

## Technical appendix
### Structured summary
```json
{
  "Create buckets": "allowed",
  "Delete buckets": "allowed",
  "Upload objects": "allowed",
  "Delete objects": "allowed",
  "Read objects": "denied",
  "Read project": "allowed",
  "Read project IAM policy": "allowed",
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
      "status": "ok",
      "project_id": "global-grammar-432121-d7",
      "project_number": "439286867078",
      "lifecycle_state": "ACTIVE",
      "parent_type": null,
      "parent_id": null
    },
    "iam": {
      "status": "ok",
      "can_read_iam_policy": true,
      "binding_count": 4,
      "etag_present": true
    },
    "permissions": {
      "status": "ok",
      "granted_permissions": [
        "resourcemanager.projects.get",
        "resourcemanager.projects.getIamPolicy",
        "storage.buckets.create",
        "storage.buckets.delete"
      ],
      "missing_permissions": [
        "storage.buckets.get",
        "storage.objects.create",
        "storage.objects.delete",
        "storage.objects.get"
      ],
      "verified": true,
      "not_verified_reason": null
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
      "Create buckets": "allowed",
      "Delete buckets": "allowed",
      "Upload objects": "allowed",
      "Delete objects": "allowed",
      "Read objects": "denied",
      "Read project": "allowed",
      "Read project IAM policy": "allowed",
      "Read bucket metadata": "allowed"
    },
    "access_level": "EDITOR",
    "recommended_actions": [
      "Ask for object read permission (storage.objects.get)."
    ]
  }
}
```
