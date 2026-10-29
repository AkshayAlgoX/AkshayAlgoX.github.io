# Akshaya R — engineering portfolio

A static engineering portfolio with five source-backed case studies. HTML and CSS are served directly by the existing GitHub Pages branch/root deployment. There is no client-side application, package install, tracking script, contact-form backend or font service.

## Authoring and local preview

Requires Python 3.10 or later; standard library only.

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Open `http://localhost:4173/`. The build generates the committed root and `projects/*/index.html` pages and a disposable, allowlisted `dist/` preview. Edit `content/projects.json`, `scripts/build.py` (templates), and `assets/site.css`, then regenerate. Commit the generated pages so GitHub Pages can serve the established `main` / `/` source without a deployment migration. Root-relative links deliberately target this account's root-domain site; a project-subdirectory deployment would need a base-path change.

## Publication boundary

This change is prepared on a review branch. CI only validates: it has read-only repository permissions and no deploy job. GitHub Pages is currently configured to build `main` at `/`. **Merging this branch would publish through that existing route**; review before merging. No production settings need changing.

## Content and evidence

- Five case studies distinguish repository behavior, personal/team attribution, recorded application tests and current availability checks.
- Source links pin the reviewed commit, rather than silently following `main`.
- The case studies intentionally omit unsupported performance headlines and exact changing profile counts.
- Deployment observations are dated, not uptime guarantees. Recheck them when editing.
- The owner-held resume was inspected to support restrained education/internship text. The resume, private contact details and employer source are not hosted.
- Repository retirement and GitHub profile drafts are separate review artifacts, not public-site content.

## Validation

`check.py` validates generated pages, local links/fragments, canonical metadata, JSON-LD, sitemap, image signature, public artifact size, retired-project exclusions and credential/contact patterns. When research checkouts exist alongside this checkout, it also checks the cited file paths; CI does not require those other repositories. These checks are not a replacement for manual claim review or accessibility testing.

The design uses semantic landmarks, normal links, visible keyboard focus, a skip link, responsive typography, system light/dark preferences and reduced-motion support. All essential content is present in HTML. `assets/social.png` is a local 1200 × 630 social preview; crawlers can fetch it after publication. Search inclusion and rich-result presentation are not guaranteed.
