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
      // Redirect stubs and the unlinked background pages stay out of the sitemap.
      filter: (page) =>
        ![
          '/about/',
          '/blog/',
          '/cv/',
          '/education/',
          '/projects/',
          '/publications/',
          '/research/',
          '/software/',
          '/talks/',
          '/teaching/',
          '/web/'
        ].some((path) => page.endsWith(path)) && !page.includes('/blog/')
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
