# Validation: AI/ML positioning pass of 29 October 2026

All results come from a local preview (`python3 -m http.server` over `dist/`) using Chromium 1248 via Playwright and Lighthouse 13.0.1. Each Lighthouse figure is a single lab run, not field data.

## Lighthouse

| Page | Preset | Performance | Accessibility | Best practices | SEO | LCP | CLS | TBT |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Home | mobile | 100 | 100 | 100 | 100 | 1.7 s | 0 | 0 ms |
| Home | desktop | 100 | 100 | 100 | 100 | 0.4 s | 0 | 0 ms |
| SettleMate case study | mobile | 100 | 100 | 100 | 100 | 0.9 s | 0 | 0 ms |
| Due Diligence case study | desktop | 100 | 100 | 100 | 100 | 0.3 s | 0 | 0 ms |

None of these runs reported a failing accessibility audit.

## Browser checks

- **Layout.** All six content pages were checked at 1440, 1280, 768, 390 and 320 px, in both the light and dark colour schemes. There was no horizontal overflow and there were no console errors. Every image loaded, with no 4xx responses, once the page was scrolled slowly enough for lazy images to finish.
- **Keyboard.** The skip link works, the tab order is logical, and every focused control (54 stops on the home page, 20 on a case study) shows a visible outline.
- **Arrows.** No page contains Unicode arrow characters; `check.py` enforces this. The only directional icon is one inline SVG chevron, used on "All projects" and next-project links. It has `aria-hidden="true"` and `focusable="false"`.
- **Links.** All 59 external links were checked. 57 return 200. LinkedIn returns 999 and LeetCode returns 403 to automated requests (bot blocking), so they were not verified by this check.
- **`scripts/check.py`.** 520 assertions, 0 failures.
- **Size.** The public artifact (pages, CSS, images and social preview) is about 388 KB.
