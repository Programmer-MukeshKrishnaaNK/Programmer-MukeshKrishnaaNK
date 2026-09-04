# Mukesh's Animated GitHub Profile

## Install

1. Open your profile repository:
   `Programmer-MukeshKrishnaaNK/Programmer-MukeshKrishnaaNK`
2. Replace its README with `README.md`.
3. Upload the `assets/` and `scripts/` folders.
4. Upload `.github/workflows/update-profile.yml`.
5. Commit to `main`.
6. Open **Actions → Update animated profile → Run workflow** once.

The workflow then refreshes the self-hosted SVG stats daily.

## Why SVG?

GitHub sanitizes profile README HTML and does not allow arbitrary JavaScript. SVG is useful here because the artwork can contain declarative animation such as SMIL, while the README only embeds the resulting image.

## Customization

- Edit `assets/hero.svg` to change the visual identity.
- Edit `README.md` for your text and project descriptions.
- Edit `scripts/generate_profile.py` for data generation.
- If GitHub seems to show an old image, bump `?v=1` to `?v=2` in README.md to force a new image URL.

## Important

The workflow uses GitHub's built-in `GITHUB_TOKEN`; you do not need to paste a personal access token into the repository.
