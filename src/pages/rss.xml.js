import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import { siteConfig } from '../site.config';

export async function GET(context) {
  const posts = (await getCollection('blog', ({ data }) => !data.draft))
    .sort((a, b) => b.data.published.valueOf() - a.data.published.valueOf());
  const base = import.meta.env.BASE_URL;

  return rss({
    title: `${siteConfig.name} : Notes`,
    description: 'Notes on curiosity, inquiry-led learning, and the research that shaped how I think about teaching.',
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.published,
      link: `${base}notes/${post.id}/`,
      categories: post.data.tags
    })),
    customData: '<language>en</language>'
  });
}
