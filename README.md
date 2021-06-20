# Development Guideline for codr backend

## Getting started

### Prerequisite Software

| **No** | **Name**           | **Version** | **Notes**                                                                        |
| ------ | ------------------ | ----------- | -------------------------------------------------------------------------------- |
| 1      | Python               | 3.7          |
| 2      | Postgres             | \*          |
| 3      | Visual Studio Code | **Latest**  | Required extensions: **EditorConfig for VS Code**, **auto-pep8 - Code formatter** |
| 4      | Docker             | **Latest**  |

### Start application locally

```docker
docker compose up --build
```

### Run test cases

```python
python -m unittest
```

## Download following [files](https://bitbucket.org/toppr/code_service/downloads/app_secrets.zip) and add it to above folder

## What's In This Document

### 1. [Coding convention](/docs/convention.md)

### 2. [Postman collection](https://www.getpostman.com/collections/f8ab54689ad39891da95)


# Development

## Style Guides

- [PEP8](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

## Development principles

- [Zen of Python.](https://www.python.org/dev/peps/pep-0020/)
- [KISS](https://en.wikipedia.org/wiki/KISS_principle): Keep it simple, Sweetie (not stupid!).
- If there's no way to keep it simple, make sure there are comments.
- Functions/methods/classes/modules must have a single concern.  [Separation of Concern vs Single Responsibility Principle.](https://weblogs.asp.net/arturtrosin/separation-of-concern-vs-single-responsibility-principle-soc-vs-srp)
- Even commits must have a single concern, so commit as often as possible (try not to have an "and" in commit messages).
- Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.  [Stay DRY: Don't repeat yourself](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself).
- Reuse domain/business logic, because those must be always consistent.
- But prefer duplication over  [the wrong abstraction](https://www.sandimetz.com/blog/2016/1/20/the-wrong-abstraction).  [See this interesting HN discussion.](https://news.ycombinator.com/item?id=11032296)
- After all,  [premature generalization](http://wiki.c2.com/?PrematureGeneralization), as well as premature optimization, is the root of all evil.
- Because probably  [YAGNI](https://martinfowler.com/bliki/Yagni.html): You aren't gonna need it.
- Better to isolate code that changes often from code that doesn't.
- [Write code that is easy to delete, not easy to extend](https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to)  Things change in unexpected ways.
- [Feature Toggles (aka Feature Flags)](https://martinfowler.com/articles/feature-toggles.html). They decouple feature releases from merging branches and deploying. And help to decouple behaviors.
- Decoupling is good if it gives you power to easily add, change, or remove code. If not, forget it.
- Pure functions are always decoupled from state and time. Avoid side effects.
- But remember that complex is better than complicated.
- Write readable code. Readable code is less likely to contain bugs, because readability makes bugs more visible.
- Know that design matters.
- And UX matters even more.
- All code should be reviewed.
- All features must be manually tested before going to production.
- And again, keep it simple.
