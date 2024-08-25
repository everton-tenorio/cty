# CONCY

concy - Conventional Commits CLI

```bash
usage: concy [-h] -t {fix,feat,docs,style,refactor,test,chore,build,ci,perf,revert} [--emoji]


options:
  -h, --help            show this help message and exit
  -t {fix,feat,docs,style,refactor,test,chore,build,ci,perf,revert}, --type {fix,feat,docs,style,refactor,test,chore,build,ci,perf,revert}
                        Tipo de commit (fix, feat, docs, style, refactor, test, chore, build, ci, perf,
                        revert)
  --emoji, -e           Tipo com emojis no commit
```

[!concy]('./concy.png')

## Conventional Commits 1.0.0

The [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification is a lightweight convention on top of commit messages.

The commit message should be structured as follows:

```plaintext
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```
