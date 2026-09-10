export const siteConfig = {
  name: 'Pardeep Kumar',
  shortName: 'PK',
  title: 'Pardeep Kumar | Education Founder & Builder',
  description: 'Building a school in India. Pardeep Kumar welcomes conversations with investors in Indian education, excellent teachers, and education partners.',
  email: 'pardeep.iitb@gmail.com',
  navigation: [
    { label: 'Home', href: '', enabled: true },
    { label: 'Education', href: 'education/', enabled: true },
    { label: 'About', href: 'about/', enabled: true },
    { label: 'Ventures', href: 'web/', enabled: true },
    { label: 'Writing', href: 'blog/', enabled: true }
  ],
  social: [
    { label: 'Email', href: 'mailto:pardeep.iitb@gmail.com' },
    { label: 'LinkedIn', href: 'https://www.linkedin.com/in/pkpardeepkumar30/' },
    { label: 'GitHub', href: 'https://github.com/pkpardeepkumar30' },
    { label: 'Google Scholar', href: 'https://scholar.google.com/citations?hl=en&user=th4w0rYAAAAJ' }
  ]
} as const;
