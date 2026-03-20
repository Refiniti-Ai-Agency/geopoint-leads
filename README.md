# Geopoint Leads

React + Vite website with Firebase Hosting.

## Quick Start

```bash
npm run dev      # Start dev server (http://localhost:5173)
npm run build    # Build for production
npm run deploy   # Build and deploy to Firebase Hosting
```

## Firebase Deployment

Project is configured for **geopoint-leads**. First time only:

```bash
npx firebase login
npm run deploy
```

## GitHub Setup

1. Create a new repo at [github.com/new](https://github.com/new) named `geopoint-leads`
2. Add the remote and push:
   ```bash
   git remote add origin https://github.com/YOUR_ORG/geopoint-leads.git
   git push -u origin main
   ```

### Auto-deploy on push

Pushing to `main` triggers a deploy. Add `FIREBASE_TOKEN` as a GitHub secret:

1. Run `npx firebase login:ci` locally and copy the token
2. Repo → Settings → Secrets → Actions → New repository secret
3. Name: `FIREBASE_TOKEN`, Value: (paste token)

---

# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
