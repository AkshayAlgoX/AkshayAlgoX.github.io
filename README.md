# Akshaya R: portfolio

Source for [akshayalgox.github.io](https://akshayalgox.github.io): a personal engineering portfolio with five project case studies. It is plain HTML and CSS served by GitHub Pages from `main` at `/`. There is no JavaScript, no font service, no tracking and no contact form.

## Edit and preview

Requires Python 3.10+ (standard library only).

```sh
python3 scripts/build.py     # regenerates index.html, 404.html, projects/*/index.html, sitemap.xml, robots.txt and dist/
python3 scripts/check.py     # structure, links, metadata, images and claim guardrails
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

What lives where:

- `content/site.json` holds all text: profile, about, experience, featured projects (homepage summary and case study) and the smaller projects.
- `scripts/build.py` holds the page templates and the small inline SVG diagrams.
- `assets/site.css` is the only stylesheet. It includes light and dark themes, a colour per project, responsive layouts and reduced-motion support.
- `assets/img/` holds project screenshots taken from each project's own repository, converted to WebP at 1200 px and 640 px.

Commit the generated pages: GitHub Pages serves them directly. CI rebuilds the site and fails if the committed pages differ from what the sources produce.

## Content rules

- **Code links are pinned.** Every case study links to code at a pinned commit (`sha` in `site.json`). Update the SHA when a project changes.
- **Results are stated exactly as recorded:**
  - HackerRank Orchestrate (September 2026): rank #85 of 3,062, score 68.2/100.
  - Amazon ML Challenge 2026: Team Duty_Drive, public leaderboard #1,200, score 0.978758.
- **Live status is plain.** Where a demo is offline, the page says so in one line.
- **Team work is credited.** The Due Diligence page lists the team.
- **Retired and unsupported claims are blocked.** `check.py` rejects retired projects and unsupported claims (for example uptime or onboarding percentages, or OR-Tools as SettleMate's running engine), as well as `mailto:` and `tel:` links.
- **Résumé link.** None is published yet. To add one, set `profile.resume_url` in `site.json` and rebuild.
