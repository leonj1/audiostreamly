import Header from '@/components/Header'

export default function Home() {
  return (
    <main className="min-h-screen bg-white scroll-smooth">
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
                  href="#pricing"
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

      {/* Features Section */}
      <section id="features" className="py-16 sm:py-24 bg-gray-50 scroll-mt-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900">
              Everything You Need to Podcast
            </h2>
            <p className="mt-4 text-lg text-gray-600 max-w-2xl mx-auto">
              Powerful features designed to make podcast hosting simple, fast, and affordable.
            </p>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* Feature 1 */}
            <div className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition-shadow">
              <div className="w-14 h-14 bg-primary/10 rounded-xl flex items-center justify-center mb-6">
                <span className="text-3xl">📤</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                Upload & Organize
              </h3>
              <p className="text-gray-600">
                Drag and drop your audio files. Organize episodes with tags, seasons, and custom metadata.
              </p>
            </div>

            {/* Feature 2 */}
            <div className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition-shadow">
              <div className="w-14 h-14 bg-primary/10 rounded-xl flex items-center justify-center mb-6">
                <span className="text-3xl">📡</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                Auto-Generate RSS
              </h3>
              <p className="text-gray-600">
                Instant RSS feed generation compatible with Apple Podcasts, Spotify, and all major platforms.
              </p>
            </div>

            {/* Feature 3 */}
            <div className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition-shadow">
              <div className="w-14 h-14 bg-primary/10 rounded-xl flex items-center justify-center mb-6">
                <span className="text-3xl">📊</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                Analytics Dashboard
              </h3>
              <p className="text-gray-600">
                Track downloads, listener locations, and engagement metrics with beautiful dashboards.
              </p>
            </div>

            {/* Feature 4 */}
            <div className="bg-white rounded-2xl p-8 shadow-sm hover:shadow-md transition-shadow">
              <div className="w-14 h-14 bg-primary/10 rounded-xl flex items-center justify-center mb-6">
                <span className="text-3xl">🎙️</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                Multi-Podcast Support
              </h3>
              <p className="text-gray-600">
                Manage multiple shows from one account. Perfect for networks and prolific creators.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-16 sm:py-24 scroll-mt-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900">
              Simple, Transparent Pricing
            </h2>
            <p className="mt-4 text-lg text-gray-600 max-w-2xl mx-auto">
              Start free and scale as you grow. No hidden fees, no surprises.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {/* Free Tier */}
            <div className="bg-white rounded-2xl p-8 border border-gray-200 hover:border-gray-300 transition-colors">
              <h3 className="text-xl font-semibold text-gray-900">Free</h3>
              <div className="mt-4 flex items-baseline">
                <span className="text-4xl font-bold text-gray-900">$0</span>
                <span className="ml-2 text-gray-500">/month</span>
              </div>
              <p className="mt-4 text-gray-600">Perfect for getting started</p>
              <ul className="mt-8 space-y-4">
                <li className="flex items-center gap-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600">1 podcast</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600">5 episodes</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600">100MB storage</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600">Basic RSS feed</span>
                </li>
              </ul>
              <a
                href="#get-started"
                className="mt-8 block w-full py-3 px-4 text-center font-medium rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 transition-colors"
              >
                Start Free
              </a>
            </div>

            {/* Creator Tier - Most Popular */}
            <div className="bg-white rounded-2xl p-8 border-2 border-primary relative shadow-lg">
              <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                <span className="bg-primary text-white text-sm font-medium px-4 py-1 rounded-full">
                  Most Popular
                </span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900">Creator</h3>
              <div className="mt-4 flex items-baseline">
                <span className="text-4xl font-bold text-gray-900">$9</span>
                <span className="ml-2 text-gray-500">/month</span>
              </div>
              <p className="mt-4 text-gray-600">For serious podcasters</p>
              <ul className="mt-8 space-y-4">
                <li className="flex items-center gap-3">
                  <span className="text-primary">✓</span>
                  <span className="text-gray-600">3 podcasts</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="text-primary">✓</span>
                  <span className="text-gray-600">Unlimited episodes</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="text-primary">✓</span>
                  <span className="text-gray-600">5GB storage</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="text-primary">✓</span>
                  <span className="text-gray-600">Custom RSS feeds</span>
                </li>
              </ul>
              <a
                href="#get-started"
                className="mt-8 block w-full py-3 px-4 text-center font-semibold rounded-lg bg-primary hover:bg-primary-hover text-white transition-colors"
              >
                Get Started
              </a>
            </div>

            {/* Pro Tier */}
            <div className="bg-white rounded-2xl p-8 border border-gray-200 hover:border-gray-300 transition-colors">
              <h3 className="text-xl font-semibold text-gray-900">Pro</h3>
              <div className="mt-4 flex items-baseline">
                <span className="text-4xl font-bold text-gray-900">$29</span>
                <span className="ml-2 text-gray-500">/month</span>
              </div>
              <p className="mt-4 text-gray-600">For networks & professionals</p>
              <ul className="mt-8 space-y-4">
                <li className="flex items-center gap-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600">10 podcasts</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600">Unlimited episodes</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600">50GB storage</span>
                </li>
                <li className="flex items-center gap-3">
                  <span className="text-green-500">✓</span>
                  <span className="text-gray-600">Advanced analytics</span>
                </li>
              </ul>
              <a
                href="#get-started"
                className="mt-8 block w-full py-3 px-4 text-center font-medium rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 transition-colors"
              >
                Go Pro
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-16 sm:py-24 bg-gray-50 scroll-mt-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900">
              About AudioStreamly
            </h2>
            <div className="mt-8 text-lg text-gray-600 space-y-6">
              <p>
                We believe every voice deserves to be heard. AudioStreamly was born from a simple idea: 
                podcast hosting shouldn&apos;t be complicated or expensive.
              </p>
              <p>
                Our mission is to democratize podcasting by providing powerful, professional-grade tools 
                at prices anyone can afford. Whether you&apos;re starting your first show or managing a 
                network of podcasts, we&apos;ve got you covered.
              </p>
              <p>
                Built by podcasters, for podcasters. We understand the challenges of creating great 
                content, and we&apos;re here to handle the technical stuff so you can focus on what 
                matters most—your message.
              </p>
            </div>
            <div className="mt-10 flex items-center justify-center gap-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-primary">10K+</div>
                <div className="text-sm text-gray-500">Podcasters</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-primary">500K+</div>
                <div className="text-sm text-gray-500">Episodes Hosted</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-primary">50M+</div>
                <div className="text-sm text-gray-500">Downloads</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-16 sm:py-24 scroll-mt-16">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl mx-auto text-center">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900">
              Get In Touch
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Have questions? We&apos;d love to hear from you. Send us a message and we&apos;ll respond as soon as possible.
            </p>
            
            <div className="mt-10 bg-gray-50 rounded-2xl p-8">
              <form className="space-y-6">
                <div className="grid sm:grid-cols-2 gap-4">
                  <input
                    type="text"
                    placeholder="Your name"
                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all"
                  />
                  <input
                    type="email"
                    placeholder="Your email"
                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all"
                  />
                </div>
                <textarea
                  placeholder="Your message"
                  rows={4}
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all resize-none"
                />
                <button
                  type="submit"
                  className="w-full sm:w-auto px-8 py-3 bg-primary hover:bg-primary-hover text-white font-semibold rounded-lg transition-colors"
                >
                  Send Message
                </button>
              </form>
              
              <div className="mt-8 pt-8 border-t border-gray-200">
                <p className="text-gray-600">
                  Or email us directly at{' '}
                  <a href="mailto:hello@audiostreamly.com" className="text-primary hover:underline font-medium">
                    hello@audiostreamly.com
                  </a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-12">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <span className="text-2xl">🎙️</span>
              <span className="text-xl font-bold text-white">AudioStreamly</span>
            </div>
            <p className="text-sm">
              © 2024 AudioStreamly. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </main>
  )
}
