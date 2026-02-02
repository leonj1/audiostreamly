export interface Env {
  BUCKET: R2Bucket;
  CONVEX_URL: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method === "OPTIONS") {
      return handleCORS();
    }

    if (request.method !== "POST") {
      return new Response("Method not allowed", { status: 405 });
    }

    try {
      // TODO: Validate JWT from Authorization header against Convex
      // TODO: Check quota via Autumn
      
      const { filename, contentType, podcastId } = await request.json() as {
        filename: string;
        contentType: string;
        podcastId: string;
      };

      // Generate unique key
      const key = `audio/${podcastId}/${Date.now()}-${filename}`;
      
      // For now, return the key - presigned URLs require additional setup
      // In production, use R2's presigned URL feature
      return new Response(JSON.stringify({
        key,
        uploadUrl: `https://audiostreamly.r2.cloudflarestorage.com/${key}`,
        publicUrl: `https://cdn.audiostreamly.com/${key}`,
      }), {
        headers: {
          "Content-Type": "application/json",
          ...corsHeaders,
        },
      });
    } catch (error) {
      return new Response(JSON.stringify({ error: "Upload failed" }), {
        status: 500,
        headers: { "Content-Type": "application/json", ...corsHeaders },
      });
    }
  },
};

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

function handleCORS(): Response {
  return new Response(null, { status: 204, headers: corsHeaders });
}
