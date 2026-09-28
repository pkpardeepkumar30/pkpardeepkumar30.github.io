export const siteConfig = {
  name: 'Pardeep Kumar',
  shortName: 'PK',
  title: 'Pardeep Kumar | Curiosity-driven school education',
  description:
    'Engineer, researcher, and future education founder. Why I believe curiosity and inquiry-led learning belong to every child, not only the privileged.',
  email: 'pardeep.iitb@gmail.com',
  navigation: [
    { label: 'Home', href: '', enabled: true },
    { label: 'My story', href: 'my-story/', enabled: true },
    { label: 'What I believe', href: 'what-i-believe/', enabled: true },
    { label: 'Notes', href: 'notes/', enabled: true },
    { label: 'Contact', href: 'contact/', enabled: true }
  ],
  social: [
    { label: 'Email', href: 'mailto:pardeep.iitb@gmail.com' },
    { label: 'LinkedIn', href: 'https://www.linkedin.com/in/pkpardeepkumar30/' },
    { label: 'GitHub', href: 'https://github.com/pkpardeepkumar30' },
    { label: 'Google Scholar', href: 'https://scholar.google.com/citations?hl=en&user=th4w0rYAAAAJ' }
  ]
} as const;
