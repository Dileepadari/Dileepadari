# not_for_you.md

A personal working log. Nothing here is needed by anyone reading the profile.

This repository is the GitHub profile README: the file renders at
<https://github.com/Dileepadari>, and that rendered page is the product. There
is no DEVDOC, for the same reason `Dileepadari.github.io` has none: a one-file
repository with a link checker has no architecture to document, and inventing
one would be filler.

`not_for_you.md` is deliberately not linked from `README.md` either. That file
is a public profile page, and a link to a working log has no business on it.

---

## The overhaul pass, 2026-09-23

### The Gmail button emailed a university address

```html
<a href="mailto:rs200302@rguktsklm.ac.in">
```

An RGUKT Srikakulam student address, on a button labelled Gmail, three
paragraphs below a "Let's Connect" section that gives `adaridileep@gmail.com`.
Anyone who clicked the obvious contact button on the profile was writing to an
address from a previous institution.

### The profile view counter had been broken in public

`profile-counter.deno.dev` is gone. Not the path, the whole service: 404 at
`/dileepadari/count.svg` and 404 at `/` as well. The predecessor,
`profile-counter.glitch.me`, answers 410 Gone.

Loading the live profile confirmed it rather than inferring it: of 45 images on
the rendered page, exactly one had `naturalWidth === 0`, and it sat directly
under the "Profile Views" heading as a 16x16 broken-image icon.

Swapped to `komarev.com/ghpvc`, which is the maintained equivalent and is what
most profile READMEs use.

### Three links that look dead to a script and are not

`codeforces.com` and `leetcode.com` return 403 to anything that is not a
browser, and LinkedIn returns its customary 999. All three are live: browsing
them gave `adaridileep - Codeforces`, `Delhiking - LeetCode Profile` and
`Dileep Kumar Adari | LinkedIn`.

They are in an explicit `ANTI_BOT_HOSTS` map in `scripts/check_links.py` with
the reason and the date they were verified by hand, rather than deleted from the
check. A shorter check that silently covers less is the thing to avoid; the
checker also exits non-zero if it finds no URLs at all, so an empty README
fails instead of reporting success.

I confirmed the checker actually fails by putting the dead counter URL back and
watching it report `HTTP 404`, then restoring the file. A link checker that has
never failed is not evidence of anything.

**There is no schedule on the workflow.** Link rot is caught on the next push or
by running the workflow by hand. That follows the standing "no scheduled CI"
rule, and it is a real limitation: a link can rot the day after a push and go
unnoticed for months.

### The emoji

The headings all carried an emoji (a magnifier on "What I'm Up To", a seedling
on "Current Focus", and so on), thirteen in all. The house rule is no emoji in any file, so they are gone
and the wording is unchanged.

This is the one change here I would most expect to be argued with. Emoji
headings are idiomatic on a profile README and these were clearly deliberate:
eight of the last commits are the owner refining this file. It is one revert
away if the rule was never meant to reach a personal profile page.

### An en dash that thirty repositories' sweeps had missed

The year range after "IIIT Hyderabad" used U+2013, not U+2014, and `scripts/sweep.sh` in the
overhaul skill only grepped for the em dash. The stricter check I wrote for this
repository's CI caught it, so the shared sweep script now looks for both.

A date range is exactly where this character gets typed, and at a glance it is a
hyphen. Worth assuming other finished repositories have them.

### Left alone deliberately

- **The deleted stats workflow stays deleted.** `35a4a72` and `3285265` removed
  `.github/workflows/github-stats.yml` and the `assets/*.svg` it generated,
  four days apart from the same author, which reads as a deliberate move to
  externally hosted stat images. The commented-out block that still referenced
  `./assets/stats.svg` is removed, since those files no longer exist, but
  nothing regenerates them.
- **The externally hosted stat images stay**, on `github-stats-extended.vercel.app`
  and `streak-stats.demolab.com`. Both answer 200. They are third-party services
  that can disappear exactly as the counter did, which is the argument for the
  link checker rather than for vendoring them.
- **No screenshot is committed.** The rendered artefact is the GitHub profile
  page itself; a screenshot of it would be stale the next time a stat image
  updates, which is daily.
- **The bio text is the owner's voice** and is not mine to rewrite. Only the
  emoji, the dead email, the dead counter and the dead comment block changed.
