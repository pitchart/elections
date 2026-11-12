# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Nature du dépôt

Kata de refactoring « Elections » : le même code legacy est porté dans plusieurs langages, chaque dossier de premier niveau est un projet autonome (`java/`, `kotlin/`, `csharp/`, `cpp/`, `typescript/`, `python/`). Il n'y a pas de build ni de code partagé entre eux.

Le code est volontairement sale (duplication, structures parallèles, branchement sur un booléen). Le but du kata (voir `README.md`) : refactorer, puis ajouter deux fonctionnalités anti-fraude :
- un vote d'un électeur d'un autre district est compté nul ;
- personne ne peut voter deux fois.

Ne pas « nettoyer » une version en passant sans que cela soit demandé : le code legacy est la matière de l'exercice.

## Architecture (identique dans tous les langages)

Une seule classe `Elections`, construite avec la liste des électeurs par district (`District 1/2/3`) et un booléen `withDistrict`.
- `addCandidate` : enregistre un candidat officiel.
- `voteFor(elector, candidate, electorDistrict)` : un candidat inconnu est ajouté à la liste des candidats mais pas à celle des officiels (vote nul) ; une chaîne vide est un vote blanc.
- `results()` : renvoie une map candidat → pourcentage formaté à la française (`"12,50%"`), plus les clés `Blank`, `Null`, `Abstention`.

Deux modes de calcul coexistent dans `results()` : sans district (pourcentage direct des votes valides) et avec districts (le vainqueur de chaque district gagne une part égale). Les structures de votes sont des listes parallèles indexées comme `candidates` (et par district en mode district). Les districts sont codés en dur.

## Commandes par langage

Depuis le dossier du langage concerné :

| Langage | Tests | Test unique |
|---|---|---|
| Python (uv, 3.11) | `uv sync` puis `uv run pytest` | `uv run pytest tests/test_elections.py::test_election_without_districts` |
| Java (Gradle) | `./gradlew test` | `./gradlew test --tests org.elections.ElectionsTest` |
| Kotlin (Gradle) | `./gradlew test` | `./gradlew test --tests org.elections.ElectionsTest` |
| C# (.NET) | `dotnet test` dans `csharp/elections` | `dotnet test --filter <NomDuTest>` |
| C++ (g++ C++20, doctest) | `make` (compile puis exécute `out/elections`) | non prévu par le Makefile |
| TypeScript (TSDX) | `yarn install` puis `yarn test` (`--watch` possible) | `yarn test -t "<nom>"` |

### Python : outillage

`python/pyproject.toml` définit des tâches taskipy (`uv run task <nom>`), nommées `intention` ou `intention:action` ou `intention:outil:action` (pas de tiret) :
- `lint` (= `lint:ruff` + `lint:types` mypy strict sur `src/` + `test:robot:lint` Robocop) ; `lint:ruff` = `lint:ruff:check` (ruff check) + `lint:ruff:format` (ruff format --check)
- `format` (corrige et formate tout : `format:ruff:fix` puis `format:ruff`)
- `test` (= `test:unit` pytest + `test:robot` Robot Framework)
- `check` : pipeline complète, `clean`

Ruff est configuré avec une complexité McCabe maximale de 10 et `S101` (assert) autorisé uniquement dans `tests/`. `pytest` est lancé avec `--testdox --cov=src` par défaut. `lint:ruff:check` et `lint:ruff:format` échouent sur le code legacy de `src/` (lignes longues, complexité) : c'est la matière du kata.

### Python : tests Robot Framework

Tout est sous `python/tests/robot/` : les `.robot` à la racine, les librairies Python dans `libraries/`, les fichiers ApprovalTests dans `approvals/` (un par scénario, nommé `elections.<nom_du_scénario>.approved.json`). Lancer avec `uv run task test:robot`, linter avec `uv run task test:robot:lint` (Robocop, avec la règle maison `BDD01` dans `robocop_rules/`). Les mots-clés Given/When/Then sont des mots-clés à arguments embarqués de `ElectionsLibrary`; `ApprovalLibrary.py` est un simple module utilitaire (pas une librairie Robot).

## État du travail en cours (branche `feat/robot-framework`)

- Les tests Python utilisent ApprovalTests (`verify_as_json`) : les fichiers `*.approved.json` à côté des tests sont la référence, à relire avant de les accepter.
- `python/tests/RCN3410.robot` est un squelette sans rapport, exclu de Robocop et non exécuté par `test:robot`. Les scénarios de `python/tests/robot/elections.robot` sont fonctionnels.
- Le port Python n'a pas la même structure que les autres : les noms sont en snake_case (`vote_for`, `add_candidate`) et les types sont annotés (mypy strict).
