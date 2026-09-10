# Pardeep Kumar — Personal Website

A founder profile focused on building a school in India and connecting with education investors, teachers, and partners. Engineering, independent products, and research provide supporting background.

## Local development

- `npm ci`
- `npm run dev`
- `npm run check`
- `npm run build`

The site uses Astro and retains the existing GitHub Pages deployment workflow. `SITE_URL` and `SITE_BASE` can override the deployment URL and base path.

## Content

- Homepage: `src/pages/index.astro`
- School overview: `src/pages/education.astro`
- Founder background: `src/pages/about.md`
- Contact invitations: `src/components/ConnectCards.astro`
- Navigation and metadata: `src/site.config.ts`
- Founder styling: `src/styles/founder.css`

Keep school content at the level of public purpose and values. Do not add the business plan, funding terms, financial projections, or confidential operating details. Résumé PDFs are retained outside the public directory in `archive/resumes/` and are not included in site builds.
