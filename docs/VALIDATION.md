# Validation: redesign of 29 October 2026

All results come from a local preview (`python3 -m http.server` over `dist/`) using Chromium 1248 via Playwright and Lighthouse 13.0.1. Each Lighthouse figure is a single lab run, not field data.

## Lighthouse

| Page | Preset | Performance | Accessibility | Best practices | SEO | LCP | CLS | TBT |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Home | mobile | 100 | 100 | 100 | 100 | 1.7 s | 0 | 0 ms |
| Home | desktop | 100 | 100 | 100 | 100 | 0.3 s | 0 | 0 ms |
| Gumora case study | mobile | 100 | 100 | 100 | 100 | 1.4 s | 0 | 0 ms |
| SettleMate case study | mobile | 100 | 100 | 100 | 100 | 0.9 s | 0 | 0 ms |

None of these runs reported a failing accessibility audit.

## Browser checks

- **Layout.** All six content pages were checked at 1440, 1280, 768, 390 and 320 px, in both the light and dark colour schemes. There was no horizontal overflow, no console errors and no failed image requests.
- **Keyboard.** The skip link works, the tab order is logical, and every focused control shows a 3 px outline.
- **Links.** All 55 external links were checked. 53 return 200, LinkedIn returns a 301 redirect, and LeetCode returns 403 to automated requests.
- **`scripts/check.py`.** 479 assertions, 0 failures.
- **Size.** The public artifact (pages, CSS, images and social preview) is about 380 KB.
