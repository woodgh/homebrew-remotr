# Remotr Homebrew Tap

Unofficial Homebrew Cask tap for Remotr. The cask tracks the stable release feed and a scheduled GitHub Actions workflow refreshes the version and SHA-256 daily.

Install:

```sh
brew tap woodgh/homebrew-remotr
brew install --cask remotr
```

Upgrade:

```sh
brew update
brew upgrade --cask remotr
```

The first command adds this unofficial tap. After that, Homebrew can resolve the short cask token `remotr`.
