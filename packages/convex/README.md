# AudioStreamly Convex Backend

## Setup

### 1. Link your Convex project
```bash
npx convex dev
```

### 2. Set environment variables
Run the setup script after linking:
```bash
chmod +x setup-env.sh
./setup-env.sh
```

Or manually set each variable in the Convex Dashboard > Settings > Environment Variables.

### Environment Variables Required

| Variable | Description |
|----------|-------------|
| `JWT_PRIVATE_KEY` | RSA private key for JWT signing |
| `JWKS` | JSON Web Key Set for JWT verification |
| `SITE_URL` | Your frontend URL (e.g., `http://localhost:3000`) |
| `AUTH_WORKOS_CLIENT_ID` | WorkOS Client ID |
| `AUTH_WORKOS_CLIENT_SECRET` | WorkOS API Key |
| `AUTH_WORKOS_CONNECTION_ID` | (Optional) WorkOS Connection ID for SSO |

## WorkOS Configuration

### Callback URL
In your WorkOS Dashboard, configure the callback URL:
```
https://your-convex-deployment.convex.site/api/auth/callback/workos
```

Replace `your-convex-deployment` with your actual Convex deployment name.

### Authentication Flow
1. User clicks "Sign In"
2. User is redirected to WorkOS
3. After authentication, WorkOS redirects back to Convex
4. Convex creates/updates user and sets session cookie
5. User is redirected back to your app

## Schema

The schema includes:
- **Auth tables** (users, sessions, accounts, etc.) from `@convex-dev/auth`
- **userProfiles** - Extended user data (Autumn customer ID, etc.)
- **podcasts** - User's podcasts
- **episodes** - Podcast episodes
