export interface Env {
  CONVEX_URL: string;
}

interface Podcast {
  title: string;
  description: string;
  coverUrl: string;
  language: string;
  category: string;
  explicit: boolean;
}

interface Episode {
  title: string;
  description: string;
  audioUrl: string;
  durationSeconds: number;
  fileSizeBytes: number;
  publishedAt: number;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const slug = url.pathname.replace("/feed/", "").replace("/", "");

    if (!slug) {
      return new Response("Podcast slug required", { status: 400 });
    }

    try {
      // TODO: Fetch podcast and episodes from Convex
      // const podcast = await fetchFromConvex(env.CONVEX_URL, "podcasts:getBySlug", { slug });
      // const episodes = await fetchFromConvex(env.CONVEX_URL, "episodes:getPublished", { podcastId: podcast._id });

      // Placeholder response
      const rss = generateRSS(
        {
          title: "Sample Podcast",
          description: "A sample podcast",
          coverUrl: "https://example.com/cover.jpg",
          language: "en",
          category: "Technology",
          explicit: false,
        },
        []
      );

      return new Response(rss, {
        headers: {
          "Content-Type": "application/rss+xml; charset=utf-8",
          "Cache-Control": "public, max-age=300",
        },
      });
    } catch (error) {
      return new Response("Feed not found", { status: 404 });
    }
  },
};

function generateRSS(podcast: Podcast, episodes: Episode[]): string {
  const escapeXml = (s: string) =>
    s.replace(/&/g, "&amp;")
     .replace(/</g, "&lt;")
     .replace(/>/g, "&gt;")
     .replace(/"/g, "&quot;");

  const formatDuration = (seconds: number): string => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return h > 0 ? `${h}:${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`
                 : `${m}:${s.toString().padStart(2, "0")}`;
  };

  const episodeItems = episodes.map(ep => `
    <item>
      <title>${escapeXml(ep.title)}</title>
      <description><![CDATA[${ep.description}]]></description>
      <enclosure url="${escapeXml(ep.audioUrl)}" type="audio/mpeg" length="${ep.fileSizeBytes}"/>
      <itunes:duration>${formatDuration(ep.durationSeconds)}</itunes:duration>
      <pubDate>${new Date(ep.publishedAt).toUTCString()}</pubDate>
      <guid isPermaLink="false">${escapeXml(ep.audioUrl)}</guid>
    </item>
  `).join("\n");

  return `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" 
     xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"
     xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>${escapeXml(podcast.title)}</title>
    <description><![CDATA[${podcast.description}]]></description>
    <language>${podcast.language}</language>
    <itunes:image href="${escapeXml(podcast.coverUrl)}"/>
    <itunes:category text="${escapeXml(podcast.category)}"/>
    <itunes:explicit>${podcast.explicit ? "yes" : "no"}</itunes:explicit>
    ${episodeItems}
  </channel>
</rss>`;
}
