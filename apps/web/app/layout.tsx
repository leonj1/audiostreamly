import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AudioStreamly - Manage Your Podcast Audio Files with Ease',
  description: 'Streamline your podcast production workflow with powerful audio management tools. Upload, organize, edit, and publish your episodes all in one place.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}
