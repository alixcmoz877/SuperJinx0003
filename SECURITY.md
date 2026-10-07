# Security Policy

## Reporting

Do not open a public issue for a vulnerability. Contact the repository owner privately and include the affected version, reproduction steps, and impact. Do not include credentials, tokens, subscription URLs, or personal data.

## Deployment rules

- Set `ADMIN_PASSWORD` as a Railway secret. Never commit it.
- Change the admin password immediately after first login.
- Keep the GitHub repository private if it contains deployment metadata.
- Attach a persistent Railway Volume at `/var/lib/marzban`.
- Use least privilege for repository and Railway access.
- Rotate credentials if logs, screenshots, or subscription URLs are exposed.
