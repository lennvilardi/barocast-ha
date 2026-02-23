# Publication GitHub + HACS (Intégration)

Ce dépôt contient uniquement l’intégration HACS (`local_weather_forecast`).

Le dépôt de la carte dashboard est séparé:
- https://github.com/lennvilardi/barocast-ha-card

## Dépôt intégration

### Fichiers à publier
- `custom_components/local_weather_forecast/`
- `.github/workflows/validate.yml`
- `hacs.json`
- `README.md`
- `LICENSE`

### Commandes
```bash
cd /Users/andrevillien/Documents/meteo

git init
git branch -M main
git add custom_components .github/workflows/validate.yml hacs.json README.md LICENSE
git commit -m "feat: initial Local Weather Forecast HACS integration"

# Remplace <USER> (repo recommandé: barocast-ha)
git remote add origin git@github.com:<USER>/barocast-ha.git
git push -u origin main

# Recommandé: release
 git tag v0.1.0
 git push origin v0.1.0

# Option GitHub Release (CLI GitHub)
gh release create v0.1.0 \
  --title "Local Weather Forecast v0.1.0" \
  --notes-file .github/RELEASE_TEMPLATE.en.md
```

### Ajout dans HACS
- HACS → menu (⋮) → **Custom repositories**
- URL du repo
- Type: **Integration**

## Vérification secrets avant push
```bash
cd /Users/andrevillien/Documents/meteo
rg -n -S --glob '!.git/**' --glob '!LICENSE' "(api[_-]?key|secret|token|password|passwd|client[_-]?secret|private[_-]?key|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z\\-_]{35}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN)" .
```

Si la commande ne retourne rien, pas de secret détecté par cette passe regex.

## Templates release bilingues
- Intégration:
  - `.github/RELEASE_TEMPLATE.en.md`
  - `.github/RELEASE_TEMPLATE.fr.md`
