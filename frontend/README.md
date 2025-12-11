# InfoFi Frontend

Next.js 14 frontend for the InfoFi intelligence platform.

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Set Environment Variables

Create a `.env.local` file:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js 14 App Router
│   │   ├── layout.tsx    # Root layout
│   │   ├── page.tsx      # Landing page
│   │   ├── globals.css   # Global styles
│   │   └── providers.tsx # React Query provider
│   ├── components/       # React components
│   │   ├── ui/          # UI components (shadcn/ui)
│   │   ├── dashboard/   # Dashboard components
│   │   ├── analytics/   # Analytics components
│   │   └── layout/      # Layout components
│   ├── lib/             # Utilities
│   │   ├── api/        # API client
│   │   ├── hooks/      # Custom hooks
│   │   └── utils/      # Utility functions
│   └── store/          # State management (Zustand)
├── public/             # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.js
```

## Tech Stack

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Query** - Data fetching
- **Axios** - HTTP client
- **Wagmi** - Web3 wallet integration
- **Zustand** - State management

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)

