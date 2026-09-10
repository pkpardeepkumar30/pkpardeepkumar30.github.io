import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { unified } from '@astrojs/markdown-remark';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

export default defineConfig({
  output: 'static',
  site: process.env.SITE_URL ?? 'https://kumarpardeep.com',
  base: process.env.SITE_BASE ?? '/',
  trailingSlash: 'always',
  integrations: [
    sitemap({
      filter: (page) => !['/projects/', '/cv/', '/teaching/'].some((path) => page.endsWith(path))
    })
  ],
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
