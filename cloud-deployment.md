# Cloud deployment blueprint

This is a proposed deployment plan, not a live deployment.

- Frontend: S3 + CloudFront or a managed static hosting provider.
- Node gateway and FastAPI service: Docker containers on ECS Fargate or another managed container platform.
- Database: managed PostgreSQL (AWS RDS).
- Cache: managed Redis only after adding actual cache/session/rate-limit usage.
- Files: private object storage bucket with encryption, lifecycle policies, and signed access.
- Secrets: AWS Secrets Manager or equivalent for DB password, JWT secret, and LLM key.
- Observability: structured logs, metrics, traces, health checks, alarms, and retention policies.
- Security: TLS, least-privilege IAM, private database networking, backup/restore testing.
