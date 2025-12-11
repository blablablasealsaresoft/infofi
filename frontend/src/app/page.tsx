'use client'

import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-slate-900 to-slate-950 text-white">
      <main className="container mx-auto px-4 py-16 text-center">
        <h1 className="text-6xl font-bold mb-6">
          🌐 InfoFi
        </h1>
        <p className="text-2xl text-slate-300 mb-4">
          The Bloomberg Terminal for Crypto Reputation & Airdrops
        </p>
        <p className="text-lg text-slate-400 mb-12 max-w-2xl mx-auto">
          Stop manually checking dozens of platforms. Let AI find the alpha for you.
        </p>
        
        <div className="flex gap-4 justify-center">
          <Link 
            href="/dashboard"
            className="px-8 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold transition-colors"
          >
            Launch Dashboard
          </Link>
          <Link 
            href="/login"
            className="px-8 py-3 bg-slate-700 hover:bg-slate-600 rounded-lg font-semibold transition-colors"
          >
            Sign In
          </Link>
        </div>

        <div className="mt-16 grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div className="p-6 bg-slate-800/50 rounded-lg">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-bold mb-2">Unified Dashboard</h3>
            <p className="text-slate-400">
              Track 10+ platforms in one place with real-time updates
            </p>
          </div>
          
          <div className="p-6 bg-slate-800/50 rounded-lg">
            <div className="text-4xl mb-4">🧠</div>
            <h3 className="text-xl font-bold mb-2">AI-Powered Insights</h3>
            <p className="text-slate-400">
              ROI predictions, shill scores, and whale tracking
            </p>
          </div>
          
          <div className="p-6 bg-slate-800/50 rounded-lg">
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="text-xl font-bold mb-2">Real-Time Alerts</h3>
            <p className="text-slate-400">
              Never miss high-value opportunities again
            </p>
          </div>
        </div>

        <div className="mt-12 text-sm text-slate-500">
          <p>Platform Status: <span className="text-green-500">● Online</span></p>
          <p className="mt-2">API Docs: <a href="http://localhost:8000/docs" target="_blank" className="text-blue-400 hover:underline">localhost:8000/docs</a></p>
        </div>
      </main>
    </div>
  )
}

