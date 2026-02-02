import type { Metadata } from 'next'
import './globals.css'
import { ConvexClientProvider } from '@/components/ConvexClientProvider'

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
      <body className="antialiased">
        <ConvexClientProvider>
          {children}
        </ConvexClientProvider>
      </body>
    </html>
  )
}
