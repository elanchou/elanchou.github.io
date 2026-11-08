# elanchou.github.io

Personal blog and portfolio at https://elanchou.github.io, built with [Hugo](https://gohugo.io) and the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme.

## Local development

```bash
git clone --recurse-submodules https://github.com/elanchou/elanchou.github.io.git
cd elanchou.github.io
hugo server -D
```

If the theme directory is empty: `git submodule update --init`.

## Structure

```text
content/posts/      blog posts
content/projects/   project pages
content/            about, archives, search, services
layouts/, assets/   template and style overrides
scripts/            helper scripts (scan_cname.py)
themes/PaperMod     theme (git submodule)
```

## Deployment

Pushing to `main` runs `.github/workflows/hugo.yml`, which builds the site and deploys it to GitHub Pages.
