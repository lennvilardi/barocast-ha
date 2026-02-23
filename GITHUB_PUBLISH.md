# Publication GitHub + HACS (2 dépôts)

Ce projet est maintenant structuré pour **2 dépôts**:

1. **Intégration HACS** (type `integration`)
2. **Carte HACS Dashboard** (type `dashboard` dans l'UI HACS, `plugin` côté backend)

## 1) Dépôt intégration

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

## 2) Dépôt carte Dashboard

Le template prêt à publier se trouve dans:
- `barocast-ha-card/`

### Commandes
```bash
cd /Users/andrevillien/Documents/meteo/barocast-ha-card

git init
git branch -M main
git add .
git commit -m "feat: initial Barocast HA dashboard card"

# IMPORTANT: nom de repo recommandé = barocast-ha-card
# (le fichier JS doit matcher le nom du repo selon les règles HACS plugin/dashboard)

git remote add origin git@github.com:<USER>/barocast-ha-card.git
git push -u origin main

# Recommandé: release
 git tag v0.1.0
 git push origin v0.1.0

# Option GitHub Release (CLI GitHub)
gh release create v0.1.0 \
  --title "Barocast HA Card v0.1.0" \
  --notes-file .github/RELEASE_TEMPLATE.en.md
```

### Ajout dans HACS
- HACS → menu (⋮) → **Custom repositories**
- URL du repo
- Type: **Dashboard**

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
- Carte dashboard:
  - `barocast-ha-card/.github/RELEASE_TEMPLATE.en.md`
  - `barocast-ha-card/.github/RELEASE_TEMPLATE.fr.md`
