import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { unified } from '@astrojs/markdown-remark';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

const [owner, repository] = (process.env.GITHUB_REPOSITORY ?? '').split('/');
const isUserSite = repository === `${owner}.github.io`;
const inferredSite = owner && repository
  ? `https://${owner}.github.io`
  : 'https://example.com';
const inferredBase = owner && repository && !isUserSite ? `/${repository}` : '/';

export default defineConfig({
  output: 'static',
  site: 'https://pkpardeepkumar30.github.io',
  base: process.env.SITE_BASE ?? inferredBase,
  trailingSlash: 'always',
  integrations: [sitemap()],
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex]
    }),
    shikiConfig: {
      theme: 'github-dark'
    }
  }
});
