import Header from '@/components/Header'

export default function Home() {
  return (
    <main className="min-h-screen bg-white">
      <Header />
      
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-16 sm:py-24 lg:py-32">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <div className="text-center lg:text-left">
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 tracking-tight leading-tight">
                Manage Your Podcast Audio Files with Ease
              </h1>
              <p className="mt-6 text-lg sm:text-xl text-gray-600 leading-relaxed">
                Streamline your podcast production workflow with powerful audio management tools. 
                Upload, organize, edit, and publish your episodes all in one place.
              </p>
              <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                <a
                  href="#get-started"
                  className="inline-flex items-center justify-center px-8 py-4 bg-primary hover:bg-primary-hover text-white font-semibold text-lg rounded-lg transition-colors shadow-lg shadow-primary/25 hover:shadow-xl hover:shadow-primary/30"
                >
                  Get Started Free
                </a>
              </div>
              <p className="mt-4 text-sm text-gray-500">
                No credit card required • 14-day free trial
              </p>
            </div>

            {/* Right Placeholder Image */}
            <div className="relative lg:ml-auto">
              <div className="relative w-full aspect-square max-w-lg mx-auto">
                {/* Decorative gradient background */}
                <div className="absolute inset-0 bg-gradient-to-br from-primary/20 via-orange-100 to-amber-50 rounded-3xl transform rotate-3" />
                <div className="absolute inset-0 bg-gradient-to-tr from-primary/10 via-white to-orange-50 rounded-3xl shadow-2xl">
                  {/* Placeholder content */}
                  <div className="absolute inset-0 flex flex-col items-center justify-center p-8">
                    <div className="text-8xl mb-4">🎧</div>
                    <div className="w-full max-w-xs space-y-3">
                      {/* Fake audio waveform bars */}
                      <div className="flex items-end justify-center gap-1 h-16">
                        {[40, 65, 45, 80, 55, 70, 40, 90, 60, 75, 50, 85, 45, 70, 55].map((height, i) => (
                          <div
                            key={i}
                            className="w-2 bg-primary/60 rounded-full"
                            style={{ height: `${height}%` }}
                          />
                        ))}
                      </div>
                      {/* Fake player controls */}
                      <div className="flex items-center justify-center gap-4 mt-4">
                        <div className="w-8 h-8 rounded-full bg-gray-200" />
                        <div className="w-12 h-12 rounded-full bg-primary flex items-center justify-center">
                          <svg className="w-6 h-6 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M8 5v14l11-7z" />
                          </svg>
                        </div>
                        <div className="w-8 h-8 rounded-full bg-gray-200" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Background decoration */}
        <div className="absolute top-0 right-0 -z-10 w-1/2 h-full bg-gradient-to-l from-orange-50 to-transparent" />
        <div className="absolute bottom-0 left-0 -z-10 w-96 h-96 bg-gradient-to-tr from-primary/5 to-transparent rounded-full blur-3xl" />
      </section>
    </main>
  )
}
