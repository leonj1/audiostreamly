# AudioStreamly - Project Plan

**Domain:** audiostreamly.com  
**Created:** 2026-02-01  
**Status:** Planning

## Overview

Multi-tenant podcast hosting platform allowing users to upload, manage, and distribute podcasts via RSS feeds. Paid tiers gate upload limits and features.

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│  Frontend (Next.js + TypeScript)                           │
│  └── Hosted on Vercel or Cloudflare Pages                  │
│  └── Auth via Convex Auth (WorkOS integration)             │
└────────────────────────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
┌───────────────────┐   ┌───────────────────────────────────┐
│  Convex           │   │  Cloudflare                        │
│  ├── Auth/WorkOS  │   │  ├── Worker: POST /upload          │
│  ├── Database     │   │  │   → auth check → Convex quota   │
│  │   ├── users    │   │  │   → presigned R2 URL            │
│  │   ├── podcasts │   │  ├── Worker: GET /feed/:id         │
│  │   └── episodes │   │  │   → fetch from Convex → RSS XML │
│  └── Functions    │   │  └── R2 Bucket: audiostreamly      │
│      └── billing  │   │      ├── /audio/:tenantId/:file    │
└───────────────────┘   │      └── /art/:tenantId/:file      │
         │              └───────────────────────────────────┘
         ▼
┌───────────────────┐
│  Autumn           │
│  └── Stripe       │
│  └── Usage gates  │
│  └── Billing UI   │
└───────────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14+, TypeScript, TailwindCSS |
| Backend | Convex (functions + database) |
| Auth | Convex Auth with WorkOS |
| Payments | Autumn → Stripe |
| Storage | Cloudflare R2 |
| Edge Functions | Cloudflare Workers |
| Domain/DNS | Cloudflare |

## Data Model (Convex)

### users
```typescript
{
  _id: Id<"users">,
  email: string,
  name: string,
  autumnCustomerId: string,  // links to Autumn/Stripe
  workosId: string,          // from WorkOS auth
  createdAt: number,
}
```

### podcasts
```typescript
{
  _id: Id<"podcasts">,
  userId: Id<"users">,
  title: string,
  description: string,
  coverUrl: string,          // R2 URL
  language: string,
  category: string,
  explicit: boolean,
  slug: string,              // for RSS: /feed/{slug}
  createdAt: number,
}
```

### episodes
```typescript
{
  _id: Id<"episodes">,
  podcastId: Id<"podcasts">,
  userId: Id<"users">,       // denormalized for queries
  title: string,
  description: string,
  audioUrl: string,          // R2 URL
  durationSeconds: number,
  fileSizeBytes: number,
  episodeNumber: number,
  season?: number,
  publishedAt?: number,      // null = draft
  createdAt: number,
}
```

## Cloudflare Workers

### 1. Upload Worker (`/api/upload`)

**Endpoint:** `POST https://api.audiostreamly.com/upload`

**Flow:**
1. Receive request with JWT token
2. Validate JWT against Convex Auth
3. Call Convex to check user quota (via Autumn)
4. If allowed, generate presigned R2 PUT URL
5. Return URL to client
6. Client uploads directly to R2

### 2. RSS Worker (`/feed/:slug`)

**Endpoint:** `GET https://audiostreamly.com/feed/:slug`

**Flow:**
1. Look up podcast by slug from Convex
2. Fetch published episodes
3. Generate RSS XML following Apple Podcast spec
4. Return with `Content-Type: application/rss+xml`

## Directory Structure

```
audiostreamly/
├── apps/
│   └── web/                    # Next.js frontend
│       ├── app/
│       │   ├── (auth)/         # login, signup
│       │   ├── (dashboard)/    # user dashboard
│       │   │   ├── podcasts/
│       │   │   ├── episodes/
│       │   │   └── billing/
│       │   └── layout.tsx
│       ├── components/
│       └── lib/
├── packages/
│   └── convex/                 # Convex backend
│       ├── schema.ts
│       ├── auth.ts
│       ├── podcasts.ts
│       ├── episodes.ts
│       └── billing.ts
├── workers/
│   ├── upload/                 # R2 presigned URL worker
│   │   ├── src/index.ts
│   │   └── wrangler.toml
│   └── rss/                    # RSS feed worker
│       ├── src/index.ts
│       └── wrangler.toml
└── docs/
    └── PLAN.md                 # this file
```

## Pricing Tiers (Autumn config)

| Tier | Price | Limits |
|------|-------|--------|
| Free | $0 | 1 podcast, 5 episodes, 100MB storage |
| Creator | $9/mo | 3 podcasts, unlimited episodes, 5GB storage |
| Pro | $29/mo | 10 podcasts, unlimited episodes, 50GB storage, analytics |
| Enterprise | Custom | Unlimited, custom domain per podcast, priority support |

## Implementation Phases

### Phase 1: Infrastructure (Parallelizable)
- [ ] **1A.** Cloudflare: Enable R2, create bucket `audiostreamly`
- [ ] **1B.** Cloudflare: Configure DNS for audiostreamly.com
- [ ] **1C.** Convex: Initialize project, define schema
- [ ] **1D.** Autumn: Create account, configure pricing tiers

### Phase 2: Core Backend
- [ ] **2A.** Convex Auth setup with WorkOS
- [ ] **2B.** Convex functions: podcast CRUD
- [ ] **2C.** Convex functions: episode CRUD
- [ ] **2D.** Autumn integration in Convex

### Phase 3: Edge Workers
- [ ] **3A.** Upload worker (presigned URLs)
- [ ] **3B.** RSS feed worker

### Phase 4: Frontend
- [ ] **4A.** Next.js scaffold with auth
- [ ] **4B.** Dashboard: podcast management
- [ ] **4C.** Dashboard: episode upload/management
- [ ] **4D.** Dashboard: billing (Autumn widget)

### Phase 5: Polish & Launch
- [ ] **5A.** Custom domains per podcast (Pro tier)
- [ ] **5B.** Analytics integration
- [ ] **5C.** Landing page
- [ ] **5D.** Documentation

## Concurrent Workstreams

**Can run in parallel:**
- 1A, 1B, 1C, 1D (all infrastructure)
- 2A-2D (once Convex initialized)
- 3A, 3B (independent workers)
- 4A-4D (once backend ready, can parallel UI work)

**Dependencies:**
- Phase 2 requires Phase 1C (Convex)
- Phase 3 requires Phase 1A (R2 bucket)
- Phase 4 requires Phase 2 (backend APIs)

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_CONVEX_URL=
NEXT_PUBLIC_AUTUMN_PUBLISHABLE_KEY=
```

### Convex
```
AUTUMN_SECRET_KEY=
```

### Workers (wrangler.toml)
```
R2_BUCKET=audiostreamly
CONVEX_URL=
```

## Notes

- RSS feeds must be fast → cache at edge, invalidate on episode publish
- Audio files can be large → direct upload to R2, not through Convex
- WorkOS gives us enterprise SSO for free (important for Enterprise tier)
- Autumn handles Stripe webhooks — no webhook code needed

---

## Credentials & Endpoints

| Service | Value |
|---------|-------|
| Convex URL | https://ideal-porpoise-605.convex.site |
| Convex Deployment | ideal-porpoise-605 |
| Cloudflare Account | 5ed28d40a898b43d65b73325d8584b6b |
| Domain | audiostreamly.com (Namecheap) |
| Cloudflare Zone ID | 568111bff0efe2b345077555ed64dbff |

---

*Plan created: 2026-02-01 23:59 EST*
*Updated: 2026-02-02 00:10 EST*
