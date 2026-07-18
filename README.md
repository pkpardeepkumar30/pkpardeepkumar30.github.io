# Pardeep Kumar — academic website

A fast, static academic website built with [Astro](https://astro.build/). Pages are written in Markdown or generated from small JSON data files; no HTML editing is needed for routine updates.

## Why Astro

Astro is a good fit for a research site because it builds plain static files, ships almost no browser JavaScript by default, supports Markdown content collections, and leaves room for small interactive elements without adopting a client-side framework. This site uses only a few official/lightweight packages for sitemap, RSS, and LaTeX math.

## Quick start

Install [Node.js 24 LTS](https://nodejs.org/) (Node 22.12 or newer also works), then run:

```bash
npm install
npm run dev
```

Open the local address printed in the terminal, normally `http://localhost:4321`.

Before committing, verify the production build:

```bash
npm run check
npm run build
npm run preview
```

## The files you will edit most often

| What | File |
| --- | --- |
| Name, email, profiles, navigation | `src/site.config.ts` |
| Publications | `src/data/publications.json` |
| News on the home page | `src/data/news.json` |
| Research text | `src/pages/research.md` |
| Web CV | `src/pages/cv.md` |
| Talks | `src/data/talks.json` |
| Blog posts | `src/content/blog/*.md` |
| Teaching text | `src/pages/teaching.md` |

## Add a new paper

Edit only `src/data/publications.json`.

1. Copy one complete publication object.
2. Paste it at the top of the array.
3. Give it a unique lowercase `id`, such as `kumar-2027-flash-calculation`.
4. Replace the title, authors, venue, year, summary, links, themes, and BibTeX.
5. Keep an empty string (`""`) for any link that does not exist; empty links are hidden automatically.
6. Remove `"status": "Placeholder entry"` or replace it with a real status such as `"Preprint"`.

Example:

```json
{
  "id": "kumar-2027-example",
  "title": "Your paper title",
  "authors": ["Pardeep Kumar", "Coauthor Name"],
  "venue": "Journal or conference",
  "year": 2027,
  "type": "Journal article",
  "status": "Published",
  "summary": "Two plain-language sentences explaining the contribution.",
  "themes": ["thermodynamics", "optimization"],
  "links": {
    "pdf": "https://example.org/paper.pdf",
    "arxiv": "https://arxiv.org/abs/0000.00000",
    "doi": "https://doi.org/10.xxxx/example",
    "code": "https://github.com/your-account/project"
  },
  "bibtex": "@article{kumar2027example,\n  author = {Kumar, Pardeep and Name, Coauthor},\n  title = {Your paper title},\n  journal = {Journal},\n  year = {2027}\n}"
}
```

The Publications page and the “Recent publications” section on the home page update automatically. To link a research theme to the paper, use `../publications/#your-paper-id` in `src/pages/research.md`.

## Add a new talk

Edit only `src/data/talks.json`. Copy the sample object, give it a unique `id`, and update the title, event, location, ISO date (`YYYY-MM-DD`), type, and optional links. The talks are sorted newest-first automatically.

To show Talks in the main navigation, change its `enabled` value from `false` to `true` in `src/site.config.ts`.

## Add a new blog post

Create one Markdown file in `src/content/blog/`, for example `phase-equilibrium-notes.md`:

```markdown
---
title: "Understanding phase equilibrium"
description: "A short description used in search results and the post list."
published: 2027-02-12
draft: true
tags:
  - thermodynamics
  - numerical methods
---

Write the post here. Inline math uses `$a^2+b^2=c^2$`.

Display math uses:

$$
F(x) = 0
$$
```

Preview drafts locally with `npm run dev`. Change `draft: true` to `draft: false` to publish. Posts are listed newest-first and are included automatically in `/rss.xml`. Enable Blog in `src/site.config.ts` when you want it in the navigation.

## Update the CV and portrait

- Edit the web CV in `src/pages/cv.md`.
- Replace `public/cv/Resume_Pardeep_Kumar_SD.pdf` with a new PDF using the same filename, or update the link in `src/pages/cv.md` if the filename changes.
- Put your portrait at `public/images/profile.jpg`, then change `images/profile-placeholder.svg` to `images/profile.jpg` in `src/pages/index.astro`. Remove the placeholder caption at the same time.

## Add ORCID and GitHub

The ORCID and GitHub entries already exist in `src/site.config.ts` with empty URLs. Add the real URLs and they will appear automatically on the home page. Other profiles can be added by copying one item in the same `social` list.

## Navigation

All navigation is in `src/site.config.ts`. Change one section's `enabled` value to show or hide it. Add another item there when adding a future top-level page.

## GitHub Pages deployment

The workflow at `.github/workflows/deploy.yml` checks and builds the site, then deploys `dist/` whenever `main` is updated.

One-time GitHub setup:

1. Push this repository to GitHub with `main` as the default branch.
2. In the repository, open **Settings → Pages**.
3. Under **Build and deployment**, choose **GitHub Actions** as the source.
4. Push a commit to `main` or run the workflow manually from the **Actions** tab.

The Astro configuration reads `GITHUB_REPOSITORY` during the workflow, so it automatically handles both:

- a personal site: `username.github.io`;
- a project site: `username.github.io/repository-name/`.

For a custom domain, set the repository variable `SITE_URL` to the full origin, such as `https://pardeep.example`, and set `SITE_BASE` to `/`. The fallback `https://example.com` is used only for local builds, so replace it or set `SITE_URL` before using a local production build for SEO validation.

## Project structure

```text
src/
  components/       Reusable display components
  content/blog/     Markdown blog posts
  data/             Publications, talks, and news
  layouts/          Shared page shells and metadata
  pages/            Routes; Markdown pages live here too
  styles/           Site-wide design system
public/
  cv/               Downloadable PDF CV
  images/           Portrait and other static images
.github/workflows/  Automatic GitHub Pages deployment
```

## Content still marked as placeholder

Before making the site public:

- replace the three fake publications;
- replace the sample talk;
- add the real portrait;
- add ORCID and GitHub URLs if desired;
- review the January 2027 defense wording;
- set the sample blog post to published or delete it.
