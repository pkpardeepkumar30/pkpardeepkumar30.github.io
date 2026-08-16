export const siteConfig = {
  name: 'Pardeep Kumar',
  shortName: 'PK',
  title: 'Pardeep Kumar | Scientific Computing Researcher',
  description:
    'Scientific computing, numerical methods, and an emerging teaching practice focused on making mathematics and physics approachable.',
  email: 'pardeep.iitb@gmail.com',
  location: 'Amsterdam, The Netherlands',
  affiliations: [
    { name: 'CWI Amsterdam', href: 'https://www.cwi.nl/' },
    { name: 'TU Delft', href: 'https://www.tudelft.nl/' }
  ],
  navigation: [
    { label: 'Home', href: '', enabled: true },
    { label: 'Research', href: 'research/', enabled: true },
    { label: 'Publications', href: 'publications/', enabled: true },
    { label: 'Teaching', href: 'teaching/', enabled: true },
    { label: 'CV', href: 'cv/', enabled: true },
    { label: 'Blog', href: 'blog/', enabled: true },
    { label: 'Web', href: 'web/', enabled: true },
    { label: 'Talks', href: 'talks/', enabled: false },
  ],
  social: [
    { label: 'Email', href: 'mailto:pardeep.iitb@gmail.com' },
    {
      label: 'Google Scholar',
      href: 'https://scholar.google.com/citations?hl=en&user=th4w0rYAAAAJ'
    },
    {
      label: 'LinkedIn',
      href: 'https://www.linkedin.com/in/pkpardeepkumar30/'
    },
    {
      label: 'ResearchGate',
      href: 'https://www.researchgate.net/profile/Pardeep-Kumar-87?ev=hdr_xprf'
    },
    // Add your real profile URLs when ready; empty links are not displayed.
    { label: 'ORCID', href: '' },
    { label: 'GitHub', href: 'https://github.com/pkpardeepkumar30' }
  ]
} as const;
