#!/bin/bash
# Run this script after linking your Convex project with `npx convex dev`
# IMPORTANT: Replace the placeholder values with your actual credentials

# Generate JWT keys using: node generateKeys.mjs
# Then paste the values below:
echo "Generate JWT keys first by running: node generateKeys.mjs"
echo "Then set them with:"
echo '  npx convex env set JWT_PRIVATE_KEY "your-private-key"'
echo '  npx convex env set JWKS "your-jwks-json"'
echo ""

# Site URL (update for production)
npx convex env set SITE_URL "http://localhost:3000"

# WorkOS credentials - replace with your actual values from WorkOS dashboard
echo "Set WorkOS credentials from your dashboard:"
echo '  npx convex env set AUTH_WORKOS_CLIENT_ID "your-client-id"'
echo '  npx convex env set AUTH_WORKOS_CLIENT_SECRET "your-api-key"'
echo ""

# WorkOS connection ID (optional - leave empty to use AuthKit)
# npx convex env set AUTH_WORKOS_CONNECTION_ID "conn_xxxxx"

echo "Remember to:"
echo "1. Configure the callback URL in WorkOS dashboard"
echo "2. Update SITE_URL for production deployment"
