import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  users: defineTable({
    email: v.string(),
    name: v.string(),
    autumnCustomerId: v.optional(v.string()),
    workosId: v.optional(v.string()),
    createdAt: v.number(),
  }).index("by_email", ["email"])
    .index("by_workos", ["workosId"]),

  podcasts: defineTable({
    userId: v.id("users"),
    title: v.string(),
    description: v.string(),
    coverUrl: v.optional(v.string()),
    language: v.string(),
    category: v.string(),
    explicit: v.boolean(),
    slug: v.string(),
    createdAt: v.number(),
  }).index("by_user", ["userId"])
    .index("by_slug", ["slug"]),

  episodes: defineTable({
    podcastId: v.id("podcasts"),
    userId: v.id("users"),
    title: v.string(),
    description: v.string(),
    audioUrl: v.optional(v.string()),
    durationSeconds: v.optional(v.number()),
    fileSizeBytes: v.optional(v.number()),
    episodeNumber: v.number(),
    season: v.optional(v.number()),
    publishedAt: v.optional(v.number()),
    createdAt: v.number(),
  }).index("by_podcast", ["podcastId"])
    .index("by_user", ["userId"])
    .index("by_published", ["podcastId", "publishedAt"]),
});
