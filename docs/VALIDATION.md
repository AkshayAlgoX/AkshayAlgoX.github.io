# Review validation — 29 October 2026

The portfolio remains a static GitHub Pages site. Review branch only; publication is not part of this change.

## Measured local results

Lighthouse 13.0.1, installed Brave/HeadlessChrome 156, with axe-core 4.14.0. The home-page runs were sequential, on the loopback Python static server, using Lighthouse's default mobile simulated throttling and its desktop preset. These are single laboratory samples, not field Core Web Vitals or production CDN measurements.

| Page / preset | Performance | Accessibility | Best practices | SEO | FCP | LCP | CLS | TBT |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Home / mobile | 100 | 100 | 100 | 100 | 0.8 s | 0.9 s | 0 | 0 ms |
| Home / desktop | 100 | 100 | 100 | 100 | 0.2 s | 0.2 s | 0 | 0 ms |

Each of the five case studies measured 100 for accessibility, best practices and SEO. Performance was measured on the homepage only. The custom 404 measured accessibility/best-practices 100 and SEO 66 because it intentionally declares `noindex`.

The first home audit found a non-scored accessible-name mismatch on the brand link. That was corrected, and all final accessibility audit failures are empty. Automated checks cannot establish complete accessibility conformance.

## Build and browser checks

- `python3 scripts/build.py` produces six content pages, custom 404, CSS, favicon, a 1200 × 630 PNG, sitemap and robots file. No runtime JavaScript or external fonts.
- `python3 scripts/check.py`: 583 assertions, zero failures with adjacent source snapshots available. Checks include local URLs/fragments, pinned source file existence, metadata, JSON-LD, public artifact size and claim guardrails. CI has fewer assertions because it intentionally does not clone the featured projects.
- Public preview artifact: 123,810 bytes across all public files; this includes the social image, which normal page loads do not request.
- Six content pages inspected at 320, 390, 768 and 1440 CSS-pixel widths: 24 page/viewport observations, no horizontal overflow.
- Browser review covered mobile and desktop renders, selected-work navigation, a case-study link, contents anchors, skip-link keyboard focus and visible focus outline. Case-study anchors settled below the 96-pixel scroll offset on desktop.
- Browser warning/error log captured for the final case-study session was empty. This is scoped to that session, not a statement about every external destination.
- Light rendering inspected from the Lighthouse screenshot; dark rendering inspected in the in-app browser. Native system theme preference and reduced-motion CSS determine presentation. No theme persistence or animation dependency.

## Claim review corrections

The current Gumora auth routes contradict its README's cookie-only-session description: `/token` returns the token and refresh accepts a body token. The case study records this remaining limitation, rather than claiming it was fixed. A README link to a missing authentication document was replaced with the actual source route. This portfolio does not modify Gumora.

SettleMate names the actual TypeScript branch-and-bound engine, keeps OR-Tools external/reference scope clear, states the HMAC secret-key requirement and distinguishes emitted SMT-LIB from runtime Z3. Candidate truncation and timeout limitations are included.

Competition results distinguish individual September rank from the Amazon team public leaderboard. Application test counts are explicitly recorded project results, not portfolio-run tests. Team 03 contributor attribution is preserved without an official membership count. No private resume, phone, email or employer source is included.

## Deployment boundary

GitHub API inspection showed legacy Pages from `main` at `/`, HTTPS enforced. Generated pages are committed at those paths, with `.nojekyll`, and CI checks regeneration consistency. CI has read-only contents permission and no deploy step. A merge would trigger the pre-existing Pages route; no merge or publication has been performed.

Local root-relative routes are correct for `akshayalgox.github.io`. They are not configured for an arbitrary repository subpath. Production cache behavior, actual search indexing and social-platform unfurl behavior can only be measured after an approved publication.
